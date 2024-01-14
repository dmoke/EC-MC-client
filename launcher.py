import os
import shutil
import subprocess
import sys
from subprocess import call
from sys import argv, exit

from PyQt5.QtCore import QThread, pyqtSignal, QSize, Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QSpacerItem, QSizePolicy, \
    QProgressBar, QPushButton, QApplication, QMainWindow
from minecraft_launcher_lib import forge
from minecraft_launcher_lib.command import get_minecraft_command
from minecraft_launcher_lib.forge import find_forge_version
from minecraft_launcher_lib.install import install_minecraft_version
from minecraft_launcher_lib.utils import get_minecraft_directory

minecraft_directory = get_minecraft_directory().replace('minecraft', 'EngineeringClubLauncher')
TITLE = "Engineering Club MC"
FORGE_VERSION_ID = '1.20'


def clear_and_move_mods(local_mods_dir):
    # Clear the existing mods directory
    mods_directory = os.path.join(minecraft_directory, 'mods')
    if os.path.exists(mods_directory):
        shutil.rmtree(mods_directory)

    # Create a new mods directory
    os.makedirs(mods_directory)

    # Move mods from the local mods directory to the Minecraft mods directory
    if os.path.exists(local_mods_dir):
        for mod_file in os.listdir(local_mods_dir):
            mod_path = os.path.join(local_mods_dir, mod_file)
            if os.path.isfile(mod_path) and mod_file.endswith('.jar'):
                shutil.copy(mod_path, mods_directory)


def create_minecraft_directory():
    # Create the Minecraft directory if it doesn't exist
    if not os.path.exists(minecraft_directory):
        os.makedirs(minecraft_directory)


def copy_servers():
    current_directory = os.getcwd()  # Get the current working directory
    local_servers_dat_path = os.path.join(current_directory, 'servers.dat')
    launcher_servers_dat_path = os.path.join(minecraft_directory, 'servers.dat')

    # Check if the file exists in the current directory
    if os.path.exists(local_servers_dat_path):
        shutil.copy(local_servers_dat_path, launcher_servers_dat_path)


class LaunchThread(QThread):
    launch_setup_signal = pyqtSignal(str, str)
    progress_update_signal = pyqtSignal(int, int, str)
    state_update_signal = pyqtSignal(bool)

    version_id = ''
    username = ''

    progress = 0
    progress_max = 0
    progress_label = ''

    def __init__(self):
        super().__init__()
        self.launch_setup_signal.connect(self.launch_setup)

    def install_forge(self, version_id):
        forge_version = find_forge_version(version_id)
        forge.install_forge_version(forge_version, minecraft_directory,
                                    callback={'setStatus': self.update_progress_label,
                                              'setProgress': self.update_progress, 'setMax': self.update_progress_max})

    def launch_setup(self, version_id, username):
        self.version_id = version_id
        self.username = username

    def update_progress_label(self, value):
        self.progress_label = value
        self.progress_update_signal.emit(self.progress, self.progress_max, self.progress_label)

    def update_progress(self, value):
        self.progress = value
        self.progress_update_signal.emit(self.progress, self.progress_max, self.progress_label)

    def installation_complete(self):
        pass

    def update_progress_max(self, value):
        self.progress_max = value
        self.progress_update_signal.emit(self.progress, self.progress_max, self.progress_label)

    def run(self):
        self.state_update_signal.emit(True)

        create_minecraft_directory()
        self.install_forge(FORGE_VERSION_ID)
        install_minecraft_version(versionid=self.version_id, minecraft_directory=minecraft_directory,
                                  callback={'setStatus': self.update_progress_label,
                                            'setProgress': self.update_progress, 'setMax': self.update_progress_max})

        clear_and_move_mods('mods')
        copy_servers()
        if self.username == '':
            pass

        options = {
            'username': self.username,
            'uuid': '',
            'token': ''
        }
        self.installation_complete()
        call(get_minecraft_command(version=self.version_id, minecraft_directory=minecraft_directory, options=options),
             creationflags=subprocess.CREATE_NO_WINDOW)

        self.state_update_signal.emit(False)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(TITLE + " Launcher")
        self.resize(300, 283)
        self.centralwidget = QWidget(self)
        self.logo = QLabel(self.centralwidget)
        self.logo.setMaximumSize(QSize(600, 350))
        self.logo.setText('')
        self.logo.setPixmap(QPixmap('assets/bg.png'))
        self.logo.setScaledContents(True)

        self.titlespacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.username = QLineEdit(self.centralwidget)
        self.username.setPlaceholderText('Username')

        self.progress_spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.start_progress_label = QLabel(self.centralwidget)
        self.start_progress_label.setText('')
        self.start_progress_label.setVisible(False)

        self.start_progress = QProgressBar(self.centralwidget)
        self.start_progress.setProperty('value', 24)
        self.start_progress.setVisible(False)

        self.start_button = QPushButton(self.centralwidget)
        self.start_button.setText('Play')
        self.start_button.clicked.connect(self.launch_game)

        self.vertical_layout = QVBoxLayout(self.centralwidget)
        self.vertical_layout.setContentsMargins(15, 15, 15, 15)
        self.vertical_layout.addWidget(self.logo, 0, Qt.AlignmentFlag.AlignHCenter)
        self.vertical_layout.addItem(self.titlespacer)
        self.vertical_layout.addWidget(self.username)
        self.vertical_layout.addItem(self.progress_spacer)
        self.vertical_layout.addWidget(
            self.start_progress_label)
        self.vertical_layout.addWidget(self.start_progress)
        self.vertical_layout.addWidget(self.start_button)

        self.launch_thread = LaunchThread()
        self.launch_thread.state_update_signal.connect(self.state_update)
        self.launch_thread.progress_update_signal.connect(self.update_progress)

        self.setCentralWidget(self.centralwidget)

        icon = QIcon("assets/icon.png")
        self.setWindowIcon(icon)

    def state_update(self, value):
        self.start_button.setDisabled(value)
        self.start_progress_label.setVisible(value)
        self.start_progress.setVisible(value)

    def update_progress(self, progress, max_progress, label):
        self.start_progress.setValue(progress)
        self.start_progress.setMaximum(max_progress)
        self.start_progress_label.setText(label)

    def launch_game(self, ):
        forge_version_id = "1.20-forge-46.0.14"

        self.start_progress_label.setText("Installing Forge...")
        # Start the launch thread after Forge installation
        self.launch_thread.launch_setup_signal.emit(forge_version_id, self.username.text())

        self.launch_thread.start()


if __name__ == '__main__':
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)

    app = QApplication(argv)
    window = MainWindow()
    window.resize(640, 480)
    window.show()

    exit(app.exec_())
