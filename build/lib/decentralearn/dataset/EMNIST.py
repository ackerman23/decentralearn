from torchvision import datasets, transforms
import os

def get_emnist(train=True):
    """Get EMNIST dataset"""
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    
    dataset = datasets.EMNIST(
        root=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data'),
        split='balanced',
        train=train,
        download=True,
        transform=transform
    )
    
    return dataset
    