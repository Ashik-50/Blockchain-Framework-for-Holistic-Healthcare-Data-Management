import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class PatientPortal:
    def __init__(self, root, healthcare_system):
        self.root = root
        self.healthcare_system = healthcare_system
        self.current_patient = None
        
        self.root.title("Patient Portal - Healthcare Blockchain")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f8ff')
        
        self.setup_ui()
    
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#3498db', height=80)
        header_frame.pack(fill='x', padx=10, pady=5)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="Patient Portal",
            font=('Arial', 18, 'bold'),
            fg='white',
            bg='#3498db'
        )
        title_label.pack(expand=True)
        
        # Main Content Frame
        main_frame = ttk.Notebook(self.root)
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Login Tab
        self.login_tab = ttk.Frame(main_frame)
        main_frame.add(self.login_tab, text="Patient Login")
        self.setup_login_tab()
        
        # Dashboard Tab
        self.dashboard_tab = ttk.Frame(main_frame)
        main_frame.add(self.dashboard_tab, text="Dashboard")
        self.setup_dashboard_tab()
        
        # Access Control Tab
        self.access_tab = ttk.Frame(main_frame)
        main_frame.add(self.access_tab, text="Access Control")
        self.setup_access_tab()
    
    def setup_login_tab(self):
        login_frame = tk.Frame(self.login_tab, bg='#f0f8ff')
        login_frame.pack(expand=True, fill='both', padx=50, pady=50)
        
        tk.Label(login_frame, text="Patient ID:", font=('Arial', 12), bg='#f0f8ff').pack(pady=10)
        self.patient_id_entry = tk.Entry(login_frame, font=('Arial', 12), width=30)
        self.patient_id_entry.pack(pady=10)
        
        tk.Label(login_frame, text="Name:", font=('Arial', 12), bg='#f0f8ff').pack(pady=10)
        self.patient_name_entry = tk.Entry(login_frame, font=('Arial', 12), width=30)
        self.patient_name_entry.pack(pady=10)
        
        login_btn = tk.Button(
            login_frame,
            text="Login / Register",
            font=('Arial', 12, 'bold'),
            bg='#3498db',
            fg='white',
            width=20,
            command=self.patient_login
        )
        login_btn.pack(pady=20)
        
        # Patient List
        tk.Label(login_frame, text="Existing Patients:", font=('Arial', 12, 'bold'), bg='#f0f8ff').pack(pady=10)
        patient_list = scrolledtext.ScrolledText(login_frame, height=8, width=60)
        patient_list.pack(pady=10)
        
        # Populate patient list
        for patient_id, patient in self.healthcare_system.patient_manager.patients.items():
            patient_list.insert(tk.END, f"ID: {patient_id} | Name: {patient.name} | Age: {patient.age}\n")
        patient_list.config(state=tk.DISABLED)
    
    def setup_dashboard_tab(self):
        dashboard_frame = tk.Frame(self.dashboard_tab, bg='#f0f8ff')
        dashboard_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Patient Info
        self.info_frame = tk.LabelFrame(dashboard_frame, text="Patient Information", font=('Arial', 12, 'bold'), bg='#f0f8ff')
        self.info_frame.pack(fill='x', pady=10)
        
        self.info_text = scrolledtext.ScrolledText(self.info_frame, height=6, width=80)
        self.info_text.pack(padx=10, pady=10)
        self.info_text.insert(tk.END, "Please login first...")
        self.info_text.config(state=tk.DISABLED)
        
        # Medical Records
        records_frame = tk.LabelFrame(dashboard_frame, text="Medical Records", font=('Arial', 12, 'bold'), bg='#f0f8ff')
        records_frame.pack(expand=True, fill='both', pady=10)
        
        self.records_text = scrolledtext.ScrolledText(records_frame, height=12, width=80)
        self.records_text.pack(padx=10, pady=10, fill='both', expand=True)
        self.records_text.insert(tk.END, "No records to display. Please login first.")
        self.records_text.config(state=tk.DISABLED)
    
    def setup_access_tab(self):
        access_frame = tk.Frame(self.access_tab, bg='#f0f8ff')
        access_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Grant Access Section
        grant_frame = tk.LabelFrame(access_frame, text="Grant Access to Doctor", font=('Arial', 12, 'bold'), bg='#f0f8ff')
        grant_frame.pack(fill='x', pady=10)
        
        tk.Label(grant_frame, text="Doctor ID:", font=('Arial', 10), bg='#f0f8ff').pack(pady=5)
        self.grant_doctor_entry = tk.Entry(grant_frame, font=('Arial', 10), width=30)
        self.grant_doctor_entry.pack(pady=5)
        
        grant_btn = tk.Button(
            grant_frame,
            text="Grant Access",
            font=('Arial', 10),
            bg='#27ae60',
            fg='white',
            command=self.grant_access
        )
        grant_btn.pack(pady=10)
        
        # Revoke Access Section
        revoke_frame = tk.LabelFrame(access_frame, text="Revoke Access from Doctor", font=('Arial', 12, 'bold'), bg='#f0f8ff')
        revoke_frame.pack(fill='x', pady=10)
        
        tk.Label(revoke_frame, text="Doctor ID:", font=('Arial', 10), bg='#f0f8ff').pack(pady=5)
        self.revoke_doctor_entry = tk.Entry(revoke_frame, font=('Arial', 10), width=30)
        self.revoke_doctor_entry.pack(pady=5)
        
        revoke_btn = tk.Button(
            revoke_frame,
            text="Revoke Access",
            font=('Arial', 10),
            bg='#e74c3c',
            fg='white',
            command=self.revoke_access
        )
        revoke_btn.pack(pady=10)
        
        # Authorized Doctors
        auth_frame = tk.LabelFrame(access_frame, text="Currently Authorized Doctors", font=('Arial', 12, 'bold'), bg='#f0f8ff')
        auth_frame.pack(expand=True, fill='both', pady=10)
        
        self.auth_doctors_text = scrolledtext.ScrolledText(auth_frame, height=8, width=80)
        self.auth_doctors_text.pack(padx=10, pady=10, fill='both', expand=True)
        self.auth_doctors_text.insert(tk.END, "Please login first...")
        self.auth_doctors_text.config(state=tk.DISABLED)
    
    def patient_login(self):
        patient_id = self.patient_id_entry.get().strip()
        name = self.patient_name_entry.get().strip()
        
        if not patient_id or not name:
            messagebox.showerror("Error", "Please enter both Patient ID and Name")
            return
        
        # Register or login patient
        patient = self.healthcare_system.register_patient(patient_id, name, 30, "Unknown", "N/A")
        if patient:
            self.current_patient = patient
            messagebox.showinfo("Success", f"Welcome {patient.name}!")
            self.update_dashboard()
        else:
            messagebox.showerror("Error", "Login failed")
    
    def update_dashboard(self):
        if not self.current_patient:
            return
        
        # Update patient info
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, 
            f"Patient ID: {self.current_patient.patient_id}\n"
            f"Name: {self.current_patient.name}\n"
            f"Age: {self.current_patient.age}\n"
            f"Gender: {self.current_patient.gender}\n"
            f"Contact: {self.current_patient.contact_info}\n"
            f"Authorized Doctors: {len(self.current_patient.authorized_doctors)}"
        )
        self.info_text.config(state=tk.DISABLED)
        
        # Update medical records
        self.records_text.config(state=tk.NORMAL)
        self.records_text.delete(1.0, tk.END)
        records = self.healthcare_system.get_patient_records(self.current_patient.patient_id)
        if records:
            for record in records:
                self.records_text.insert(tk.END, 
                    f"Record ID: {record['record_id']}\n"
                    f"Doctor: {record['doctor_id']}\n"
                    f"Diagnosis: {record['diagnosis']}\n"
                    f"Prescription: {record['prescription']}\n"
                    f"Date: {record['timestamp']}\n"
                    f"{'-'*50}\n"
                )
        else:
            self.records_text.insert(tk.END, "No medical records found.")
        self.records_text.config(state=tk.DISABLED)
        
        # Update authorized doctors
        self.auth_doctors_text.config(state=tk.NORMAL)
        self.auth_doctors_text.delete(1.0, tk.END)
        if self.current_patient.authorized_doctors:
            for doctor_id in self.current_patient.authorized_doctors:
                doctor = self.healthcare_system.doctor_manager.get_doctor(doctor_id)
                if doctor:
                    self.auth_doctors_text.insert(tk.END, 
                        f"ID: {doctor.doctor_id} | Dr. {doctor.name} | {doctor.specialization}\n"
                    )
        else:
            self.auth_doctors_text.insert(tk.END, "No authorized doctors.")
        self.auth_doctors_text.config(state=tk.DISABLED)
    
    def grant_access(self):
        if not self.current_patient:
            messagebox.showerror("Error", "Please login first")
            return
        
        doctor_id = self.grant_doctor_entry.get().strip()
        if not doctor_id:
            messagebox.showerror("Error", "Please enter Doctor ID")
            return
        
        if self.healthcare_system.grant_doctor_access(self.current_patient.patient_id, doctor_id):
            messagebox.showinfo("Success", f"Access granted to Doctor {doctor_id}")
            self.update_dashboard()
        else:
            messagebox.showerror("Error", "Failed to grant access")
    
    def revoke_access(self):
        if not self.current_patient:
            messagebox.showerror("Error", "Please login first")
            return
        
        doctor_id = self.revoke_doctor_entry.get().strip()
        if not doctor_id:
            messagebox.showerror("Error", "Please enter Doctor ID")
            return
        
        if self.healthcare_system.revoke_doctor_access(self.current_patient.patient_id, doctor_id):
            messagebox.showinfo("Success", f"Access revoked from Doctor {doctor_id}")
            self.update_dashboard()
        else:
            messagebox.showerror("Error", "Failed to revoke access")