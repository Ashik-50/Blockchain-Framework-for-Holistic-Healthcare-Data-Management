import json
from datetime import datetime

class MedicalRecord:
    def __init__(self, record_id, patient_id, doctor_id, diagnosis, prescription, notes):
        self.record_id = record_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.diagnosis = diagnosis
        self.prescription = prescription
        self.notes = notes
        self.timestamp = datetime.now().isoformat()
        self.ipfs_hash = None
        self.encrypted_session_key = None
    
    def to_dict(self):
        """Convert to dictionary for storage"""
        return {
            'record_id': self.record_id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'diagnosis': self.diagnosis,
            'prescription': self.prescription,
            'notes': self.notes,
            'timestamp': self.timestamp,
            'ipfs_hash': self.ipfs_hash,
            'encrypted_session_key': self.encrypted_session_key
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create MedicalRecord object from dictionary"""
        record = cls(
            data['record_id'],
            data['patient_id'],
            data['doctor_id'],
            data['diagnosis'],
            data['prescription'],
            data['notes']
        )
        record.timestamp = data['timestamp']
        record.ipfs_hash = data['ipfs_hash']
        record.encrypted_session_key = data['encrypted_session_key']
        return record