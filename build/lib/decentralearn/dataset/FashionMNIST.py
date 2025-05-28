from torchvision import datasets, transforms
import os

def get_fashionmnist(train=True):
    """Get FashionMNIST dataset"""
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    
    dataset = datasets.FashionMNIST(
        root=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data'),
        train=train,
        download=True,
        transform=transform
    )
    
    return dataset
    