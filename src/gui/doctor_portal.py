import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class DoctorPortal:
    def __init__(self, root, healthcare_system):
        self.root = root
        self.healthcare_system = healthcare_system
        self.current_doctor = None
        
        self.root.title("Doctor Portal - Healthcare Blockchain")
        self.root.geometry("1000x800")
        self.root.configure(bg='#f0f8ff')
        
        self.setup_ui()
    
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#27ae60', height=80)
        header_frame.pack(fill='x', padx=10, pady=5)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="Doctor Portal",
            font=('Arial', 18, 'bold'),
            fg='white',
            bg='#27ae60'
        )
        title_label.pack(expand=True)
        
        # Main Content Frame
        main_frame = ttk.Notebook(self.root)
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Login Tab
        self.login_tab = ttk.Frame(main_frame)
        main_frame.add(self.login_tab, text="Doctor Login")
        self.setup_login_tab()
        
        # EMR Management Tab
        self.emr_tab = ttk.Frame(main_frame)
        main_frame.add(self.emr_tab, text="EMR Management")
        self.setup_emr_tab()
        
        # Patient Access Tab
        self.access_tab = ttk.Frame(main_frame)
        main_frame.add(self.access_tab, text="Patient Access")
        self.setup_access_tab()
    
    def setup_login_tab(self):
        login_frame = tk.Frame(self.login_tab, bg='#f0f8ff')
        login_frame.pack(expand=True, fill='both', padx=50, pady=50)
        
        tk.Label(login_frame, text="Doctor ID:", font=('Arial', 12), bg='#f0f8ff').pack(pady=10)
        self.doctor_id_entry = tk.Entry(login_frame, font=('Arial', 12), width=30)
        self.doctor_id_entry.pack(pady=10)
        
        tk.Label(login_frame, text="Name:", font=('Arial', 12), bg='#f0f8ff').pack(pady=10)
        self.doctor_name_entry = tk.Entry(login_frame, font=('Arial', 12), width=30)
        self.doctor_name_entry.pack(pady=10)
        
        tk.Label(login_frame, text="Specialization:", font=('Arial', 12), bg='#f0f8ff').pack(pady=10)
        self.specialization_entry = tk.Entry(login_frame, font=('Arial', 12), width=30)
        self.specialization_entry.pack(pady=10)
        
        login_btn = tk.Button(
            login_frame,
            text="Login / Register",
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            width=20,
            command=self.doctor_login
        )
        login_btn.pack(pady=20)
        
        # Doctor List
        tk.Label(login_frame, text="Existing Doctors:", font=('Arial', 12, 'bold'), bg='#f0f8ff').pack(pady=10)
        doctor_list = scrolledtext.ScrolledText(login_frame, height=8, width=80)
        doctor_list.pack(pady=10)
        
        # Populate doctor list
        for doctor_id, doctor in self.healthcare_system.doctor_manager.doctors.items():
            doctor_list.insert(tk.END, f"ID: {doctor_id} | Dr. {doctor.name} | {doctor.specialization}\n")
        doctor_list.config(state=tk.DISABLED)
    
    def setup_emr_tab(self):
        emr_frame = tk.Frame(self.emr_tab, bg='#f0f8ff')
        emr_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Create EMR Section
        create_frame = tk.LabelFrame(emr_frame, text="Create New Medical Record", font=('Arial', 12, 'bold'), bg='#f0f8ff')
        create_frame.pack(fill='x', pady=10)
        
        tk.Label(create_frame, text="Patient ID:", font=('Arial', 10), bg='#f0f8ff').pack(pady=5)
        self.patient_id_entry = tk.Entry(create_frame, font=('Arial', 10), width=30)
        self.patient_id_entry.pack(pady=5)
        
        tk.Label(create_frame, text="Diagnosis:", font=('Arial', 10), bg='#f0f8ff').pack(pady=5)
        self.diagnosis_entry = tk.Entry(create_frame, font=('Arial', 10), width=50)
        self.diagnosis_entry.pack(pady=5)
        
        tk.Label(create_frame, text="Prescription:", font=('Arial', 10), bg='#f0f8ff').pack(pady=5)
        self.prescription_entry = tk.Entry(create_frame, font=('Arial', 10), width=50)
        self.prescription_entry.pack(pady=5)
        
        tk.Label(create_frame, text="Notes:", font=('Arial', 10), bg='#f0f8ff').pack(pady=5)
        self.notes_entry = tk.Text(create_frame, height=4, width=50)
        self.notes_entry.pack(pady=5)
        
        create_btn = tk.Button(
            create_frame,
            text="Create EMR Record",
            font=('Arial', 10, 'bold'),
            bg='#3498db',
            fg='white',
            command=self.create_emr
        )
        create_btn.pack(pady=10)
        
        # View EMR Section
        view_frame = tk.LabelFrame(emr_frame, text="View Patient Records", font=('Arial', 12, 'bold'), bg='#f0f8ff')
        view_frame.pack(expand=True, fill='both', pady=10)
        
        tk.Label(view_frame, text="Patient ID to View:", font=('Arial', 10), bg='#f0f8ff').pack(pady=5)
        self.view_patient_entry = tk.Entry(view_frame, font=('Arial', 10), width=30)
        self.view_patient_entry.pack(pady=5)
        
        view_btn = tk.Button(
            view_frame,
            text="View Records",
            font=('Arial', 10),
            bg='#9b59b6',
            fg='white',
            command=self.view_patient_records
        )
        view_btn.pack(pady=5)
        
        self.view_records_text = scrolledtext.ScrolledText(view_frame, height=15, width=80)
        self.view_records_text.pack(padx=10, pady=10, fill='both', expand=True)
        self.view_records_text.insert(tk.END, "Please login and enter a Patient ID to view records.")
        self.view_records_text.config(state=tk.DISABLED)
    
    def setup_access_tab(self):
        access_frame = tk.Frame(self.access_tab, bg='#f0f8ff')
        access_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Request Access Section
        request_frame = tk.LabelFrame(access_frame, text="Request Patient Access", font=('Arial', 12, 'bold'), bg='#f0f8ff')
        request_frame.pack(fill='x', pady=10)
        
        tk.Label(request_frame, text="Patient ID:", font=('Arial', 10), bg='#f0f8ff').pack(pady=5)
        self.request_patient_entry = tk.Entry(request_frame, font=('Arial', 10), width=30)
        self.request_patient_entry.pack(pady=5)
        
        request_btn = tk.Button(
            request_frame,
            text="Request Access",
            font=('Arial', 10),
            bg='#f39c12',
            fg='white',
            command=self.request_access
        )
        request_btn.pack(pady=10)
        
        # Accessible Patients
        accessible_frame = tk.LabelFrame(access_frame, text="Currently Accessible Patients", font=('Arial', 12, 'bold'), bg='#f0f8ff')
        accessible_frame.pack(expand=True, fill='both', pady=10)
        
        self.accessible_patients_text = scrolledtext.ScrolledText(accessible_frame, height=12, width=80)
        self.accessible_patients_text.pack(padx=10, pady=10, fill='both', expand=True)
        self.accessible_patients_text.insert(tk.END, "Please login first...")
        self.accessible_patients_text.config(state=tk.DISABLED)
    
    def doctor_login(self):
        doctor_id = self.doctor_id_entry.get().strip()
        name = self.doctor_name_entry.get().strip()
        specialization = self.specialization_entry.get().strip()
        
        if not doctor_id or not name or not specialization:
            messagebox.showerror("Error", "Please enter all fields")
            return
        
        # Register or login doctor
        doctor = self.healthcare_system.register_doctor(doctor_id, name, specialization, f"LIC{doctor_id}", "General Hospital")
        if doctor:
            self.current_doctor = doctor
            messagebox.showinfo("Success", f"Welcome Dr. {doctor.name}!")
            self.update_access_tab()
        else:
            messagebox.showerror("Error", "Login failed")
    
    def create_emr(self):
        if not self.current_doctor:
            messagebox.showerror("Error", "Please login first")
            return
        
        patient_id = self.patient_id_entry.get().strip()
        diagnosis = self.diagnosis_entry.get().strip()
        prescription = self.prescription_entry.get().strip()
        notes = self.notes_entry.get(1.0, tk.END).strip()
        
        if not all([patient_id, diagnosis, prescription]):
            messagebox.showerror("Error", "Please fill all required fields")
            return
        
        try:
            record_id = f"EMR_{patient_id}_{len(self.healthcare_system.get_patient_records(patient_id)) + 1}"
            success = self.healthcare_system.create_medical_record(
                record_id, patient_id, self.current_doctor.doctor_id,
                diagnosis, prescription, notes
            )
            
            if success:
                messagebox.showinfo("Success", "Medical record created and stored on blockchain!")
                # Clear fields
                self.patient_id_entry.delete(0, tk.END)
                self.diagnosis_entry.delete(0, tk.END)
                self.prescription_entry.delete(0, tk.END)
                self.notes_entry.delete(1.0, tk.END)
            else:
                messagebox.showerror("Error", "Failed to create medical record. Check if you have access.")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create record: {str(e)}")
    
    def view_patient_records(self):
        if not self.current_doctor:
            messagebox.showerror("Error", "Please login first")
            return
        
        patient_id = self.view_patient_entry.get().strip()
        if not patient_id:
            messagebox.showerror("Error", "Please enter Patient ID")
            return
        
        try:
            records = self.healthcare_system.get_patient_records(patient_id)
            self.view_records_text.config(state=tk.NORMAL)
            self.view_records_text.delete(1.0, tk.END)
            
            if records:
                for record in records:
                    self.view_records_text.insert(tk.END, 
                        f"Record ID: {record['record_id']}\n"
                        f"Doctor: {record['doctor_id']}\n"
                        f"Diagnosis: {record['diagnosis']}\n"
                        f"Prescription: {record['prescription']}\n"
                        f"Notes: {record.get('notes', 'N/A')}\n"
                        f"Date: {record['timestamp']}\n"
                        f"{'-'*50}\n"
                    )
            else:
                self.view_records_text.insert(tk.END, "No records found or access denied.")
            
            self.view_records_text.config(state=tk.DISABLED)
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve records: {str(e)}")
    
    def request_access(self):
        if not self.current_doctor:
            messagebox.showerror("Error", "Please login first")
            return
        
        patient_id = self.request_patient_entry.get().strip()
        if not patient_id:
            messagebox.showerror("Error", "Please enter Patient ID")
            return
        
        # In a real system, this would send a request to the patient
        # For demo, we'll auto-grant access
        if self.healthcare_system.grant_doctor_access(patient_id, self.current_doctor.doctor_id):
            messagebox.showinfo("Success", f"Access granted to patient {patient_id}")
            self.update_access_tab()
        else:
            messagebox.showerror("Error", "Patient not found or access request failed")
    
    def update_access_tab(self):
        if not self.current_doctor:
            return
        
        self.accessible_patients_text.config(state=tk.NORMAL)
        self.accessible_patients_text.delete(1.0, tk.END)
        
        accessible_patients = []
        for patient_id, patient in self.healthcare_system.patient_manager.patients.items():
            if patient.has_access(self.current_doctor.doctor_id):
                accessible_patients.append(patient)
        
        if accessible_patients:
            for patient in accessible_patients:
                self.accessible_patients_text.insert(tk.END, 
                    f"ID: {patient.patient_id} | {patient.name} | Age: {patient.age}\n"
                )
        else:
            self.accessible_patients_text.insert(tk.END, "No accessible patients. Request access first.")
        
        self.accessible_patients_text.config(state=tk.DISABLED)