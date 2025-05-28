import torch
from torch.utils.data import Dataset
from torchvision import transforms
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from decentralearn.dataset.DatasetFactory import DatasetFactory

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Example custom dataset
class CustomDataset(Dataset):
    def __init__(self, train=True, size=1000):
        self.data = torch.randn(size, 3, 32, 32)
        self.targets = torch.randint(0, 10, (size,))
        self.transform = transforms.Compose([
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return self.transform(self.data[idx]), self.targets[idx]

def get_custom_dataset(train=True, **kwargs):
    return CustomDataset(train=train, **kwargs)

def test_custom_dataset():
    # Initialize dataset factory
    factory = DatasetFactory()
    
    # Test built-in datasets
    logger.info("Testing built-in datasets...")
    for dataset_name in ['FashionMNIST', 'CIFAR10', 'CIFAR100', 'EMNIST']:
        try:
            dataset = factory.get_dataset(dataset_name, train=True)
            logger.info(f"Successfully loaded {dataset_name}")
        except Exception as e:
            logger.error(f"Failed to load {dataset_name}: {e}")
    
    # Add custom dataset
    logger.info("\nAdding custom dataset...")
    factory.add_custom_dataset('Custom', get_custom_dataset)
    
    # Test custom dataset
    try:
        dataset = factory.get_dataset('Custom', train=True, size=100)
        logger.info("Successfully loaded custom dataset")
        logger.info(f"Dataset size: {len(dataset)}")
    except Exception as e:
        logger.error(f"Failed to load custom dataset: {e}")
    
    # List available datasets
    logger.info("\nAvailable datasets:")
    for name, type_ in factory.list_available_datasets().items():
        logger.info(f"- {name} ({type_})")

if __name__ == "__main__":
    test_custom_dataset() 