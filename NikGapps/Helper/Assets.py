from .Constants import Constants
from .FileOp import FileOp
import os.path
import platform


class Assets:
    assets_folder = os.path.join(os.getcwd(), 'NikGapps', 'Assets')
    cwd = assets_folder + Constants.dir_sep
    system_name = platform.system()
    if system_name == "Windows":
        aapt_path = os.path.join(assets_folder, 'bin', system_name, 'aapt_64.exe')
        adb_path = os.path.join(assets_folder, 'bin', system_name, 'adb.exe')
    elif system_name == "Linux":
        aapt_path = "adb"
        adb_path = "aapt"
    elif system_name == "Darwin":
        aapt_path = "/Users/runner/Library/Android/sdk/build-tools/30.0.0/aapt"
        adb_path = "adb"
    else:
        aapt_path = "adb"
        adb_path = "aapt"
    addon_path = cwd + "addon"
    header_path = cwd + "header"
    functions_path = cwd + "functions.sh"
    addon_sh_path = cwd + "addon.sh"
    busybox = cwd + "busybox"
    afzc_path = cwd + "afzc"
    file_sizes_path = cwd + "file_size.txt"
    ak3mount_path = cwd + "ak3mount"
    update_binary_busybox_path = cwd + "update-binary-busybox"
    update_script_path = cwd + "updater-script"
    nikgapps_config = cwd + "nikgapps.config"
    debloater_config = cwd + "debloater.config"
    installer_path = cwd + "installer"
    changelog = cwd + "changelogs.yaml"
    sign_jar = os.path.join(assets_folder, "NikGappsZipSigner.jar")

    @staticmethod
    def get_string_resource(file_path):
        return FileOp.read_string_file(file_path)

    @staticmethod
    def get_binary_resource(file_path):
        return FileOp.read_binary_file(file_path)
