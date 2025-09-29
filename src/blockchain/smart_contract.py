import json
from src.crypto.ecc_manager import ECCManager

class SmartContract:
    def __init__(self, blockchain, patient_manager, doctor_manager):
        self.blockchain = blockchain
        self.patient_manager = patient_manager
        self.doctor_manager = doctor_manager
        self.ecc_manager = ECCManager()
    
    def verify_access_permission(self, doctor_id, patient_id):
        """Verify if doctor has access to patient's records"""
        patient = self.patient_manager.get_patient(patient_id)
        if not patient:
            return False
        return patient.has_access(doctor_id)
    
    def verify_emr_signature(self, transaction_data, signature, doctor_public_key_str):
        """Verify EMR transaction signature"""
        doctor_public_key = self.doctor_manager.get_doctor_public_key(doctor_public_key_str)
        if not doctor_public_key:
            return False
        
        # Verify the signature
        return self.ecc_manager.verify_signature(transaction_data, signature, doctor_public_key)
    
    def process_emr_creation(self, patient_id, doctor_id, ipfs_hash, encrypted_key, signature):
        """Process EMR creation with smart contract logic"""
        # Verify doctor has access
        if not self.verify_access_permission(doctor_id, patient_id):
            raise Exception("Doctor does not have access to patient records")
        
        # Create transaction data for signature verification
        transaction_data = {
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "ipfs_hash": ipfs_hash,
            "encrypted_session_key": encrypted_key
        }
        
        # Get doctor's public key for verification
        doctor = self.doctor_manager.get_doctor(doctor_id)
        if not doctor:
            raise Exception("Doctor not found")
        
        # Verify signature
        if not self.verify_emr_signature(transaction_data, signature, doctor.public_key):
            raise Exception("Invalid signature")
        
        # Add to blockchain
        return self.blockchain.add_emr_transaction(
            patient_id, doctor_id, ipfs_hash, encrypted_key, signature
        )
    
    def grant_access(self, patient_id, doctor_id):
        """Grant access to doctor through smart contract"""
        patient = self.patient_manager.get_patient(patient_id)
        if patient:
            patient.grant_access(doctor_id)
            self.patient_manager.save_patients()
            return True
        return False
    
    def revoke_access(self, patient_id, doctor_id):
        """Revoke access from doctor through smart contract"""
        patient = self.patient_manager.get_patient(patient_id)
        if patient:
            patient.revoke_access(doctor_id)
            self.patient_manager.save_patients()
            return True
        return False