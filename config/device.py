import torch
class Device:
    def __init__(self):
        self.device = self.get_device()
        self.device_name = self.get_device_name()
        
    def get_device(self):
        if torch.backends.mps.is_available():
            return torch.device('mps')
        elif torch.cuda.is_available():
            return torch.device('cuda')
        else:
            return torch.device('cpu')
        
    def get_device_name(self):
        if torch.backends.mps.is_available():
            return 'mps'
        elif torch.cuda.is_available():
            return 'cuda'
        else:
            return 'cpu'
        
        
