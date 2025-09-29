from ecdsa import SigningKey, SECP256k1, VerifyingKey
import hashlib
import base64
import os

class KeyGenerator:
    @staticmethod
    def generate_ecc_key_pair():
        """Generate ECC key pair using secp256k1 curve"""
        private_key = SigningKey.generate(curve=SECP256k1)
        public_key = private_key.get_verifying_key()
        return private_key, public_key
    
    @staticmethod
    def keys_to_string(private_key, public_key):
        """Convert keys to string format for storage"""
        priv_str = private_key.to_string().hex()
        pub_str = public_key.to_string().hex()
        return priv_str, pub_str
    
    @staticmethod
    def string_to_keys(priv_str, pub_str):
        """Convert string back to key objects"""
        private_key = SigningKey.from_string(bytes.fromhex(priv_str), curve=SECP256k1)
        public_key = VerifyingKey.from_string(bytes.fromhex(pub_str), curve=SECP256k1)
        return private_key, public_key
    
    @staticmethod
    def generate_symmetric_key():
        """Generate symmetric key for session encryption"""
        return base64.b64encode(os.urandom(32)).decode()
    
    @staticmethod
    def encrypt_with_public_key(data, public_key_str):
        """Simulate encryption with public key"""
        if isinstance(data, dict):
            import json
            data = json.dumps(data)
        # For demo purposes, we'll use simple base64 encoding
        # In real implementation, use proper ECIES
        encrypted_data = base64.b64encode(data.encode()).decode()
        encrypted_key = public_key_str[:32]  # Simulate encrypted key
        return encrypted_data, encrypted_key
    
    @staticmethod
    def decrypt_with_private_key(encrypted_data, encrypted_key, private_key):
        """Simulate decryption with private key"""
        try:
            decrypted_data = base64.b64decode(encrypted_data).decode()
            return decrypted_data
        except Exception as e:
            raise Exception(f"Decryption failed: {str(e)}")