from torchvision import datasets, transforms
import os

def get_cifar10(train=True):
    """Get CIFAR10 dataset"""
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))
    ])
    
    dataset = datasets.CIFAR10(
        root=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data'),
        train=train,
        download=True,
        transform=transform
    )
    
    return dataset
    