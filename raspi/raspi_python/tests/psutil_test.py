import os
import time
import psutil
import subprocess

# Function to terminate the initialize.py process
def kill_initialize_process():
    current_pid = os.getpid()
    # Get a list of all running processes
    for proc in psutil.process_iter(['pid', 'cmdline']):
        try:
            cmdline = proc.info.get('cmdline')
            if cmdline is not None and 'initialize.py' in cmdline and str(current_pid) not in cmdline:
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

# Function to restart initialize.py
def restart_initialize():
    # Terminate the existing initialize.py process
    kill_initialize_process()
    # Restart initialize.py
    subprocess.Popen(["python", "initialize.py"])

# Function to check if there are prints in the last 30 seconds
def check_prints(last_print_time):
    # Check if the last print was more than 30 seconds ago
    return (time.time() - last_print_time) >= 10

# Main function
def main():
    last_print_time = time.time()  # Initialize the last print time

    # Run initialize.py
    subprocess.Popen(["python", "initialize.py"])

    # Monitor prints in the console
    while True:
        # Check if there has been any print in the last 30 seconds
        if check_prints(last_print_time):
            print("No prints detected for 30 seconds. Restarting initialize.py...")
            restart_initialize()
            last_print_time = time.time()  # Reset the last print time

        # Wait for a short duration before checking again
        time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    main()
