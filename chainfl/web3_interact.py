'''
Web3-based blockchain interaction module for VeryFL
'''
import logging
from web3 import Web3
from eth_account import Account
from collections import defaultdict
import json
import torch
from util import jsonFormat

logger = logging.getLogger(__name__)

# Initialize Web3 connection
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))  # Connect to local Ganache
if not w3.is_connected():
    raise Exception("Failed to connect to Ethereum node")

# Enable account creation
Account.enable_unaudited_hdwallet_features()

class Web3Proxy:
    def __init__(self):
        self.upload_params = None
        self.accounts = []
        self.client_list = defaultdict(str)
        self.client_num = 0
        
        # Create server account
        self.server_account = Account.create()
        self.accounts.append(self.server_account)
        
        logger.info("Web3Proxy initialized with server account: %s", self.server_account.address)
    
    def get_client_num(self):
        return self.client_num
    
    def get_client_list(self):
        return self.client_list
    
    def add_account(self) -> str:
        """Create a new Ethereum account"""
        account = Account.create()
        self.accounts.append(account)
        return account.address
    
    def client_regist(self) -> str:
        """Register a new client"""
        self.client_num += 1
        if len(self.accounts) <= self.client_num:
            self.add_account()
        client_id = str(self.client_num)
        self.client_list[client_id] = self.accounts[self.client_num].address
        return client_id
    
    def upload_model(self, upload_params: dict):
        """Upload model parameters to the blockchain"""
        model_state_dict = upload_params['state_dict']
        upload_params['state_dict'] = jsonFormat.model2json(model_state_dict)
        self.upload_params = upload_params
        logger.info("Model uploaded successfully")
    
    def download_model(self, params=None):
        """Download model parameters from the blockchain"""
        if self.upload_params is None:
            raise Exception("No model uploaded")
        download_params = self.upload_params.copy()
        download_params['state_dict'] = jsonFormat.json2model(download_params['state_dict'])
        return download_params
    
    def construct_sign(self, args: dict = {}):
        """Construct watermark signature for model protection"""
        sign_config = args.get('sign_config')
        model_name = args.get('model')
        bit_length = args.get('bit_length')
        
        if model_name != "SignAlexNet":
            logger.error("Watermark Not Support for this network")
            raise Exception("Watermark Not Support for this network")
        
        watermark_args = dict()
        alexnet_channels = {
            '4': (384, 3456),
            '5': (256, 2304),
            '6': (256, 2304)
        }
        
        for layer_key in sign_config:
            flag = sign_config[layer_key]
            b = flag if isinstance(flag, str) else None
            if b is not None:
                flag = True
            watermark_args[layer_key] = {
                'flag': flag
            }

            if b is not None:
                if layer_key == "4":
                    output_channels = int(bit_length * 384 / 896)
                if layer_key == "5":
                    output_channels = int(bit_length * 256 / 896)
                if layer_key == "6":
                    output_channels = int(bit_length * 256 / 896)

                b = torch.sign(torch.rand(output_channels) - 0.5)
                M = torch.randn(alexnet_channels[layer_key][0], output_channels)

                watermark_args[layer_key]['b'] = b
                watermark_args[layer_key]['M'] = M

        return watermark_args

# Create a singleton instance
chain_proxy = Web3Proxy() 