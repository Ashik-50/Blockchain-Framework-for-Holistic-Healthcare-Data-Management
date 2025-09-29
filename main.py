import tkinter as tk
import os
import sys

# Add the src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from src.healthcare_system import HealthcareSystem
    from src.gui.main_window import MainWindow
    print("✅ All modules imported successfully!")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please make sure all files are in the correct structure.")
    sys.exit(1)

def main():
    """Main function to start the Healthcare Blockchain Application"""
    print("Initializing ECC-Blockchain Healthcare Framework...")
    
    try:
        # Initialize healthcare system
        healthcare_system = HealthcareSystem()
        
        # Create main window
        root = tk.Tk()
        app = MainWindow(root, healthcare_system)
        
        # Set window icon and title
        root.title("ECC-Blockchain Healthcare Framework")
        
        # Center the window
        window_width = 800
        window_height = 600
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        print("System initialized successfully!")
        print(f"Patients: {len(healthcare_system.patient_manager.patients)}")
        print(f"Doctors: {len(healthcare_system.doctor_manager.doctors)}")
        print(f"Blocks: {len(healthcare_system.blockchain.chain)}")
        print("Blockchain valid:", healthcare_system.blockchain.is_chain_valid())
        
        # Start the GUI
        root.mainloop()
        
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()