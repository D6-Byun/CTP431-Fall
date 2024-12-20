import torch
import torch.nn as nn
from torchvision import models

class VGG19_Pretrained(nn.Module):
    def __init__(self, num_class = 11):
        super(VGG19_Pretrained, self).__init__()

        pretrained_vgg = models.vgg19(pretrained=True)

        self.features = pretrained_vgg.features

        self.classifier = nn.Sequential(
            nn.Linear(512 * 7 * 7, 4096),
            nn.ReLU(),
            nn.Dropout(),
            nn.Linear(4096, 4096),
            nn.ReLU(),
            nn.Dropout(),
            nn.Linear(4096, num_class)
        )

    def forward(self, x):
        x = self.features(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x