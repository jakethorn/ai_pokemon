import torch
from tqdm import tqdm

from datasets.image_type_dataset import ImageTypeDataset
from models.type_classifier import TypeClassifier
from torch.nn import CrossEntropyLoss
from torch.optim import SGD
from torch.utils.data import random_split


def main() -> None:
    model = TypeClassifier()
    dataset = ImageTypeDataset()
    train_loader, test_loader = random_split(dataset, (0.9, 0.1))
    loss_function = CrossEntropyLoss()
    optimizer = SGD(model.parameters(), lr=0.001, momentum=0.9)

    for epoch in range(200):
        train_accuracy = train(model, train_loader, loss_function, optimizer)
        test_accuracy = test(model, test_loader)
        print(f"Epoch {epoch} - Train: {train_accuracy*100:.2f}%    Test: {test_accuracy*100:.2f}%")


def train(model, data_loader, loss_function, optimizer):
    model.train()

    num_total, num_correct = 0.0, 0.0
    for image, label in tqdm(data_loader):
        prediction = model(image)
        loss = loss_function(prediction, label)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        num_total += 1.0
        if is_correct(prediction, label):
            num_correct += 1.0

    return num_correct / num_total


def test(model, data_loader):
    model.eval()

    num_total, num_correct = 0.0, 0.0
    with torch.no_grad():
        for image, label in tqdm(data_loader):
            prediction = model(image)

            num_total += 1.0
            if is_correct(prediction, label):
                num_correct += 1.0

    return num_correct / num_total


def is_correct(prediction: torch.Tensor, label: torch.Tensor) -> bool:
    num_types = label.sum(dtype=torch.int).item()
    prediction_indices = prediction.topk(num_types).indices.sort().values
    label_indices = label.topk(num_types).indices.sort().values
    return prediction_indices.eq(label_indices).all().item()


if __name__ == "__main__":
    main()
