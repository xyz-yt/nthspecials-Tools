import os
import sys
import ctypes
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
from typing import List

def hide_console():
    """Hide the console window in GUI mode"""
    if sys.platform == 'win32':
        console_window = ctypes.windll.kernel32.GetConsoleWindow()
        if console_window != 0:
            ctypes.windll.user32.ShowWindow(console_window, 0)

# Hide the console immediately when starting
hide_console()

def is_admin():
    """Check if the script is running with administrator privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def restart_as_admin():
    """Restart the script with administrator privileges"""
    script = sys.argv[0]
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, script, None, 1)

def run_powershell_command(command: str) -> None:
    """Execute a PowerShell command from Python without showing window"""
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    
    subprocess.run(["powershell", "-Command", command], 
                  startupinfo=startupinfo,
                  stdout=subprocess.PIPE,
                  stderr=subprocess.PIPE,
                  check=True)

def remove_bloatware_apps(apps_to_remove: List[str], progress_var, status_label) -> None:
    """Remove pre-installed Windows apps with progress feedback"""
    total_apps = len(apps_to_remove)
    for i, app in enumerate(apps_to_remove, 1):
        try:
            # Update progress and status
            progress_var.set((i / total_apps) * 100)
            status_label.config(text=f"Removing: {app}...")
            status_label.update()
            
            # Remove the app
            run_powershell_command(f"Get-AppxPackage *{app}* | Remove-AppxPackage -ErrorAction SilentlyContinue")
            run_powershell_command(f"Get-AppxPackage -Name *{app}* -AllUsers | Remove-AppxPackage -ErrorAction SilentlyContinue")
            run_powershell_command(f'Get-AppxProvisionedPackage -Online | Where-Object DisplayName -Like "*{app}*" | Remove-AppxProvisionedPackage -Online -ErrorAction SilentlyContinue')
            
        except subprocess.CalledProcessError as e:
            print(f"Failed to remove {app}: {e}")

def create_gui():
    """Create the main GUI window with progress bar"""
    root = tk.Tk()
    root.title("Windows Debloater")
    root.geometry("500x350")
    root.resizable(False, False)

    # Style configuration
    bg_color = "#000000"
    button_color = "#545454"
    text_color = "white"
    
    root.configure(bg=bg_color)

    # Title label
    tk.Label(root, text="Windows Debloater", font=("Arial", 16, "bold"), 
             bg=bg_color, fg=text_color).pack(pady=10)

    # Info label
    tk.Label(root, 
             text="This tool will remove bloatware apps and optimize Windows settings",
             bg=bg_color, fg=text_color).pack(pady=5)

    # Status label
    status_label = tk.Label(root, text="Ready to begin...", 
                           bg=bg_color, fg="yellow", font=("Arial", 10))
    status_label.pack(pady=10)

    # Progress bar
    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, 
                                 length=400, mode='determinate')
    progress_bar.pack(pady=20)

    # Run button
    run_btn = tk.Button(root, text="Run Debloater", 
                        command=lambda: run_debloater(root, progress_var, status_label),
                        bg=button_color, fg=text_color, width=20,
                        font=("Arial", 10, "bold"))
    run_btn.pack(pady=10)

    # Exit button
    tk.Button(root, text="Exit", command=root.destroy,
              bg=button_color, fg=text_color, width=20,
              font=("Arial", 10)).pack()

    return root, progress_var, status_label

def run_debloater(root, progress_var, status_label):
    """Execute the debloating process with progress feedback"""
    bloatware_apps = [
        "BingWeather", "GetHelp", "Getstarted", "Messaging",
        "Microsoft3DViewer", "MicrosoftOfficeHub", "MicrosoftSolitaireCollection",
        "MixedReality.Portal", "Office.OneNote", "OneConnect", "People",
        "Print3D", "SkypeApp", "Wallet", "WindowsAlarms",
        "windowscommunicationsapps", "WindowsFeedbackHub", "WindowsMaps",
        "WindowsSoundRecorder", "XboxApp", "XboxGameOverlay",
        "XboxGamingOverlay", "XboxIdentityProvider", "XboxSpeechToTextOverlay",
        "YourPhone", "ZuneMusic", "ZuneVideo"
    ]

    try:
        remove_bloatware_apps(bloatware_apps, progress_var, status_label)
        messagebox.showinfo("Success", "Debloating completed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
    finally:
        root.destroy()

def main():
    if not is_admin():
        # Create a simple GUI to request admin privileges
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        response = messagebox.askyesno(
            "Admin Privileges Required",
            "This program requires administrator privileges.\n"
            "Would you like to restart as administrator?",
            icon='warning')
        
        if response:
            restart_as_admin()
        sys.exit()
    else:
        # If already admin, show the main GUI
        root, progress_var, status_label = create_gui()
        root.mainloop()

if __name__ == "__main__":
    main()