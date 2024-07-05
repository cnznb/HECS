# -*- encoding = utf-8 -*-
"""
@description: training by HGNN model
@date: 2024/1/25
@File : train.py
@Software : PyCharm
"""
import os
from random import random

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

# Assuming your HGNN models is defined in a file called model.py
from model import HGNN, HGNNPLUS

# Assuming your dataset creation code is in a file called dataset.py
from dataset import get_dataset
from sklearn.metrics import precision_score, recall_score, f1_score


# Define the training function
def train_epoch(model, dataloader, optimizer, criterion, device):
    model.train()
    total_loss = 0.0

    for data in dataloader:
        hg, link, features, label = data[0], data[1], data[2], data[3]
        hg, link, features, label = hg.to(device), link.to(device), features.to(device), label.to(device)

        optimizer.zero_grad()
        output = model(features, hg, link)
        loss = criterion(output.squeeze(), label.float())
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    return total_loss / len(dataloader)


# Define the testing function
def test_epoch(model, dataloader, criterion, device):
    model.eval()
    total_loss = 0.0
    correct_predictions = 0
    all_predictions = []
    all_labels = []

    with torch.no_grad():
        for data in dataloader:
            hg, link, features, label = data[0], data[1], data[2], data[3]
            hg, link, features, label = hg.to(device), link.to(device), features.to(device), label.to(device)
            output = model(features, hg, link)
            loss = criterion(output.squeeze(), label.float())

            total_loss += loss.item()
            predictions = (output > 0.5).float()
            all_predictions.extend(predictions.cpu().numpy())
            all_labels.extend(label.view(-1).cpu().numpy())

            correct_predictions += (predictions == label).sum().item()

    accuracy = correct_predictions / len(dataloader.dataset)
    precision = precision_score(all_labels, all_predictions)
    recall = recall_score(all_labels, all_predictions)
    f1 = f1_score(all_labels, all_predictions)

    return total_loss / len(dataloader), accuracy, precision, recall, f1


# Main training and testing loop
def main(emb, md):
    # Set your hyperparameters
    in_channels = 768  # Set your input feature size   256
    h_channels = 256  # Set your hidden feature size   64
    out_channels = 16  # Set your output feature size  16
    epochs = 500  # Set the number of training epochs

    # Load the dataset
    # codebert codegpt codet5 codet5plus codetrans cotext graphcodebert plbart
    emb_type = emb  # Set your embedding type
    model_name = md
    # 'GraphSAGE_HGNN', 'GCN_HGNNPLUS', 'GraphSAGE_HGNNPLUS'
    if md == "HGNN":
        model = HGNN(in_channels, h_channels, out_channels)
    elif md == "HGNNPLUS":
        model = HGNNPLUS(in_channels, h_channels, out_channels)

    if os.path.exists("model/_" + model_name + "_" + emb_type + "-" + str(h_channels) + "-" + str(out_channels) + ".pth"):
        state_dict = torch.load("model/_" + model_name + "_" + emb_type + "-" + str(h_channels) + "-" + str(out_channels) + ".pth")
        model.load_state_dict(state_dict)
    # Assuming you have already defined your loss function, optimizer, and other parameters
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    device = torch.device("cpu")
    train_set, val_set, test_set = get_dataset(emb_type)
    # Convert datasets to DataLoader
    train_loader = DataLoader(train_set, batch_size=None, shuffle=True)
    val_loader = DataLoader(val_set, batch_size=None, shuffle=False)
    test_loader = DataLoader(test_set, batch_size=None, shuffle=False)

    model.to(device)

    best_val_loss = float('inf')
    best_val_accuracy = 0
    best_val_precision = 0
    best_val_recall = 0
    best_val_f1 = 0
    best_state = None
    best_epoch = -1
    patience = 10
    counter = 0
    result_file_path = "result1/_" + model_name + "_" + emb_type + "-" + str(h_channels) + "-" + str(out_channels) + ".txt"
    # Training loop
    for epoch in range(epochs):
        train_loss = train_epoch(model, train_loader, optimizer, criterion, device)
        val_loss, val_accuracy, val_precision, val_recall, val_f1 = test_epoch(model, val_loader, criterion, device)
        with open(result_file_path, "a") as file:
            file.write(
                f"Epoch {epoch + 1}/{epochs} - Train Loss: {train_loss:.4f} - Val Loss: {val_loss:.4f} - Val Accuracy: {val_accuracy:.4f} - Val Precision: {val_precision:.4f} - Val Recall: {val_recall:.4f} - Val F1: {val_f1:.4f}\n")

        print(
            f"Epoch {epoch + 1}/{epochs} - Train Loss: {train_loss:.4f} - Val Loss: {val_loss:.4f} - Val Accuracy: {val_accuracy:.4f} - Val Precision: {val_precision:.4f} - Val Recall: {val_recall:.4f} - Val F1: {val_f1:.4f}")

        if val_f1 > best_val_f1:
            best_val_loss = val_loss
            best_val_accuracy = val_accuracy
            best_val_precision = val_precision
            best_val_recall = val_recall
            best_val_f1 = val_f1
            best_state = model.state_dict()
            best_epoch = epoch + 1
            torch.save(model.state_dict(), "model/_" + model_name + "_" + emb_type + "-" + str(h_channels) + "-" + str(out_channels) + ".pth")

        if epoch % 20 == 0 and epoch != 0:
            test_loss, test_accuracy, test_precision, test_recall, test_f1 = test_epoch(model, test_loader, criterion,
                                                                                        device)
            with open(result_file_path, "a") as file:
                file.write(f"Test Loss: {test_loss:.4f} - Test Accuracy: {test_accuracy:.4f} - Test Precision: {test_precision:.4f} - Test Recall: {test_recall:.4f} - Test F1: {test_f1:.4f}\n")

            print(f"Test Loss: {test_loss:.4f} - Test Accuracy: {test_accuracy:.4f} - Test Precision: {test_precision:.4f} - Test Recall: {test_recall:.4f} - Test F1: {test_f1:.4f}")


    print(
        f"Best Epoch: {best_epoch} - Best Val Precision: {best_val_precision:.4f} - Best val Recall: {best_val_recall:.4f} - best val F1: {best_val_f1:.4f}")

    # Test the models
    model.load_state_dict(best_state)
    test_loss, test_accuracy, test_precision, test_recall, test_f1 = test_epoch(model, test_loader, criterion, device)
    print(
        f"Test Loss: {test_loss:.4f} - Test Accur acy: {test_accuracy:.4f} - Test Precision: {test_precision:.4f} - Test Recall: {test_recall:.4f} - Test F1: {test_f1:.4f}")

    with open(result_file_path, "a") as file:
        file.write(
            f"Best Epoch: {best_epoch} - Best Val Precision: {best_val_precision:.4f} - Best val Recall: {best_val_recall:.4f} - best val F1: {best_val_f1:.4f}\n")

        file.write(
            f"Test Loss: {test_loss:.4f} - Test Accuracy: {test_accuracy:.4f} - Test Precision: {test_precision:.4f} - Test Recall: {test_recall:.4f} - Test F1: {test_f1:.4f}\n")


if __name__ == "__main__":
    embs = ['codebert', 'codegpt', 'codet5', 'cotext', 'graphcodebert', 'plbart']
    model_names = ['HGNN', 'HGNNPLUS']
    for emb in embs:
        for md in model_names:
            main(emb, md)
