import logging
from collections import defaultdict

from torch.utils.data import DataLoader, Subset
from torchvision import datasets, transforms


def split_non_iid(dataset, n_clients: int, samples_per_client: int) -> list[list[int]]:
    """
    Create a simple non-IID split for MNIST.

    Strategy:
    - Group dataset indices by label
    - Assign a small subset of labels to each client
    - Each client receives data mostly from its assigned labels

    Example for 4 clients:
    client 0 -> labels [0, 1, 2]
    client 1 -> labels [2, 3, 4]
    client 2 -> labels [5, 6, 7]
    client 3 -> labels [7, 8, 9]

    Overlap is intentional so distribution is non-IID but not too extreme.
    """
    targets = dataset.targets.tolist()

    label_to_indices = defaultdict(list)
    for idx, label in enumerate(targets):
        label_to_indices[label].append(idx)

    # Label assignment per client
    if n_clients == 4:
        client_labels = [
            [0, 1, 2],
            [2, 3, 4],
            [5, 6, 7],
            [7, 8, 9],
        ]
    else:
        # Generic fallback:
        # distribute labels in blocks with slight overlap
        client_labels = []
        labels_per_client = 3
        for i in range(n_clients):
            start_label = (i * 2) % 10
            labels = [(start_label + j) % 10 for j in range(labels_per_client)]
            client_labels.append(labels)

    client_indices = []

    for i in range(n_clients):
        chosen_labels = client_labels[i]
        per_label = samples_per_client // len(chosen_labels)

        indices = []
        for label in chosen_labels:
            selected = label_to_indices[label][:per_label]
            indices.extend(selected)

            # Remove used indices so the same sample is not reused across clients
            label_to_indices[label] = label_to_indices[label][per_label:]

        # If division leaves a remainder, fill from the last chosen label
        while len(indices) < samples_per_client:
            last_label = chosen_labels[-1]
            if not label_to_indices[last_label]:
                break
            indices.append(label_to_indices[last_label].pop(0))

        client_indices.append(indices)

        logging.info(
            f"Client {i} assigned labels {chosen_labels} | total_samples={len(indices)}"
        )

    return client_indices


def make_client_loaders(
    n_clients: int,
    samples_per_client: int = 500,
    batch_size: int = 32,
    data_dir: str = "./data",
) -> tuple[list[DataLoader], DataLoader]:
    """
    Returns:
        client_loaders : list of non-IID client DataLoaders
        test_loader    : DataLoader over full MNIST test set
    """
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,)),
    ])

    train_dataset = datasets.MNIST(
        data_dir, train=True, download=True, transform=transform
    )
    test_dataset = datasets.MNIST(
        data_dir, train=False, download=True, transform=transform
    )

    logging.info(
        f"Loaded MNIST dataset | train={len(train_dataset)} samples | test={len(test_dataset)} samples"
    )

    client_split_indices = split_non_iid(
        train_dataset,
        n_clients=n_clients,
        samples_per_client=samples_per_client,
    )

    client_loaders = []
    for i in range(n_clients):
        subset = Subset(train_dataset, client_split_indices[i])
        loader = DataLoader(subset, batch_size=batch_size, shuffle=True)
        client_loaders.append(loader)

    test_loader = DataLoader(test_dataset, batch_size=256, shuffle=False)

    logging.info(
        f"Created {n_clients} non-IID client loaders | batch_size={batch_size}"
    )

    return client_loaders, test_loader