#  Secure Decentralized Federated Learning using Gossip Protocol

##  Overview

This project implements a **fully decentralized federated learning (FL) system** using a **gossip-based communication protocol** and **post-quantum cryptographic signatures (Dilithium)** for secure model updates.

Unlike traditional federated learning systems that rely on a **central server**, this implementation eliminates central aggregation and enables **peer-to-peer model exchange and aggregation**.

---

##  Key Features

*  **Decentralized Training**
  No central server is used for aggregation — all nodes collaborate via peer-to-peer gossip.

*  **Gossip Protocol Communication**
  Model updates are propagated using a **push-based randomized gossip protocol**.

*  **Post-Quantum Security (Dilithium)**
  Each client signs its model updates using **Dilithium digital signatures**, ensuring integrity and authenticity.

*  **Local Model Aggregation**
  Each node aggregates received updates independently using decentralized FedAvg-style aggregation.

*  **Efficient Propagation**
  Controlled using:

  * `fanout` (number of peers)
  * `max_hops` (propagation depth)

---

##  System Architecture

```text
          +-----------+
          | Client 0  |
          +-----------+
                |
                v
      +-------------------+
      | Gossip Protocol   |
      +-------------------+
          /      |      \
         v       v       v
   +---------+ +---------+ +---------+
   | Client1 | | Client2 | | Client3 |
   +---------+ +---------+ +---------+
```

Each client:

* trains locally
* signs updates
* sends updates to random peers
* verifies received updates
* aggregates locally

---

##  Workflow

1. **Initialization**

   * All clients start with a **common initial model**

2. **Local Training**

   * Each client trains on its private dataset

3. **Signing**

   * Model updates are signed using Dilithium

4. **Gossip Propagation**

   * Updates are shared with randomly selected peers

5. **Verification**

   * Each node verifies received updates

6. **Local Aggregation**

   * Each node aggregates valid updates locally

7. **Repeat**

   * The process continues for multiple rounds

---

## ⚙️ Configuration

```python
N_CLIENTS = 4
N_ROUNDS = 3
LOCAL_EPOCHS = 15
SAMPLES_PER_CLIENT = 500
GOSSIP_FANOUT = 2
GOSSIP_MAX_HOPS = 3
```

---

##  How to Run

```bash
# Install dependencies
pip install torch torchvision numpy

# Run the project
py main.py
```

---

##  Sample Output

The program displays:

* local training loss for each client
* Dilithium signing time
* gossip propagation logs
* signature verification time
* round execution time

---

##  Security Aspect

This project uses **Dilithium**, a **post-quantum digital signature scheme**, to secure model updates.

This ensures:

* ✔ authenticity of updates
* ✔ integrity of transmitted model parameters
* ✔ resistance against quantum attacks

---

##  Key Concepts Used

* Federated Learning
* Gossip Protocol
* Decentralized Aggregation
* Peer-to-Peer Communication
* Digital Signatures
* Post-Quantum Cryptography
* FedAvg

---

##  Centralized vs Decentralized FL

| Feature         | Centralized FL  | This Project      |
| --------------- | --------------- | ----------------- |
| Server          | Required        | ❌ Not required    |
| Aggregation     | Server-side     | Local (each node) |
| Communication   | Client → Server | Peer-to-peer      |
| Fault Tolerance | Low             | High              |
| Scalability     | Limited         | High              |

---

##  Conclusion

This project demonstrates a **secure, scalable, and fully decentralized federated learning system** using gossip-based communication and post-quantum cryptography.

It removes reliance on a central server while maintaining model integrity and collaborative learning.

---


