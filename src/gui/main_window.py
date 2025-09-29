import tkinter as tk
from tkinter import ttk
import sys
import os

# Remove Pillow imports and use tkinter's built-in functionality
try:
    from ..gui.patient_portal import PatientPortal
    from ..gui.doctor_portal import DoctorPortal
    from ..gui.admin_portal import AdminPortal
    from ..utils.config import Config
except ImportError:
    from src.gui.patient_portal import PatientPortal
    from src.gui.doctor_portal import DoctorPortal
    from src.gui.admin_portal import AdminPortal
    from src.utils.config import Config

class MainWindow:
    def __init__(self, root, healthcare_system):
        self.root = root
        self.healthcare_system = healthcare_system
        self.root.title("ECC-Blockchain Healthcare Framework")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f8ff')
        
        self.setup_ui()
    
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=100)
        header_frame.pack(fill='x', padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="ECC-Blockchain Healthcare Framework",
            font=('Arial', 20, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Secure Healthcare Data Management System",
            font=('Arial', 12),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        subtitle_label.pack(expand=True)
        
        # Main Content
        content_frame = tk.Frame(self.root, bg='#f0f8ff')
        content_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Welcome Message
        welcome_label = tk.Label(
            content_frame,
            text="Welcome to the Healthcare Blockchain System",
            font=('Arial', 16, 'bold'),
            fg='#2c3e50',
            bg='#f0f8ff'
        )
        welcome_label.pack(pady=20)
        
        # Portal Selection Buttons
        button_frame = tk.Frame(content_frame, bg='#f0f8ff')
        button_frame.pack(expand=True)
        
        # Patient Portal Button
        patient_btn = tk.Button(
            button_frame,
            text="Patient Portal",
            font=('Arial', 14),
            bg='#3498db',
            fg='white',
            width=20,
            height=3,
            command=self.open_patient_portal
        )
        patient_btn.pack(pady=10)
        
        # Doctor Portal Button
        doctor_btn = tk.Button(
            button_frame,
            text="Doctor Portal",
            font=('Arial', 14),
            bg='#27ae60',
            fg='white',
            width=20,
            height=3,
            command=self.open_doctor_portal
        )
        doctor_btn.pack(pady=10)
        
        # Admin Portal Button
        admin_btn = tk.Button(
            button_frame,
            text="Admin Portal",
            font=('Arial', 14),
            bg='#e74c3c',
            fg='white',
            width=20,
            height=3,
            command=self.open_admin_portal
        )
        admin_btn.pack(pady=10)
        
        # System Info
        info_frame = tk.Frame(content_frame, bg='#f0f8ff')
        info_frame.pack(fill='x', pady=20)
        
        stats_label = tk.Label(
            info_frame,
            text=f"System Status: Active | Patients: {len(self.healthcare_system.patient_manager.patients)} | "
                 f"Doctors: {len(self.healthcare_system.doctor_manager.doctors)} | "
                 f"Blocks: {len(self.healthcare_system.blockchain.chain)}",
            font=('Arial', 10),
            fg='#7f8c8d',
            bg='#f0f8ff'
        )
        stats_label.pack()
    
    def open_patient_portal(self):
        patient_window = tk.Toplevel(self.root)
        PatientPortal(patient_window, self.healthcare_system)
    
    def open_doctor_portal(self):
        doctor_window = tk.Toplevel(self.root)
        DoctorPortal(doctor_window, self.healthcare_system)
    
    def open_admin_portal(self):
        admin_window = tk.Toplevel(self.root)
        AdminPortal(admin_window, self.healthcare_system)