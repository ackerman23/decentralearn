from torchvision import datasets
from torch.utils.data import Dataset
import logging
from .FashionMNIST import get_fashionmnist
from .CIFAR10      import get_cifar10
from .CIFAR100     import get_cifar100
from .EMNIST       import get_emnist
from typing import Dict, Callable, Optional

logger = logging.getLogger(__name__)

class DatasetFactory:
    '''
    Server as an factory for user to get benchmark dataset.
    This class provide a unified interface to access the basic datasets.
    
    '''
    def __init__(self):
        self._custom_datasets: Dict[str, Callable] = {}
        self._builtin_datasets = {
            'FashionMNIST': get_fashionmnist,
            'CIFAR10': get_cifar10,
            'CIFAR100': get_cifar100,
            'EMNIST': get_emnist
        }

    def add_custom_dataset(self, dataset_name: str, dataset_loader: Callable) -> None:
        """
        Add support for a custom dataset.
        
        Args:
            dataset_name (str): Name of the dataset
            dataset_loader (Callable): Function that returns a PyTorch Dataset
        """
        if dataset_name in self._builtin_datasets or dataset_name in self._custom_datasets:
            logger.warning(f"Dataset {dataset_name} already exists")
            return
        
        self._custom_datasets[dataset_name] = dataset_loader
        logger.info(f"Added custom dataset: {dataset_name}")

    def get_dataset(self, dataset: str, train: bool = True, **kwargs) -> Dataset:
        """
        Get a dataset by name.
        
        Args:
            dataset (str): Name of the dataset
            train (bool): Whether to get training or test set
            **kwargs: Additional arguments to pass to the dataset loader
            
        Returns:
            Dataset: PyTorch Dataset object
            
        Raises:
            Exception: If dataset is not found
        """
        # Try built-in datasets first
        if dataset in self._builtin_datasets:
            return self._builtin_datasets[dataset](train=train, **kwargs)
        
        # Try custom datasets
        if dataset in self._custom_datasets:
            return self._custom_datasets[dataset](train=train, **kwargs)
        
        # Dataset not found
        logger.error(f"DatasetFactory received an unknown dataset: {dataset}")
        raise Exception(f"Unrecognized Dataset: {dataset}")

    def list_available_datasets(self) -> Dict[str, str]:
        """
        List all available datasets.
        
        Returns:
            Dict[str, str]: Dictionary mapping dataset names to their types (builtin/custom)
        """
        datasets = {}
        for name in self._builtin_datasets:
            datasets[name] = "builtin"
        for name in self._custom_datasets:
            datasets[name] = "custom"
        return datasets