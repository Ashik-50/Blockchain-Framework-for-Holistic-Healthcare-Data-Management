import json
from src.crypto.key_generator import KeyGenerator

class Doctor:
    def __init__(self, doctor_id, name, specialization, license_number, hospital):
        self.doctor_id = doctor_id
        self.name = name
        self.specialization = specialization
        self.license_number = license_number
        self.hospital = hospital
        self.private_key = None
        self.public_key = None
        self.generate_keys()
    
    def generate_keys(self):
        """Generate ECC key pair for doctor"""
        private_key, public_key = KeyGenerator.generate_ecc_key_pair()
        self.private_key, self.public_key = KeyGenerator.keys_to_string(private_key, public_key)
    
    def to_dict(self):
        """Convert to dictionary for storage"""
        return {
            'doctor_id': self.doctor_id,
            'name': self.name,
            'specialization': self.specialization,
            'license_number': self.license_number,
            'hospital': self.hospital,
            'public_key': self.public_key,
            'private_key': self.private_key
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Doctor object from dictionary"""
        doctor = cls(
            data['doctor_id'],
            data['name'],
            data['specialization'],
            data['license_number'],
            data['hospital']
        )
        doctor.public_key = data['public_key']
        doctor.private_key = data['private_key']
        return doctor