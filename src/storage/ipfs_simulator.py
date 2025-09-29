import os
import json
import hashlib
from src.utils.config import Config

class IPFSSimulator:
    def __init__(self):
        self.storage_dir = Config.IPFS_STORAGE
        os.makedirs(self.storage_dir, exist_ok=True)
    
    def store_data(self, data):
        """Store data and return simulated IPFS hash"""
        if isinstance(data, dict):
            data_str = json.dumps(data, sort_keys=True)
        else:
            data_str = str(data)
        
        # Generate hash as simulated CID
        cid = hashlib.sha256(data_str.encode()).hexdigest()
        
        # Store in file system (simulating IPFS)
        file_path = os.path.join(self.storage_dir, f"{cid}.json")
        with open(file_path, 'w') as f:
            json.dump({'data': data_str}, f)
        
        return cid
    
    def retrieve_data(self, cid):
        """Retrieve data using CID"""
        file_path = os.path.join(self.storage_dir, f"{cid}.json")
        try:
            with open(file_path, 'r') as f:
                stored_data = json.load(f)
            return stored_data['data']
        except FileNotFoundError:
            raise Exception(f"Data with CID {cid} not found")
    
    def delete_data(self, cid):
        """Delete data (for cleanup)"""
        file_path = os.path.join(self.storage_dir, f"{cid}.json")
        try:
            os.remove(file_path)
            return True
        except FileNotFoundError:
            return False