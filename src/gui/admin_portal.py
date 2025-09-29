import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class AdminPortal:
    def __init__(self, root, healthcare_system):
        self.root = root
        self.healthcare_system = healthcare_system
        
        self.root.title("Admin Portal - Healthcare Blockchain")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f8ff')
        
        self.setup_ui()
    
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#e74c3c', height=80)
        header_frame.pack(fill='x', padx=10, pady=5)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="Admin Portal - System Overview",
            font=('Arial', 18, 'bold'),
            fg='white',
            bg='#e74c3c'
        )
        title_label.pack(expand=True)
        
        # Main Content Frame
        main_frame = ttk.Notebook(self.root)
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # System Overview Tab
        overview_tab = ttk.Frame(main_frame)
        main_frame.add(overview_tab, text="System Overview")
        self.setup_overview_tab(overview_tab)
        
        # Blockchain Viewer Tab
        blockchain_tab = ttk.Frame(main_frame)
        main_frame.add(blockchain_tab, text="Blockchain Viewer")
        self.setup_blockchain_tab(blockchain_tab)
        
        # Data Management Tab
        data_tab = ttk.Frame(main_frame)
        main_frame.add(data_tab, text="Data Management")
        self.setup_data_tab(data_tab)
    
    def setup_overview_tab(self, parent):
        overview_frame = tk.Frame(parent, bg='#f0f8ff')
        overview_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Statistics
        stats_frame = tk.LabelFrame(overview_frame, text="System Statistics", font=('Arial', 12, 'bold'), bg='#f0f8ff')
        stats_frame.pack(fill='x', pady=10)
        
        stats_text = scrolledtext.ScrolledText(stats_frame, height=8, width=80)
        stats_text.pack(padx=10, pady=10, fill='both')
        
        # Calculate statistics
        total_patients = len(self.healthcare_system.patient_manager.patients)
        total_doctors = len(self.healthcare_system.doctor_manager.doctors)
        total_blocks = len(self.healthcare_system.blockchain.chain)
        total_transactions = sum(len(block.data) if isinstance(block.data, list) else 1 for block in self.healthcare_system.blockchain.chain[1:])
        chain_valid = self.healthcare_system.blockchain.is_chain_valid()
        
        stats_text.insert(tk.END, 
            f"System Status: {'ACTIVE' if chain_valid else 'ERROR'}\n"
            f"Blockchain Valid: {'YES' if chain_valid else 'NO'}\n"
            f"Total Patients: {total_patients}\n"
            f"Total Doctors: {total_doctors}\n"
            f"Total Blocks: {total_blocks}\n"
            f"Total Transactions: {total_transactions}\n"
            f"Blockchain Difficulty: {self.healthcare_system.blockchain.difficulty}\n"
            f"Latest Block Hash: {self.healthcare_system.blockchain.get_latest_block().hash[:20]}...\n"
        )
        stats_text.config(state=tk.DISABLED)
        
        # Recent Activity
        activity_frame = tk.LabelFrame(overview_frame, text="Recent Activity", font=('Arial', 12, 'bold'), bg='#f0f8ff')
        activity_frame.pack(expand=True, fill='both', pady=10)
        
        self.activity_text = scrolledtext.ScrolledText(activity_frame, height=12, width=80)
        self.activity_text.pack(padx=10, pady=10, fill='both', expand=True)
        self.update_activity_text()
    
    def setup_blockchain_tab(self, parent):
        blockchain_frame = tk.Frame(parent, bg='#f0f8ff')
        blockchain_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Blockchain Explorer
        explorer_frame = tk.LabelFrame(blockchain_frame, text="Blockchain Explorer", font=('Arial', 12, 'bold'), bg='#f0f8ff')
        explorer_frame.pack(expand=True, fill='both', pady=10)
        
        # Block selection
        selection_frame = tk.Frame(explorer_frame, bg='#f0f8ff')
        selection_frame.pack(fill='x', pady=5)
        
        tk.Label(selection_frame, text="Select Block:", font=('Arial', 10), bg='#f0f8ff').pack(side=tk.LEFT, padx=5)
        self.block_var = tk.StringVar()
        block_combobox = ttk.Combobox(selection_frame, textvariable=self.block_var, state='readonly')
        block_combobox['values'] = [f"Block {i}" for i in range(len(self.healthcare_system.blockchain.chain))]
        block_combobox.current(0)
        block_combobox.pack(side=tk.LEFT, padx=5)
        block_combobox.bind('<<ComboboxSelected>>', self.on_block_selected)
        
        # Block details
        self.block_details_text = scrolledtext.ScrolledText(explorer_frame, height=20, width=80)
        self.block_details_text.pack(padx=10, pady=10, fill='both', expand=True)
        self.on_block_selected()  # Show first block initially
    
    def setup_data_tab(self, parent):
        data_frame = tk.Frame(parent, bg='#f0f8ff')
        data_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Patients List
        patients_frame = tk.LabelFrame(data_frame, text="Registered Patients", font=('Arial', 12, 'bold'), bg='#f0f8ff')
        patients_frame.pack(fill='both', pady=10, side=tk.LEFT, expand=True)
        
        patients_text = scrolledtext.ScrolledText(patients_frame, height=15, width=40)
        patients_text.pack(padx=10, pady=10, fill='both', expand=True)
        
        for patient_id, patient in self.healthcare_system.patient_manager.patients.items():
            patients_text.insert(tk.END, 
                f"ID: {patient.patient_id}\n"
                f"Name: {patient.name}\n"
                f"Age: {patient.age}\n"
                f"Authorized Doctors: {len(patient.authorized_doctors)}\n"
                f"{'-'*30}\n"
            )
        patients_text.config(state=tk.DISABLED)
        
        # Doctors List
        doctors_frame = tk.LabelFrame(data_frame, text="Registered Doctors", font=('Arial', 12, 'bold'), bg='#f0f8ff')
        doctors_frame.pack(fill='both', pady=10, side=tk.RIGHT, expand=True)
        
        doctors_text = scrolledtext.ScrolledText(doctors_frame, height=15, width=40)
        doctors_text.pack(padx=10, pady=10, fill='both', expand=True)
        
        for doctor_id, doctor in self.healthcare_system.doctor_manager.doctors.items():
            doctors_text.insert(tk.END, 
                f"ID: {doctor.doctor_id}\n"
                f"Name: Dr. {doctor.name}\n"
                f"Specialization: {doctor.specialization}\n"
                f"Hospital: {doctor.hospital}\n"
                f"{'-'*30}\n"
            )
        doctors_text.config(state=tk.DISABLED)
    
    def on_block_selected(self, event=None):
        selected = self.block_var.get()
        if selected:
            block_index = int(selected.split()[1])
            block = self.healthcare_system.blockchain.chain[block_index]
            
            self.block_details_text.config(state=tk.NORMAL)
            self.block_details_text.delete(1.0, tk.END)
            
            self.block_details_text.insert(tk.END, 
                f"Block {block.index}\n"
                f"Timestamp: {block.timestamp}\n"
                f"Previous Hash: {block.previous_hash[:20]}...\n"
                f"Hash: {block.hash}\n"
                f"Nonce: {block.nonce}\n"
                f"Data:\n"
            )
            
            if isinstance(block.data, list):
                for i, transaction in enumerate(block.data):
                    self.block_details_text.insert(tk.END, f"\nTransaction {i+1}:\n")
                    for key, value in transaction.items():
                        self.block_details_text.insert(tk.END, f"  {key}: {value}\n")
            else:
                self.block_details_text.insert(tk.END, f"  {block.data}\n")
            
            self.block_details_text.config(state=tk.DISABLED)
    
    def update_activity_text(self):
        self.activity_text.config(state=tk.NORMAL)
        self.activity_text.delete(1.0, tk.END)
        
        # Get recent transactions from last few blocks
        recent_transactions = []
        for block in self.healthcare_system.blockchain.chain[-5:]:  # Last 5 blocks
            if isinstance(block.data, list):
                for transaction in block.data:
                    if transaction.get('type') == 'EMR_CREATION':
                        recent_transactions.append(transaction)
        
        if recent_transactions:
            for transaction in recent_transactions[-10:]:  # Show last 10 transactions
                self.activity_text.insert(tk.END,
                    f"EMR Created - Patient: {transaction.get('patient_id')} | "
                    f"Doctor: {transaction.get('doctor_id')} | "
                    f"Time: {transaction.get('timestamp')}\n"
                )
        else:
            self.activity_text.insert(tk.END, "No recent activity found.")
        
        self.activity_text.config(state=tk.DISABLED)