# client/fl_client.py
# Each FL client:
#   1. Generates a Dilithium keypair on init
#   2. Receives common initial weights once
#   3. Trains locally on its private data
#   4. Signs its updated weights

import hashlib
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

from model.cnn import SmallCNN
from crypto import dilithium_utils
from utils.weights import apply_weight_arrays, weights_to_bytes


USE_HASH = False


class FederatedClient:
    def __init__(self, client_id: str, dataloader: DataLoader, device: str):
        self.client_id = client_id
        self.dataloader = dataloader
        self.device = device
        self.model = SmallCNN().to(device)

        # loss and optimizer
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)

        # ── Dilithium keygen ──────────────────────────────────
        self.pk, self.sk, keygen_ms = dilithium_utils.keygen()
        print(
            f"  [{client_id}] keygen : {keygen_ms:.2f} ms  "
            f"(pk={len(self.pk)}B  sk={len(self.sk)}B)"
        )

    def local_train(self, global_weight_arrays=None, epochs=1):
        if global_weight_arrays is not None:
            apply_weight_arrays(self.model, global_weight_arrays)

        if epochs == 0:
            return

        self.model.train()
        total_loss = 0.0

        for _ in range(epochs):
            for x, y in self.dataloader:
                x, y = x.to(self.device), y.to(self.device)

                self.optimizer.zero_grad()
                output = self.model(x)
                loss = self.criterion(output, y)
                loss.backward()
                self.optimizer.step()

                total_loss += loss.item()

        print(f"  [{self.client_id}] trained  | loss: {total_loss / len(self.dataloader):.4f}")

    def sign_update(self) -> dict:
        update_bytes = weights_to_bytes(self.model)

        if USE_HASH:
            payload = hashlib.sha256(update_bytes).digest()
            mode = "HASHED"
        else:
            payload = update_bytes
            mode = "RAW"

        signature, sign_ms = dilithium_utils.sign(self.sk, payload)

        print(
            f"  [{self.client_id}] signed ({mode}) | {sign_ms:.3f} ms  "
            f"input={len(payload)} B  update={len(update_bytes)/1024:.1f} KB  "
            f"sig={len(signature)} B"
        )

        return {
            "client_id": self.client_id,
            "update_bytes": update_bytes,
            "payload": payload,
            "signature": signature,
            "sign_ms": sign_ms,
        }