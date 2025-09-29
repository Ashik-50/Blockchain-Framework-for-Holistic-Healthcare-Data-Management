from ecdsa import SigningKey, SECP256k1, VerifyingKey
import hashlib
import json
from .key_generator import KeyGenerator

class ECCManager:
    def __init__(self):
        self.curve = SECP256k1
    
    def sign_data(self, data, private_key):
        """Sign data using ECDSA"""
        if isinstance(data, dict):
            data = json.dumps(data, sort_keys=True)
        signature = private_key.sign(data.encode())
        return signature.hex()
    
    def verify_signature(self, data, signature, public_key):
        """Verify ECDSA signature"""
        if isinstance(data, dict):
            data = json.dumps(data, sort_keys=True)
        try:
            public_key.verify(bytes.fromhex(signature), data.encode())
            return True
        except:
            return False
    
    def hash_data(self, data):
        """Create SHA-256 hash of data"""
        if isinstance(data, dict):
            data = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()
    
    def encrypt_emr(self, emr_data, patient_public_key_str):
        """Encrypt EMR data using hybrid encryption"""
        emr_json = json.dumps(emr_data)
        encrypted_data, encrypted_key = KeyGenerator.encrypt_with_public_key(
            emr_json, patient_public_key_str
        )
        return encrypted_data, encrypted_key
    
    def decrypt_emr(self, encrypted_data, encrypted_key, doctor_private_key):
        """Decrypt EMR data"""
        return KeyGenerator.decrypt_with_private_key(
            encrypted_data, encrypted_key, doctor_private_key
        )