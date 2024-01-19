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


def delete_files_except_sl_password_and_tmp(directory):
    # Verify if the elevator.py file exists in the specified directory
    elevator_script_path = os.path.join(directory, 'tmp', 'assets', 'elevator.py')
    if not os.path.isfile(elevator_script_path):
        print(f"Error: elevator.py not found in {directory}")
        return

    # Change the working directory to the specified directory
    os.chdir(directory)

    # Iterate over files and subdirectories in the regular directory
    for entry in os.listdir(directory):
        entry_path = os.path.join(directory, entry)

        # Skip tmp directory and .sl_password file
        if entry == 'tmp' or entry == '.sl_password':
            continue

        try:
            if os.path.isfile(entry_path):
                os.remove(entry_path)
            elif os.path.isdir(entry_path):
                shutil.rmtree(entry_path)
        except PermissionError as e:
            print(f"PermissionError: {e} - Could not delete {entry_path}")


def move_files(src_directory, dest_directory):
    for filename in os.listdir(src_directory):
        src_path = os.path.join(src_directory, filename)
        dest_path = os.path.join(dest_directory, filename)
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
    time.sleep(3)
    # Get the current directory of elevator.py
    current_directory = tmp_assets_directory = os.path.dirname(os.path.realpath(__file__))
    # Find the 'client' directory
    client_directory = find_client_directory(current_directory)
    tmp_directory = find_tmp_directory(current_directory)

    # Delete files in client except .sl_password and tmp/
    delete_files_except_sl_password_and_tmp(client_directory)

    move_files(tmp_directory, client_directory)

    # Delete tmp directory
    tmp_directory = os.path.join(client_directory, 'tmp')
    shutil.rmtree(tmp_directory)

    # Launch the launcher
    relaunch_updated_launcher()

    # Exit the current instance
    sys.exit()
