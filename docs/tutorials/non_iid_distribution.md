# Non-IID Data Distribution Tutorial

This tutorial explains how to work with non-IID (non-Independent and Identically Distributed) data in DecentraLearn using the Dirichlet distribution for data splitting.

## Overview

In real-world federated learning scenarios, data is often non-IID. DecentraLearn provides tools to simulate and handle non-IID data distributions using the Dirichlet distribution.

## Understanding Non-IID Data

Non-IID data can occur in several ways:
1. **Quantity Skew**: Different clients have different amounts of data
2. **Label Skew**: Different clients have different class distributions
3. **Feature Skew**: Different clients have different feature distributions
4. **Time Skew**: Data is collected at different times

## Using Dirichlet Distribution

The Dirichlet distribution is used to create non-IID data splits by controlling the concentration parameter (α):
- α → ∞: IID distribution (uniform)
- α → 0: Extreme non-IID (each client gets samples from only one class)
- 0 < α < 1: Moderate non-IID

## Basic Usage

1. **Initialize Components**:
```python
from decentralearn.dataset import DatasetFactory, DatasetSpliter

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
```

2. **Split with Different α Values**:
```python
# Mild non-IID (α = 1.0)
dataloaders_mild = splitter.dirichlet_split(
    dataset=dataset,
    client_list=client_list,
    batch_size=32,
    alpha=1.0
)

# Moderate non-IID (α = 0.5)
dataloaders_moderate = splitter.dirichlet_split(
    dataset=dataset,
    client_list=client_list,
    batch_size=32,
    alpha=0.5
)

# Extreme non-IID (α = 0.1)
dataloaders_extreme = splitter.dirichlet_split(
    dataset=dataset,
    client_list=client_list,
    batch_size=32,
    alpha=0.1
)
```

## Analyzing Distribution

You can analyze the distribution of data among clients:

```python
import numpy as np
import matplotlib.pyplot as plt

def analyze_distribution(dataloaders, num_classes=10):
    # Initialize class counts
    class_counts = {client_id: np.zeros(num_classes) for client_id in dataloaders.keys()}
    
    # Count classes for each client
    for client_id, dataloader in dataloaders.items():
        for _, targets in dataloader:
            for target in targets:
                class_counts[client_id][target] += 1
    
    # Plot distribution
    fig, axes = plt.subplots(len(dataloaders), 1, figsize=(10, 5*len(dataloaders)))
    for idx, (client_id, counts) in enumerate(class_counts.items()):
        axes[idx].bar(range(num_classes), counts)
        axes[idx].set_title(f'Client {client_id} Class Distribution')
        axes[idx].set_xlabel('Class')
        axes[idx].set_ylabel('Count')
    
    plt.tight_layout()
    plt.show()

# Analyze different distributions
print("Mild Non-IID Distribution:")
analyze_distribution(dataloaders_mild)

print("\nModerate Non-IID Distribution:")
analyze_distribution(dataloaders_moderate)

print("\nExtreme Non-IID Distribution:")
analyze_distribution(dataloaders_extreme)
```

## Custom Non-IID Distribution

You can create custom non-IID distributions by modifying the splitting logic:

```python
class CustomSplitter(DatasetSpliter):
    def custom_split(self, dataset, client_list, batch_size=32, distribution=None):
        """Custom non-IID split based on provided distribution"""
        if distribution is None:
            distribution = self._create_custom_distribution(len(client_list))
        
        # Get class indices
        per_class_list = defaultdict(list)
        for ind, (_, label) in enumerate(dataset):
            per_class_list[int(label)].append(ind)
        
        # Distribute samples according to custom distribution
        per_client_list = defaultdict(list)
        for class_idx, indices in per_class_list.items():
            # Shuffle indices
            random.shuffle(indices)
            
            # Get distribution for this class
            class_dist = distribution[class_idx]
            
            # Distribute samples
            current_idx = 0
            for client_idx, (client_id, _) in enumerate(client_list.items()):
                num_samples = int(len(indices) * class_dist[client_idx])
                if num_samples > 0:
                    end_idx = min(current_idx + num_samples, len(indices))
                    per_client_list[client_id].extend(indices[current_idx:end_idx])
                    current_idx = end_idx
        
        # Create dataloaders
        dataloaders = {}
        for client_id in client_list.keys():
            if per_client_list[client_id]:
                subset = Subset(dataset, per_client_list[client_id])
                dataloaders[client_id] = DataLoader(
                    dataset=subset,
                    batch_size=min(batch_size, len(per_client_list[client_id])),
                    shuffle=True
                )
        
        return dataloaders
    
    def _create_custom_distribution(self, num_clients):
        """Create a custom distribution matrix"""
        # Example: Create a distribution where each client specializes in certain classes
        distribution = np.zeros((10, num_clients))  # 10 classes
        for i in range(10):
            # Assign 80% of samples to one client, 20% distributed among others
            main_client = i % num_clients
            distribution[i, main_client] = 0.8
            remaining = 0.2 / (num_clients - 1)
            for j in range(num_clients):
                if j != main_client:
                    distribution[i, j] = remaining
        return distribution
```

## Best Practices

1. **Choosing α Value**:
   - Start with α = 1.0 for mild non-IID
   - Experiment with different values
   - Consider your specific use case

2. **Handling Imbalanced Data**:
   - Monitor class distributions
   - Implement appropriate sampling strategies
   - Consider data augmentation

3. **Performance Considerations**:
   - Balance between non-IID-ness and model performance
   - Monitor convergence rates
   - Adjust training parameters accordingly

## Common Issues and Solutions

1. **Convergence Issues**:
   - Try different α values
   - Adjust learning rates
   - Implement client selection strategies

2. **Memory Issues**:
   - Use appropriate batch sizes
   - Implement efficient data loading
   - Consider distributed storage

3. **Performance Issues**:
   - Optimize data distribution
   - Use appropriate hardware
   - Implement efficient algorithms

## Next Steps

1. **Advanced Techniques**:
   - Implement custom distribution strategies
   - Add support for time-based distributions
   - Handle feature-based non-IID

2. **Performance Optimization**:
   - Implement efficient algorithms
   - Add support for distributed computing
   - Optimize memory usage

3. **Research Integration**:
   - Add support for new research methods
   - Implement advanced sampling strategies
   - Support different aggregation methods

## Additional Resources

- [Dataset Management API](../api/dataset_management.md)
- [Custom Dataset Tutorial](custom_dataset.md)
- [Advanced Features Tutorial](advanced_features.md) 