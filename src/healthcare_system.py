import json
import os
from datetime import datetime

# Use relative imports for Python 3.13 compatibility
try:
    from .utils.config import Config
    from .models.patient import Patient
    from .models.doctor import Doctor
    from .models.medical_record import MedicalRecord
    from .crypto.ecc_manager import ECCManager
    from .crypto.key_generator import KeyGenerator
    from .blockchain.blockchain_core import Blockchain
    from .blockchain.smart_contract import SmartContract
    from .storage.ipfs_simulator import IPFSSimulator
except ImportError:
    # Fallback for direct execution
    from utils.config import Config
    from models.patient import Patient
    from models.doctor import Doctor
    from models.medical_record import MedicalRecord
    from crypto.ecc_manager import ECCManager
    from crypto.key_generator import KeyGenerator
    from blockchain.blockchain_core import Blockchain
    from blockchain.smart_contract import SmartContract
    from storage.ipfs_simulator import IPFSSimulator

class PatientManager:
    def __init__(self):
        self.patients = {}
        self.load_patients()
    
    def register_patient(self, patient_id, name, age, gender, contact_info):
        """Register a new patient"""
        if patient_id in self.patients:
            return self.patients[patient_id]
        
        patient = Patient(patient_id, name, age, gender, contact_info)
        self.patients[patient_id] = patient
        self.save_patients()
        return patient
    
    def get_patient(self, patient_id):
        """Get patient by ID"""
        return self.patients.get(patient_id)
    
    def get_patient_public_key(self, public_key_str):
        """Get patient by public key string"""
        for patient in self.patients.values():
            if patient.public_key == public_key_str:
                return patient
        return None
    
    def save_patients(self):
        """Save patients to file"""
        os.makedirs(os.path.dirname(Config.PATIENTS_FILE), exist_ok=True)
        with open(Config.PATIENTS_FILE, 'w') as f:
            data = {pid: patient.to_dict() for pid, patient in self.patients.items()}
            json.dump(data, f, indent=2)
    
    def load_patients(self):
        """Load patients from file"""
        try:
            if os.path.exists(Config.PATIENTS_FILE):
                with open(Config.PATIENTS_FILE, 'r') as f:
                    data = json.load(f)
                    self.patients = {pid: Patient.from_dict(patient_data) for pid, patient_data in data.items()}
        except Exception as e:
            print(f"Error loading patients: {e}")
            self.patients = {}

class DoctorManager:
    def __init__(self):
        self.doctors = {}
        self.load_doctors()
    
    def register_doctor(self, doctor_id, name, specialization, license_number, hospital):
        """Register a new doctor"""
        if doctor_id in self.doctors:
            return self.doctors[doctor_id]
        
        doctor = Doctor(doctor_id, name, specialization, license_number, hospital)
        self.doctors[doctor_id] = doctor
        self.save_doctors()
        return doctor
    
    def get_doctor(self, doctor_id):
        """Get doctor by ID"""
        return self.doctors.get(doctor_id)
    
    def get_doctor_public_key(self, public_key_str):
        """Get doctor by public key string"""
        for doctor in self.doctors.values():
            if doctor.public_key == public_key_str:
                return doctor
        return None
    
    def save_doctors(self):
        """Save doctors to file"""
        os.makedirs(os.path.dirname(Config.DOCTORS_FILE), exist_ok=True)
        with open(Config.DOCTORS_FILE, 'w') as f:
            data = {did: doctor.to_dict() for did, doctor in self.doctors.items()}
            json.dump(data, f, indent=2)
    
    def load_doctors(self):
        """Load doctors from file"""
        try:
            if os.path.exists(Config.DOCTORS_FILE):
                with open(Config.DOCTORS_FILE, 'r') as f:
                    data = json.load(f)
                    self.doctors = {did: Doctor.from_dict(doctor_data) for did, doctor_data in data.items()}
        except Exception as e:
            print(f"Error loading doctors: {e}")
            self.doctors = {}

