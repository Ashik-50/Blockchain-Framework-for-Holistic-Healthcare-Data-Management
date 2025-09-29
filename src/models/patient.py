import json
from src.crypto.key_generator import KeyGenerator

class Patient:
    def __init__(self, patient_id, name, age, gender, contact_info):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.gender = gender
        self.contact_info = contact_info
        self.authorized_doctors = []
        self.private_key = None
        self.public_key = None
        self.generate_keys()
    
    def generate_keys(self):
        """Generate ECC key pair for patient"""
        private_key, public_key = KeyGenerator.generate_ecc_key_pair()
        self.private_key, self.public_key = KeyGenerator.keys_to_string(private_key, public_key)
    
    def grant_access(self, doctor_id):
        """Grant access to a doctor"""
        if doctor_id not in self.authorized_doctors:
            self.authorized_doctors.append(doctor_id)
    
    def revoke_access(self, doctor_id):
        """Revoke access from a doctor"""
        if doctor_id in self.authorized_doctors:
            self.authorized_doctors.remove(doctor_id)
    
    def has_access(self, doctor_id):
        """Check if doctor has access"""
        return doctor_id in self.authorized_doctors
    
    def to_dict(self):
        """Convert to dictionary for storage"""
        return {
            'patient_id': self.patient_id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'contact_info': self.contact_info,
            'authorized_doctors': self.authorized_doctors,
            'public_key': self.public_key,
            'private_key': self.private_key
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Patient object from dictionary"""
        patient = cls(
            data['patient_id'],
            data['name'],
            data['age'],
            data['gender'],
            data['contact_info']
        )
        patient.authorized_doctors = data['authorized_doctors']
        patient.public_key = data['public_key']
        patient.private_key = data['private_key']
        return patient