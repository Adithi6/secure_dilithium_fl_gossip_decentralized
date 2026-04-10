import logging
from torch.utils.data import DataLoader, Subset
from torchvision import datasets, transforms


def make_client_loaders(
    n_clients: int,
    samples_per_client: int = 500,
    batch_size: int = 32,
    data_dir: str = "./data",
) -> tuple[list[DataLoader], DataLoader]:

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,)),
    ])

    train_dataset = datasets.MNIST(data_dir, train=True,  download=True, transform=transform)
    test_dataset  = datasets.MNIST(data_dir, train=False, download=True, transform=transform)

    logging.info(
        f"Loaded MNIST dataset | train={len(train_dataset)} samples | test={len(test_dataset)} samples"
    )

    client_loaders = []
    for i in range(n_clients):
        start = i * samples_per_client
        end   = start + samples_per_client

        indices = list(range(start, end))
        subset  = Subset(train_dataset, indices)
        loader  = DataLoader(subset, batch_size=batch_size, shuffle=True)

        logging.info(f"Client {i} assigned samples {start} to {end}")

        client_loaders.append(loader)

    test_loader = DataLoader(test_dataset, batch_size=256, shuffle=False)

    logging.info(f"Created {n_clients} client loaders | batch_size={batch_size}")

    return client_loaders, test_loader