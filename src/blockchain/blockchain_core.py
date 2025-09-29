import json
import hashlib
import time
from datetime import datetime
from src.utils.config import Config

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        """Calculate SHA-256 hash of the block"""
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty):
        """Mine block with given difficulty"""
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
    
    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = Config.DIFFICULTY
        self.pending_transactions = []
    
    def create_genesis_block(self):
        """Create the first block in the chain"""
        return Block(0, datetime.now().isoformat(), "Genesis Block", "0")
    
    def get_latest_block(self):
        """Get the most recent block"""
        return self.chain[-1]
    
    def add_block(self, data):
        """Add a new block to the chain"""
        latest_block = self.get_latest_block()
        new_block = Block(
            len(self.chain),
            datetime.now().isoformat(),
            data,
            latest_block.hash
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        return new_block
    
    def is_chain_valid(self):
        """Validate the entire blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            # Check if current block hash is valid
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Check if previous hash matches
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True
    
    def add_emr_transaction(self, patient_id, doctor_id, ipfs_hash, encrypted_key, signature):
        """Add EMR transaction to blockchain"""
        transaction = {
            "type": "EMR_CREATION",
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "ipfs_hash": ipfs_hash,
            "encrypted_session_key": encrypted_key,
            "signature": signature,
            "timestamp": datetime.now().isoformat()
        }
        
        # Add to pending transactions and create block
        self.pending_transactions.append(transaction)
        new_block = self.add_block(self.pending_transactions)
        self.pending_transactions = []  # Clear pending transactions
        return new_block
    
    def get_emr_transactions(self, patient_id=None, doctor_id=None):
        """Get EMR transactions with optional filtering"""
        all_transactions = []
        for block in self.chain[1:]:  # Skip genesis block
            if isinstance(block.data, list):
                for transaction in block.data:
                    if transaction.get("type") == "EMR_CREATION":
                        if patient_id and transaction.get("patient_id") != patient_id:
                            continue
                        if doctor_id and transaction.get("doctor_id") != doctor_id:
                            continue
                        all_transactions.append(transaction)
        return all_transactions
    
    def to_dict(self):
        """Convert blockchain to dictionary for storage"""
        return {
            "chain": [block.to_dict() for block in self.chain],
            "difficulty": self.difficulty,
            "pending_transactions": self.pending_transactions
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Blockchain from dictionary"""
        blockchain = cls()
        blockchain.chain = []
        for block_data in data["chain"]:
            block = Block(
                block_data["index"],
                block_data["timestamp"],
                block_data["data"],
                block_data["previous_hash"]
            )
            block.nonce = block_data["nonce"]
            block.hash = block_data["hash"]
            blockchain.chain.append(block)
        blockchain.difficulty = data["difficulty"]
        blockchain.pending_transactions = data["pending_transactions"]
        return blockchain