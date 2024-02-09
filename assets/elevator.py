# elevator.py
import os
import platform
import shutil
import subprocess
import sys
import time

MAX_RETRIES = 100
RETRY_DELAY_SECONDS = 2


def retry_operation(func, *args, **kwargs):
    for _ in range(MAX_RETRIES):
        try:
            func(*args, **kwargs)
            return True
        except PermissionError as e:
            print(f"PermissionError: {e}")
            print("Retrying, please wait, don't close this window...")
            time.sleep(RETRY_DELAY_SECONDS)
    return False


def find_client_directory(current_dir):
    # Navigate up two levels to find the 'client' directory
    return os.path.abspath(os.path.join(current_dir, '..', '..'))


def find_tmp_directory(current_dir):
    # Navigate up two levels to find the 'client' directory
    return os.path.abspath(os.path.join(current_dir, '..'))


def delete_file_or_directory(path):
    if os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)


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
                retry_operation(delete_file_or_directory, entry_path)
                print(f"Deleted: {entry_path}")
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
            retry_operation(os.remove, dest_path)

        retry_operation(shutil.move, src_path, dest_path)


def relaunch_updated_launcher(arg_username):
    # Relaunch the updated launcher executable or JAR file with the provided username
    system = platform.system().lower()

    if system == 'windows':
        launcher_exe_path = os.path.join(os.getcwd(), 'launcher.exe')
        subprocess.Popen([launcher_exe_path, '--username', arg_username])
    elif system == 'darwin':
        launcher_jar_path = os.path.join(os.getcwd(), 'launcher.jar')
        subprocess.Popen(['java', '-jar', launcher_jar_path, '--username', arg_username])
    else:
        print("Unsupported platform.")
        sys.exit()

    # Exit the current instance of the launcher
    sys.exit()


if __name__ == '__main__':
    time.sleep(2)
    # Get the current directory of elevator.py
    current_directory = tmp_assets_directory = os.path.dirname(os.path.realpath(__file__))
    # Find the 'client' directory
    client_directory = find_client_directory(current_directory)
    tmp_directory = find_tmp_directory(current_directory)

    # Delete files in client except .sl_password and tmp/
    delete_specific_entries(client_directory)

    move_files(tmp_directory, client_directory)

    # Delete tmp directory
    tmp_directory = os.path.join(client_directory, 'tmp')
    retry_operation(shutil.rmtree, tmp_directory)

    # Get the username from command line arguments
    username = None
    if '--username' in sys.argv:
        username_index = sys.argv.index('--username')
        if username_index + 1 < len(sys.argv):
            username = sys.argv[username_index + 1]

    # Launch the launcher with the provided username
    relaunch_updated_launcher(username)

    # Exit the current instance
    sys.exit()