class HealthcareSystem:
    def __init__(self):
        self.patient_manager = PatientManager()
        self.doctor_manager = DoctorManager()
        self.blockchain = self.load_blockchain()
        self.ipfs = IPFSSimulator()
        self.ecc_manager = ECCManager()
        self.smart_contract = SmartContract(self.blockchain, self.patient_manager, self.doctor_manager)
        
        # Initialize with sample data if empty
        self.initialize_sample_data()
    
    def load_blockchain(self):
        """Load blockchain from file or create new"""
        try:
            if os.path.exists(Config.BLOCKCHAIN_FILE):
                with open(Config.BLOCKCHAIN_FILE, 'r') as f:
                    data = json.load(f)
                    return Blockchain.from_dict(data)
        except Exception as e:
            print(f"Error loading blockchain: {e}")
        
        return Blockchain()
    
    def save_blockchain(self):
        """Save blockchain to file"""
        os.makedirs(os.path.dirname(Config.BLOCKCHAIN_FILE), exist_ok=True)
        with open(Config.BLOCKCHAIN_FILE, 'w') as f:
            data = self.blockchain.to_dict()
            json.dump(data, f, indent=2)
    
    def initialize_sample_data(self):
        """Initialize with sample data for demo"""
        if not self.patient_manager.patients:
            self.register_patient("PAT001", "John Doe", 35, "Male", "john.doe@email.com")
            self.register_patient("PAT002", "Jane Smith", 28, "Female", "jane.smith@email.com")
            self.register_patient("PAT003", "Robert Johnson", 45, "Male", "robert.j@email.com")
        
        if not self.doctor_manager.doctors:
            self.register_doctor("DOC001", "Alice Brown", "Cardiology", "LIC001", "City General Hospital")
            self.register_doctor("DOC002", "Michael Wilson", "Neurology", "LIC002", "Metropolitan Medical Center")
            self.register_doctor("DOC003", "Sarah Davis", "Pediatrics", "LIC003", "Children's Hospital")
        
        # Grant some access permissions
        patient1 = self.patient_manager.get_patient("PAT001")
        patient2 = self.patient_manager.get_patient("PAT002")
        
        if patient1:
            patient1.grant_access("DOC001")
            patient1.grant_access("DOC002")
        
        if patient2:
            patient2.grant_access("DOC001")
        
        self.patient_manager.save_patients()
    
    def register_patient(self, patient_id, name, age, gender, contact_info):
        """Register a new patient"""
        return self.patient_manager.register_patient(patient_id, name, age, gender, contact_info)
    
    def register_doctor(self, doctor_id, name, specialization, license_number, hospital):
        """Register a new doctor"""
        return self.doctor_manager.register_doctor(doctor_id, name, specialization, license_number, hospital)
    
    def grant_doctor_access(self, patient_id, doctor_id):
        """Grant doctor access to patient records"""
        return self.smart_contract.grant_access(patient_id, doctor_id)
    
    def revoke_doctor_access(self, patient_id, doctor_id):
        """Revoke doctor access to patient records"""
        return self.smart_contract.revoke_access(patient_id, doctor_id)
    
    def create_medical_record(self, record_id, patient_id, doctor_id, diagnosis, prescription, notes):
        """Create and store a medical record on blockchain"""
        try:
            # Get patient and doctor
            patient = self.patient_manager.get_patient(patient_id)
            doctor = self.doctor_manager.get_doctor(doctor_id)
            
            if not patient or not doctor:
                raise Exception("Patient or doctor not found")
            
            # Check if doctor has access
            if not patient.has_access(doctor_id):
                raise Exception("Doctor does not have access to patient records")
            
            # Create medical record
            medical_record = MedicalRecord(record_id, patient_id, doctor_id, diagnosis, prescription, notes)
            
            # Convert doctor private key string back to object
            doctor_private_key, _ = KeyGenerator.string_to_keys(doctor.private_key, doctor.public_key)
            
            # Encrypt EMR data
            emr_data = medical_record.to_dict()
            encrypted_emr, encrypted_session_key = self.ecc_manager.encrypt_emr(emr_data, patient.public_key)
            
            # Store encrypted EMR on IPFS
            ipfs_hash = self.ipfs.store_data(encrypted_emr)
            medical_record.ipfs_hash = ipfs_hash
            medical_record.encrypted_session_key = encrypted_session_key
            
            # Create transaction data for signing
            transaction_data = {
                "patient_id": patient_id,
                "doctor_id": doctor_id,
                "ipfs_hash": ipfs_hash,
                "encrypted_session_key": encrypted_session_key
            }
            
            # Sign the transaction
            signature = self.ecc_manager.sign_data(transaction_data, doctor_private_key)
            
            # Process through smart contract and add to blockchain
            self.smart_contract.process_emr_creation(
                patient_id, doctor_id, ipfs_hash, encrypted_session_key, signature
            )
            
            # Save blockchain state
            self.save_blockchain()
            
            return True
        
        except Exception as e:
            print(f"Error creating medical record: {e}")
            return False
    
    def get_patient_records(self, patient_id):
        """Get all medical records for a patient"""
        try:
            records = []
            transactions = self.blockchain.get_emr_transactions(patient_id=patient_id)
            
            for transaction in transactions:
                record_data = {
                    'record_id': f"EMR_{transaction['patient_id']}_{transactions.index(transaction) + 1}",
                    'patient_id': transaction['patient_id'],
                    'doctor_id': transaction['doctor_id'],
                    'diagnosis': "Encrypted - Requires decryption",
                    'prescription': "Encrypted - Requires decryption", 
                    'notes': "Encrypted - Requires decryption",
                    'timestamp': transaction['timestamp'],
                    'ipfs_hash': transaction['ipfs_hash'],
                    'encrypted_session_key': transaction['encrypted_session_key']
                }
                records.append(record_data)
            
            return records
        
        except Exception as e:
            print(f"Error retrieving patient records: {e}")
            return []
    
    def decrypt_medical_record(self, encrypted_data, encrypted_key, doctor_private_key_str):
        """Decrypt a medical record for authorized doctors"""
        try:
            # Convert doctor private key string back to object
            doctor_private_key, _ = KeyGenerator.string_to_keys(doctor_private_key_str, "")
            
            # Decrypt the data
            decrypted_data = self.ecc_manager.decrypt_emr(encrypted_data, encrypted_key, doctor_private_key)
            return json.loads(decrypted_data)
        
        except Exception as e:
            print(f"Error decrypting medical record: {e}")
            return None
    
    def get_system_stats(self):
        """Get system statistics"""
        return {
            'total_patients': len(self.patient_manager.patients),
            'total_doctors': len(self.doctor_manager.doctors),
            'total_blocks': len(self.blockchain.chain),
            'total_transactions': sum(len(block.data) if isinstance(block.data, list) else 1 
                                   for block in self.blockchain.chain[1:]),
            'blockchain_valid': self.blockchain.is_chain_valid(),
            'latest_block_hash': self.blockchain.get_latest_block().hash
        }