from torchvision import datasets, transforms
import os

def get_cifar100(train=True):
    """Get CIFAR100 dataset"""
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5071, 0.4867, 0.4408), (0.2675, 0.2565, 0.2761))
    ])
    
    dataset = datasets.CIFAR100(
        root=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data'),
        train=train,
        download=True,
        transform=transform
    )
    
    return dataset
    