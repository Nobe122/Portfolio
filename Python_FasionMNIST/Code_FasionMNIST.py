import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
import torchvision.datasets as datasets

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import seaborn as sns

# ----------------------------
# 1. データ前処理
# ----------------------------
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

train_dataset = datasets.FashionMNIST(
    root=r"C:\Users\Ktoma\.vscode\VScode_saves\2025_2nd_3-1-class\ASI3_data",
    train=True,
    download=True,
    transform=transform
)

test_dataset = datasets.FashionMNIST(
    root=r"C:\Users\Ktoma\.vscode\VScode_saves\2025_2nd_3-1-class\ASI3_data",
    train=False,
    download=True,
    transform=transform
)

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader  = DataLoader(test_dataset, batch_size=64, shuffle=False)

class_names = train_dataset.classes

# ----------------------------
# 2. CNNモデル定義
# ----------------------------
class FashionCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)

        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        x = x.view(x.size(0), -1)
        x = torch.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = FashionCNN().to(device)

# ----------------------------
# 3. 損失関数・最適化・スケジューラ
# ----------------------------
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-3)

# 学習率スケジューラ
scheduler = optim.lr_scheduler.StepLR(
    optimizer,
    step_size=5,   # 5エポックごと
    gamma=0.5      # 学習率を半分に
)

# ----------------------------
# 4. 学習ループ
# ----------------------------
num_epochs = 15
train_losses = []
test_accuracies = []

for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0

    for imgs, labels in train_loader:
        imgs, labels = imgs.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(imgs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    scheduler.step()

    epoch_loss = running_loss / len(train_loader)
    train_losses.append(epoch_loss)

    # ---------- テスト精度 ----------
    model.eval()
    correct, total = 0, 0
    with torch.no_grad():
        for imgs, labels in test_loader:
            imgs, labels = imgs.to(device), labels.to(device)
            outputs = model(imgs)
            _, preds = torch.max(outputs, 1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)

    test_acc = correct / total
    test_accuracies.append(test_acc)

    print(f"Epoch [{epoch+1}/{num_epochs}] "
          f"Loss: {epoch_loss:.4f} "
          f"Acc: {test_acc*100:.2f}% "
          f"LR: {optimizer.param_groups[0]['lr']:.6f}")


# ----------------------------
# 5. 評価（混同行列・クラス別精度）
# ----------------------------
model.eval()
all_preds = []
all_labels = []
misclassified = []

with torch.no_grad():
    for imgs, labels in test_loader:
        imgs, labels = imgs.to(device), labels.to(device)
        outputs = model(imgs)
        _, preds = torch.max(outputs, 1)

        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.numpy())
        
        for i in range(len(labels)):
            if preds[i] != labels[i]:
                misclassified.append((
                    imgs[i].cpu(),
                    labels[i].item(),
                    preds[i].item()
                ))

# 混同行列
cm = confusion_matrix(all_labels, all_preds)

# クラスごとの精度
class_accuracy = cm.diagonal() / cm.sum(axis=1)

print("\nClass-wise Accuracy:")
for i, acc in enumerate(class_accuracy):
    print(f"{class_names[i]:>10s}: {acc*100:.2f}%")

# 全体精度
overall_accuracy = np.trace(cm) / np.sum(cm)
print(f"\nOverall Accuracy: {overall_accuracy*100:.2f}%")

# ----------------------------
# 6. 混同行列の可視化
# ----------------------------
plt.figure(figsize=(8, 6))
sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=class_names,
    yticklabels=class_names
)
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.title("Confusion Matrix (FashionMNIST)")
plt.tight_layout()
plt.show()

# ----------------------------
# 7. 学習曲線の可視化コード
# ----------------------------
epochs = range(1, num_epochs + 1)

plt.figure(figsize=(12, 5))

# Loss
plt.subplot(1, 2, 1)
plt.plot(epochs, train_losses, marker='o')
plt.xlabel("Epoch")
plt.ylabel("Training Loss")
plt.title("Training Loss Curve")
plt.grid(True)

# Accuracy
plt.subplot(1, 2, 2)
plt.plot(epochs, test_accuracies, marker='o')
plt.xlabel("Epoch")
plt.ylabel("Test Accuracy")
plt.title("Test Accuracy Curve")
plt.grid(True)

plt.tight_layout()
plt.show()

# ----------------------------
# 8. 誤分類画像の可視化
# ----------------------------
plt.figure(figsize=(12, 6))

for i in range(10): # e.g. 10 pictures
    img, true_label, pred_label = misclassified[i]

    plt.subplot(2, 5, i + 1)
    plt.imshow(img.squeeze(), cmap="gray")
    plt.title(f"T:{class_names[true_label]}\nP:{class_names[pred_label]}")
    plt.axis("off")

plt.suptitle("Misclassified Examples")
plt.tight_layout()
plt.show()
