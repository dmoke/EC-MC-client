# elevator.py
import os
import platform
import shutil
import subprocess
import sys
import time


def find_client_directory(current_dir):
    # Navigate up two levels to find the 'client' directory
    return os.path.abspath(os.path.join(current_dir, '..', '..'))


def find_tmp_directory(current_dir):
    # Navigate up two levels to find the 'client' directory
    return os.path.abspath(os.path.join(current_dir, '..'))


def delete_specific_entries(directory):
    # Verify if the elevator.py file exists in the specified directory
    elevator_script_path = os.path.join(directory, 'tmp', 'assets', 'elevator.py')
    if not os.path.isfile(elevator_script_path):
        print(f"Error: elevator.py not found in {directory}")
        return

    try:
        # Change the working directory to the specified directory
        os.chdir(directory)

        # Entries to be deleted
        entries_to_delete = ['assets', 'config', 'logs', 'mods', 'shaderpacks', 'venv', 'launcher.exe', 'launcher.jar',
                             'launcher.py', 'requirements.txt', 'servers.dat']

        # Iterate over files and subdirectories in the regular directory
        for entry in entries_to_delete:
            entry_path = os.path.join(directory, entry)

            # Check if the file or directory exists before attempting to delete
            if os.path.exists(entry_path):
                try:
                    if os.path.isfile(entry_path):
                        os.remove(entry_path)
                    elif os.path.isdir(entry_path):
                        shutil.rmtree(entry_path)
                    print(f"Deleted: {entry_path}")
                except PermissionError as e:
                    print(f"PermissionError: {e} - Could not delete {entry_path}")
            else:
                print(f"Not found: {entry_path}")

    except Exception as e:
        print(f"An error occurred: {e}")


def move_files(src_directory, dest_directory):
    for filename in os.listdir(src_directory):
        src_path = os.path.join(src_directory, filename)
        dest_path = os.path.join(dest_directory, filename)

        # Check if the file already exists in the destination directory
        if os.path.exists(dest_path):
            # If it does, remove the existing file before moving
            os.remove(dest_path)

        # Move the file from source to destination
        shutil.move(src_path, dest_path)


def relaunch_updated_launcher():
    # Relaunch the updated launcher executable or JAR file
    system = platform.system().lower()

    if system == 'windows':
        launcher_exe_path = os.path.join(os.getcwd(), 'launcher.exe')
        subprocess.Popen([launcher_exe_path])
    elif system == 'darwin':
        launcher_jar_path = os.path.join(os.getcwd(), 'launcher.jar')
        subprocess.Popen(['java', '-jar', launcher_jar_path])
    else:
        print("Unsupported platform.")
        sys.exit()

    # Exit the current instance of the launcher
    sys.exit()


if __name__ == '__main__':
    time.sleep(1)
    # Get the current directory of elevator.py
    current_directory = tmp_assets_directory = os.path.dirname(os.path.realpath(__file__))
    # Find the 'client' directory
    client_directory = find_client_directory(current_directory)
    tmp_directory = find_tmp_directory(current_directory)

    # Delete files in client except .sl_password and tmp/
    delete_specific_entries(client_directory)

    # Add a delay before moving files
    time.sleep(1)  # Adjust the duration as needed

    move_files(tmp_directory, client_directory)

    # Delete tmp directory
    tmp_directory = os.path.join(client_directory, 'tmp')
    shutil.rmtree(tmp_directory)

    # Add a delay before relaunching
    time.sleep(1)  # Adjust the duration as needed

    # Launch the launcher
    relaunch_updated_launcher()

    # Exit the current instance
    sys.exit()