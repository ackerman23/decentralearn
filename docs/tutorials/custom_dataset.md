# Custom Dataset Tutorial

This tutorial will guide you through creating and using custom datasets in DecentraLearn.

## Overview

DecentraLearn supports custom datasets through the `DatasetFactory` class. You can create your own dataset class and register it with the factory for use in federated learning experiments.

## Creating a Custom Dataset

1. **Basic Dataset Structure**:
```python
from torch.utils.data import Dataset
import torch

class CustomDataset(Dataset):
    def __init__(self, train=True, size=1000):
        # Initialize your dataset
        self.data = torch.randn(size, 3, 32, 32)  # Example: 1000 RGB images of size 32x32
        self.targets = torch.randint(0, 10, (size,))  # Example: 10 classes
        self.train = train
        self.size = size
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return self.data[idx], self.targets[idx]
```

2. **Dataset Loader Function**:
```python
def get_custom_dataset(train=True, **kwargs):
    return CustomDataset(train=train, **kwargs)
```

## Registering the Dataset

1. **Initialize the Factory**:
```python
from decentralearn.dataset import DatasetFactory

factory = DatasetFactory()
```

2. **Register the Dataset**:
```python
factory.add_custom_dataset('Custom', get_custom_dataset)
```

## Using the Custom Dataset

1. **Loading the Dataset**:
```python
# Get the dataset
dataset = factory.get_dataset('Custom', train=True, size=1000)

# Verify dataset properties
print(f"Dataset size: {len(dataset)}")
print(f"Sample shape: {dataset[0][0].shape}")
print(f"Number of classes: {len(torch.unique(dataset.targets))}")
```

2. **Splitting the Dataset**:
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

# Split dataset
dataloaders = splitter.random_split(
    dataset=dataset,
    client_list=client_list,
    batch_size=32
)
```

## Advanced Custom Dataset Example

Here's a more complex example with data loading and transformations:

```python
import os
import torch
from torch.utils.data import Dataset
from PIL import Image
from torchvision import transforms

class ImageClassificationDataset(Dataset):
    def __init__(self, root_dir, train=True, transform=None):
        self.root_dir = root_dir
        self.train = train
        self.transform = transform or self._get_default_transform()
        
        # Load image paths and labels
        self.image_paths = []
        self.labels = []
        self._load_data()
    
    def _get_default_transform(self):
        return transforms.Compose([
            transforms.Resize((32, 32)),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])
    
    def _load_data(self):
        # Example: Load data from directory structure
        # root_dir/
        #   class1/
        #     image1.jpg
        #     image2.jpg
        #   class2/
        #     image1.jpg
        #     ...
        
        for class_idx, class_name in enumerate(os.listdir(self.root_dir)):
            class_dir = os.path.join(self.root_dir, class_name)
            if os.path.isdir(class_dir):
                for img_name in os.listdir(class_dir):
                    if img_name.endswith(('.jpg', '.png')):
                        self.image_paths.append(os.path.join(class_dir, img_name))
                        self.labels.append(class_idx)
    
    def __len__(self):
        return len(self.image_paths)
    
    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        image = Image.open(img_path).convert('RGB')
        label = self.labels[idx]
        
        if self.transform:
            image = self.transform(image)
        
        return image, label

def get_image_dataset(train=True, **kwargs):
    return ImageClassificationDataset(
        root_dir='path/to/your/data',
        train=train,
        **kwargs
    )
```

## Best Practices

1. **Data Loading**:
   - Implement efficient data loading
   - Use proper data caching
   - Handle memory constraints

2. **Transformations**:
   - Include appropriate data augmentations
   - Normalize data properly
   - Handle different data formats

3. **Error Handling**:
   - Validate data paths
   - Handle corrupt files
   - Provide meaningful error messages

## Common Issues and Solutions

1. **Memory Issues**:
   - Use lazy loading for large datasets
   - Implement proper data caching
   - Consider using data loaders with workers

2. **Performance Issues**:
   - Optimize data loading
   - Use appropriate batch sizes
   - Implement efficient transformations

3. **Compatibility Issues**:
   - Ensure proper data format
   - Handle different image types
   - Support various label formats

## Next Steps

1. **Data Augmentation**:
   - Learn about advanced transformations
   - Implement custom augmentations
   - Handle different data types

2. **Non-IID Distribution**:
   - Explore non-IID data splitting
   - Implement custom distribution strategies
   - Handle imbalanced datasets

3. **Advanced Features**:
   - Implement streaming datasets
   - Add support for distributed storage
   - Handle large-scale datasets

## Additional Resources

- [Dataset Management API](../api/dataset_management.md)
- [Non-IID Distribution Tutorial](non_iid_distribution.md)
- [Advanced Features Tutorial](advanced_features.md) 