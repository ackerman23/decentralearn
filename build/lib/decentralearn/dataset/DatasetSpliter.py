import logging
import numpy as np
import random
from torch.utils.data import Dataset, DataLoader, Subset
from torch.utils.data.sampler import SubsetRandomSampler
from collections import defaultdict

logger = logging.getLogger(__name__)


class DatasetSpliter:
    '''
    Receive a dataset object. Provided with some method to random divided the dataset.
    
    For Federated Learning: 
    1. Random Split
    2. Non-IID Split with params of dirichlet distribution. 
    '''
    def __init__(self) -> None:
        return
    
    def _sample_random(self, dataset: Dataset, client_list: dict) -> defaultdict(list):
        """Random split dataset indices among clients"""
        indices = list(range(len(dataset)))
        random.shuffle(indices)
        
        # Calculate samples per client
        num_clients = len(client_list)
        samples_per_client = len(indices) // num_clients
        remainder = len(indices) % num_clients
        
        # Distribute indices to clients
        per_client_list = defaultdict(list)
        start_idx = 0
        for client_id in client_list.keys():
            # Add one extra sample if there are remainders left
            extra = 1 if remainder > 0 else 0
            end_idx = start_idx + samples_per_client + extra
            
            per_client_list[client_id] = indices[start_idx:end_idx]
            start_idx = end_idx
            remainder -= 1 if remainder > 0 else 0
            
        return per_client_list
    
    def _sample_dirichlet(self, dataset: Dataset, client_list: dict, alpha: int) -> defaultdict(list):
        """Split dataset indices using Dirichlet distribution"""
        client_num = len(client_list.keys())
        per_class_list = defaultdict(list)
        
        # Get each class index
        for ind, (_, label) in enumerate(dataset):
            per_class_list[int(label)].append(ind)
        
        # Split the dataset using Dirichlet distribution
        class_num = len(per_class_list.keys())
        per_client_list = defaultdict(list)
        
        for n in range(class_num):
            random.shuffle(per_class_list[n])
            class_size = len(per_class_list[n])
            
            # Sample probabilities from Dirichlet distribution
            sampled_probabilities = class_size * np.random.dirichlet(np.array(client_num * [alpha]))
            
            # Distribute samples according to probabilities
            current_idx = 0
            for client_idx, (client_id, _) in enumerate(client_list.items()):
                no_imgs = int(round(sampled_probabilities[client_idx]))
                if no_imgs > 0:  # Only add if client gets samples
                    end_idx = min(current_idx + no_imgs, class_size)
                    per_client_list[client_id].extend(per_class_list[n][current_idx:end_idx])
                    current_idx = end_idx
                
                if current_idx >= class_size:
                    break
        
        return per_client_list
    
    def random_split(self, dataset: Dataset, client_list: dict, batch_size: int = 32) -> dict[DataLoader]:
        """Split dataset randomly among clients"""
        # Get indices for each client
        split_list = self._sample_random(dataset, client_list)
        
        # Create dataloaders
        dataloaders = {}
        for client_id in client_list.keys():
            if split_list[client_id]:  # Only create dataloader if client has samples
                subset = Subset(dataset, split_list[client_id])
                dataloaders[client_id] = DataLoader(
                    dataset=subset,
                    batch_size=min(batch_size, len(split_list[client_id])),
                    shuffle=True,
                    num_workers=0  # Avoid multiprocessing issues in testing
                )
        
        return dataloaders
    
    def dirichlet_split(self, dataset: Dataset, client_list: dict, batch_size: int = 32, alpha: int = 1) -> dict[DataLoader]:
        """Split dataset using Dirichlet distribution"""
        # Get indices for each client
        split_list = self._sample_dirichlet(dataset, client_list, alpha)
        
        # Create dataloaders
        dataloaders = {}
        for client_id in client_list.keys():
            if split_list[client_id]:  # Only create dataloader if client has samples
                subset = Subset(dataset, split_list[client_id])
                dataloaders[client_id] = DataLoader(
                    dataset=subset,
                    batch_size=min(batch_size, len(split_list[client_id])),
                    shuffle=True,
                    num_workers=0  # Avoid multiprocessing issues in testing
                )
        
        return dataloaders
    
    

    