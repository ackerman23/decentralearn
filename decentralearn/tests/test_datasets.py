import pytest
import torch
from torch.utils.data import Dataset, DataLoader
from decentralearn.dataset import DatasetFactory, DatasetSpliter
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Example custom dataset
class CustomDataset(Dataset):
    def __init__(self, train=True, size=1000):
        print(f"\nInitializing CustomDataset with size {size} (train={train})")
        self.data = torch.randn(size, 3, 32, 32)
        self.targets = torch.randint(0, 10, (size,))
        self.train = train
        self.size = size
        print(f"Created dataset with {len(self.data)} samples")
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return self.data[idx], self.targets[idx]

def get_custom_dataset(train=True, **kwargs):
    print(f"\nCreating custom dataset with train={train}, kwargs={kwargs}")
    return CustomDataset(train=train, **kwargs)

@pytest.fixture
def dataset_factory():
    print("\nSetting up dataset factory fixture...")
    factory = DatasetFactory()
    factory.add_custom_dataset('Custom', get_custom_dataset)
    print("Dataset factory initialized with custom dataset")
    return factory

@pytest.fixture
def dataset_spliter():
    print("\nSetting up dataset splitter fixture...")
    return DatasetSpliter()

def test_builtin_datasets(dataset_factory):
    """Test loading built-in datasets"""
    print("\n=== Testing Built-in Datasets ===")
    builtin_datasets = ['FashionMNIST', 'CIFAR10', 'CIFAR100', 'EMNIST']
    
    for dataset_name in builtin_datasets:
        try:
            print(f"\nTesting {dataset_name} dataset...")
            dataset = dataset_factory.get_dataset(dataset_name, train=True)
            assert dataset is not None
            print(f"Successfully loaded {dataset_name} with {len(dataset)} samples")
            
            # Test single item loading
            data, target = dataset[0]
            assert isinstance(data, torch.Tensor)
            assert isinstance(target, (torch.Tensor, int))
            print(f"Successfully loaded sample from {dataset_name}")
            
            logger.info(f"Successfully tested {dataset_name}")
        except Exception as e:
            logger.error(f"Failed to test {dataset_name}: {e}")
            raise
    print("=== Built-in Datasets Test Completed ===")

def test_custom_dataset(dataset_factory):
    """Test custom dataset functionality"""
    print("\n=== Testing Custom Dataset ===")
    # Test adding and loading custom dataset
    print("Loading custom dataset...")
    dataset = dataset_factory.get_dataset('Custom', train=True, size=100)
    assert dataset is not None
    print(f"Loaded custom dataset with {len(dataset)} samples")
    
    # Test data shape
    print("Testing data shape...")
    data, target = dataset[0]
    assert data.shape == (3, 32, 32)
    assert isinstance(target, (torch.Tensor, int))
    print("Data shape verification successful")
    
    logger.info("Successfully tested custom dataset")
    print("=== Custom Dataset Test Completed ===")

def test_dataset_listing(dataset_factory):
    """Test dataset listing functionality"""
    print("\n=== Testing Dataset Listing ===")
    available_datasets = dataset_factory.list_available_datasets()
    print(f"Available datasets: {available_datasets}")
    
    assert isinstance(available_datasets, dict)
    assert 'Custom' in available_datasets
    assert available_datasets['Custom'] == 'custom'
    assert any(ds for ds, type_ in available_datasets.items() if type_ == 'builtin')
    
    logger.info("Successfully tested dataset listing")
    print("=== Dataset Listing Test Completed ===")

def test_random_split(dataset_factory, dataset_spliter):
    """Test random splitting of datasets"""
    print("\n=== Testing Random Dataset Split ===")
    # Create a small dataset
    print("Creating test dataset...")
    dataset = dataset_factory.get_dataset('Custom', train=True, size=100)
    
    # Create mock client list
    client_list = {
        'client1': 'addr1',
        'client2': 'addr2',
        'client3': 'addr3'
    }
    print(f"Splitting dataset among {len(client_list)} clients...")
    
    # Test random split
    dataloaders = dataset_spliter.random_split(
        dataset=dataset,
        client_list=client_list,
        batch_size=32
    )
    
    assert len(dataloaders) == len(client_list)
    print("Verifying dataloaders for each client...")
    for client_id, dataloader in dataloaders.items():
        assert isinstance(dataloader, DataLoader)
        # Test loading a batch
        batch_data, batch_targets = next(iter(dataloader))
        assert isinstance(batch_data, torch.Tensor)
        assert isinstance(batch_targets, torch.Tensor)
        print(f"Successfully verified dataloader for {client_id}")
    
    logger.info("Successfully tested random split")
    print("=== Random Split Test Completed ===")

def test_dirichlet_split(dataset_factory, dataset_spliter):
    """Test non-IID splitting using Dirichlet distribution"""
    print("\n=== Testing Dirichlet Dataset Split ===")
    # Create a small dataset
    print("Creating test dataset...")
    dataset = dataset_factory.get_dataset('Custom', train=True, size=100)
    
    # Create mock client list
    client_list = {
        'client1': 'addr1',
        'client2': 'addr2',
        'client3': 'addr3'
    }
    print(f"Splitting dataset among {len(client_list)} clients using Dirichlet distribution...")
    
    # Test Dirichlet split
    dataloaders = dataset_spliter.dirichlet_split(
        dataset=dataset,
        client_list=client_list,
        batch_size=32,
        alpha=0.5  # More non-IID
    )
    
    assert len(dataloaders) == len(client_list)
    print("Verifying dataloaders for each client...")
    for client_id, dataloader in dataloaders.items():
        assert isinstance(dataloader, DataLoader)
        # Test loading a batch
        try:
            batch_data, batch_targets = next(iter(dataloader))
            assert isinstance(batch_data, torch.Tensor)
            assert isinstance(batch_targets, torch.Tensor)
            print(f"Successfully verified dataloader for {client_id}")
        except StopIteration:
            # Some clients might get no data due to Dirichlet distribution
            logger.warning(f"Client {client_id} received no data in non-IID split")
            print(f"Warning: Client {client_id} received no data")
    
    logger.info("Successfully tested Dirichlet split")
    print("=== Dirichlet Split Test Completed ===")

if __name__ == "__main__":
    print("\n=== Starting Dataset Tests ===")
    pytest.main([__file__, "-v"])
    print("\n=== Dataset Tests Completed ===") 