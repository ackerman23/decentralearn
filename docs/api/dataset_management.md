# Dataset Management API

The Dataset Management API provides tools for working with datasets in DecentraLearn, including built-in datasets, custom datasets, and data splitting utilities.

## Table of Contents

1. [DatasetFactory](#datasetfactory)
2. [Built-in Datasets](#built-in-datasets)
3. [Custom Datasets](#custom-datasets)
4. [DatasetSpliter](#datasetspliter)
5. [Examples](#examples)

## DatasetFactory

The `DatasetFactory` class manages dataset creation and loading.

### Methods

```python
class DatasetFactory:
    def __init__(self)
    def add_custom_dataset(self, dataset_name: str, dataset_loader: Callable) -> None
    def get_dataset(self, dataset: str, train: bool = True, **kwargs) -> Dataset
    def list_available_datasets(self) -> Dict[str, str]
```

### Parameters

- `dataset_name`: Name of the custom dataset
- `dataset_loader`: Function that returns a PyTorch Dataset
- `dataset`: Name of the dataset to load
- `train`: Whether to load training or test data
- `**kwargs`: Additional arguments for dataset creation

### Example

```python
from decentralearn.dataset import DatasetFactory

# Initialize factory
factory = DatasetFactory()

# Get built-in dataset
dataset = factory.get_dataset('FashionMNIST', train=True)

# List available datasets
available = factory.list_available_datasets()
```

## Built-in Datasets

DecentraLearn provides several built-in datasets:

1. **FashionMNIST**
   - 60,000 training images
   - 10,000 test images
   - 10 classes
   - 28x28 grayscale images

2. **CIFAR10**
   - 50,000 training images
   - 10,000 test images
   - 10 classes
   - 32x32 RGB images

3. **CIFAR100**
   - 50,000 training images
   - 10,000 test images
   - 100 classes
   - 32x32 RGB images

4. **EMNIST**
   - 697,932 training images
   - 116,323 test images
   - 47 classes
   - 28x28 grayscale images

## Custom Datasets

You can create and register custom datasets:

```python
from torch.utils.data import Dataset

class MyDataset(Dataset):
    def __init__(self, train=True, size=1000):
        self.data = torch.randn(size, 3, 32, 32)
        self.targets = torch.randint(0, 10, (size,))
        self.train = train
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return self.data[idx], self.targets[idx]

def get_my_dataset(train=True, **kwargs):
    return MyDataset(train=train, **kwargs)

# Register custom dataset
factory.add_custom_dataset('MyDataset', get_my_dataset)
```

## DatasetSpliter

The `DatasetSpliter` class handles data distribution among clients.

### Methods

```python
class DatasetSpliter:
    def random_split(self, dataset: Dataset, client_list: dict, batch_size: int = 32) -> dict[DataLoader]
    def dirichlet_split(self, dataset: Dataset, client_list: dict, batch_size: int = 32, alpha: int = 1) -> dict[DataLoader]
```

### Parameters

- `dataset`: PyTorch Dataset to split
- `client_list`: Dictionary of client IDs and addresses
- `batch_size`: Size of data batches
- `alpha`: Dirichlet distribution parameter for non-IID splitting

### Example

```python
from decentralearn.dataset import DatasetSpliter

# Initialize splitter
splitter = DatasetSpliter()

# Create client list
client_list = {
    'client1': 'addr1',
    'client2': 'addr2',
    'client3': 'addr3'
}

# Random split
dataloaders = splitter.random_split(
    dataset=dataset,
    client_list=client_list,
    batch_size=32
)

# Non-IID split
dataloaders = splitter.dirichlet_split(
    dataset=dataset,
    client_list=client_list,
    batch_size=32,
    alpha=0.5
)
```

## Examples

### Complete Workflow

```python
from decentralearn.dataset import DatasetFactory, DatasetSpliter
import torch

# Initialize components
factory = DatasetFactory()
splitter = DatasetSpliter()

# Get dataset
dataset = factory.get_dataset('FashionMNIST', train=True)

# Create client list
client_list = {
    'client1': 'addr1',
    'client2': 'addr2',
    'client3': 'addr3'
}

# Split dataset
dataloaders = splitter.random_split(
    dataset=dataset,
    client_list=client_list,
    batch_size=32
)

# Use dataloaders
for client_id, dataloader in dataloaders.items():
    for batch_idx, (data, target) in enumerate(dataloader):
        # Process batch
        print(f'Client {client_id} - Batch {batch_idx}: {data.shape}')
```

### Custom Dataset with Non-IID Split

```python
from decentralearn.dataset import DatasetFactory, DatasetSpliter
import torch

# Create custom dataset
class CustomDataset(torch.utils.data.Dataset):
    def __init__(self, train=True, size=1000):
        self.data = torch.randn(size, 3, 32, 32)
        self.targets = torch.randint(0, 10, (size,))
        self.train = train
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return self.data[idx], self.targets[idx]

def get_custom_dataset(train=True, **kwargs):
    return CustomDataset(train=train, **kwargs)

# Initialize components
factory = DatasetFactory()
splitter = DatasetSpliter()

# Register and get custom dataset
factory.add_custom_dataset('Custom', get_custom_dataset)
dataset = factory.get_dataset('Custom', train=True, size=1000)

# Create client list
client_list = {
    'client1': 'addr1',
    'client2': 'addr2',
    'client3': 'addr3'
}

# Non-IID split
dataloaders = splitter.dirichlet_split(
    dataset=dataset,
    client_list=client_list,
    batch_size=32,
    alpha=0.5
)
```

## Best Practices

1. **Dataset Creation**:
   - Implement proper `__len__` and `__getitem__` methods
   - Handle data loading efficiently
   - Include proper data transformations

2. **Data Splitting**:
   - Choose appropriate batch sizes
   - Consider memory constraints
   - Use non-IID splitting carefully

3. **Performance**:
   - Use data loading workers when possible
   - Implement proper data caching
   - Optimize data transformations

## Next Steps

- [Blockchain Client API](blockchain_client.md)
- [Model Management API](model_management.md)
- [Configuration API](configuration.md) 