import os

class Config:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    
    # File paths
    PATIENTS_FILE = os.path.join(DATA_DIR, "patients.json")
    DOCTORS_FILE = os.path.join(DATA_DIR, "doctors.json")
    BLOCKCHAIN_FILE = os.path.join(DATA_DIR, "blockchain_data.json")
    
    # ECC Configuration
    ECC_CURVE = "secp256r1"
    
    # Blockchain Configuration
    DIFFICULTY = 4
    MINING_REWARD = 10
    
    # IPFS Simulation
    IPFS_STORAGE = os.path.join(DATA_DIR, "ipfs_storage")