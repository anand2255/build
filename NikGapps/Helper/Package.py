from pathlib import Path
from .Assets import Assets
from .XmlOp import XmlOp
from Config import TARGET_ANDROID_VERSION
from .Cmd import Cmd
from .Constants import Constants
from .FileOp import FileOp


class Package:
    def __init__(self, title, package_name, app_type, package_title=None):
        self.package_name = package_name
        self.title = title
        self.package_title = package_title
        if package_title is None:
            self.package_title = title
        self.app_type = app_type  # Whether the Package is system app or private app
        # target_folder is the folder where the package will be installed
        if app_type == Constants.is_priv_app:
            self.target_folder = str(Constants.system_root_dir + "/" + "priv-app" + "/" + title).replace("\\\\", "/")
        elif app_type == Constants.is_system_app:
            self.target_folder = str(Constants.system_root_dir + "/" + "app" + "/" + title).replace("\\\\", "/")
        self.install_list = []  # Stores list of files installed to the package directory
        self.predefined_file_list = []  # Stores list of predefined file list
        self.overlay_list = []  # Stores list of overlay apks
        self.framework_list = []  # Stores list of Framework files
        self.primary_app_location = None  # This will help generating priv-app whitelist permissions
        self.folder_dict = dict()  # Stores list of folders that needs 755 permissions
        self.file_dict = dict()  # Stores the file location on server as key and on device as value
        self.delete_files_list = []  # Stores the path of file to delete. Helpful for removing AOSP counterpart
        self.delete_rom_files_list = []  # Helpful for removing files in Roms with gapps
        self.priv_app_permissions = []  # Stores the priv-app whitelist permissions for the package
        self.enabled = 1
        self.validated = True
        self.additional_installer_script = ""
        self.failure_logs = ""

    def delete_in_rom(self, data):
        if not str(data).startswith("/"):
            if data not in self.delete_rom_files_list:
                self.delete_rom_files_list.append(data)
        else:
            if data not in self.delete_rom_files_list:
                self.delete_rom_files_list.append(data)

    def delete(self, data):
        if not str(data).startswith("/"):
            if data not in self.delete_files_list:
                self.delete_files_list.append(data)
        else:
            if data not in self.delete_files_list:
                self.delete_files_list.append(data)

    # this will generate the xml providing white-list permissions to the package
    def generate_priv_app_whitelist(self, app_set, permissions_list, pkg_path=None):
        for perm in self.priv_app_permissions:
            if perm not in permissions_list:
                permissions_list.append(perm)
        permissions_path = "/etc/permissions/" + str(self.package_name) + ".xml"
        import_path = Constants.get_import_path(app_set, self.package_title, permissions_path, pkg_path)
        self.file_dict[import_path] = "etc/permissions/" + str(self.package_name) + ".xml"
        XmlOp(self.package_name, permissions_list, import_path)

    def get_installer_script(self):
        lines = Assets.get_string_resource(Assets.installer_path)
        str_data = ""
        for line in lines:
            str_data += line

        str_data += "# Initialize the variables\n"
        str_data += "title=\"" + self.title + "\"\n"
        str_data += "package_title=\"" + self.package_title + "\"\n"
        if self.package_name is not None:
            str_data += "package_name=\"" + self.package_name + "\"\n"
        else:
            str_data += "package_name=\"\"" + "\n"
        str_data += "packagePath=install" + self.package_title + "Files\n"
        str_data += "deleteFilesPath=delete" + self.package_title + "Files\n"
        str_data += "deleteFilesFromRomPath=delete" + self.package_title + "FromRomFiles\n"
        str_data += "\n"
        str_data += f"remove_aosp_apps_from_rom=\"\n"
        for delete_folder in self.delete_files_list:
            str_data += f"{delete_folder}\n"
        str_data += "\"\n"
        str_data += "\n"
        str_data += f"remove_gapps_from_rom=\"\n"
        for delete_folder in self.delete_rom_files_list:
            str_data += f"{delete_folder}\n"
        str_data += "\"\n"
        str_data += "\n"
        str_data += f"file_list=\"\n"
        for file in self.file_dict:
            str_data += str(file)[str(file).find("___"):].replace("\\", "/") + "\n"
        str_data += "\"\n"
        str_data += "\n"
        str_data += "remove_existing_package() {\n"
        str_data += "   # remove the existing folder for clean install of " + self.package_title + "\n"
        str_data += "   delete_package \"" + self.title + "\"\n"
        # str_data += " # remove the data of package"
        # str_data += " delete_package_data \"" + self.package_name + "\"\n"
        str_data += "}\n"
        str_data += "\n"
        str_data += "remove_aosp_apps() {\n"
        str_data += "   # Delete the folders that we want to remove with installing " + self.package_title + "\n"
        str_data += "   for i in $remove_aosp_apps_from_rom; do\n"
        str_data += "       RemoveAospAppsFromRom \"$i\"\n"
        str_data += "   done\n"
        str_data += "}\n"
        str_data += "\n"
        str_data += "remove_gapps_from_rom() {\n"
        str_data += "   # Delete the folders that we want to remove with installing on Rom with Gapps\n"
        str_data += "   for i in $remove_gapps_from_rom; do\n"
        str_data += "       RemoveFromRomWithGapps \"$i\"\n"
        str_data += "   done\n"
        str_data += "}\n"
        str_data += "\n"
        str_data += "install_package() {\n"
        str_data += "   remove_existing_package\n"
        str_data += "   remove_aosp_apps\n"
        str_data += "   remove_gapps_from_rom\n"
        str_data += "   # Create folders and set the permissions\n"
        for folder in self.folder_dict:
            str_data += "   make_dir \"" + folder + "\"\n"
        str_data += "\n"
        str_data += "   # Copy the files and set the permissions\n"
        str_data += "   for i in $file_list; do\n"
        str_data += "       InstallFile \"$i\"\n"
        str_data += "   done\n"
        str_data += "\n"
        if not str(self.additional_installer_script).__eq__(""):
            str_data += self.additional_installer_script
            str_data += "\n"
        str_data += "   chmod 755 \"/tmp/AFZCScripts/addon\";\n"
        str_data += "   . /tmp/AFZCScripts/addon \"$OFD\" \"" + self.package_title + "\" \"/tmp/addon/$packagePath\"" \
                    + " \"/tmp/addon/$deleteFilesPath\"" + " \"\"" + " \"/tmp/addon/$deleteFilesFromRomPath\"\n"
        str_data += "   CopyFile \"$NikGappsAddonDir/" + self.package_title + ".sh\" \"$logDir/addonscripts/" + self.package_title + ".sh\"\n"
        str_data += "   CopyFile \"/tmp/addon/$packagePath\" \"$logDir/addonfiles/" + "$packagePath" + ".addon\"\n"
        str_data += "   rm -rf \"/tmp/addon/$packagePath\"\n"
        str_data += "   CopyFile \"/tmp/addon/$deleteFilesPath\" \"$logDir/addonfiles/" + "$deleteFilesPath" + ".addon\"\n"
        str_data += "   CopyFile \"/tmp/addon/$deleteFilesFromRomPath\" \"$logDir/addonfiles/" + "$deleteFilesFromRomPath" + ".addon\"\n"
        str_data += "   rm -rf \"/tmp/addon/$deleteFilesPath\"\n"
        str_data += "   rm -rf \"/tmp/addon/$deleteFilesFromRomPath\"\n"
        str_data += "}\n"
        str_data += "\n"
        str_data += "uninstall_package() {\n"
        str_data += "   # Remove the files when we're uninstalling NiKGapps\n"
        str_data += "   for i in $file_list; do\n"
        str_data += "       UninstallFile \"$i\"\n"
        str_data += "   done\n"
        str_data += "}\n"
        str_data += "\n"
        str_data += "find_install_mode\n"
        str_data += "\n"
        return str_data

    # pull the package and update the packages
    def pull_package_files(self, app_set=None):
        cmd = Cmd()
        self.failure_logs = ""
        if self.install_list.__len__() > 0 or self.predefined_file_list.__len__() > 0:
            for file in self.install_list:
                # Fetch the folder where the app files are located
                source_folder = str(Path(self.primary_app_location).parent).replace("\\", "/")
                # Replace the source folder with target so the data app becomes system app
                install_location = file.replace(source_folder, self.target_folder)
                # Replace the base.apk with System_App_Name.apk
                install_location = str(
                    install_location).replace("base.apk", Constants.get_base_name(self.target_folder) + ".apk")
                # Prepare the server directory where the pulled files will be stored
                source = install_location
                # Encrypt the file names and store it on server
                server_location = Constants.get_import_path(app_set, self.package_title, source)
                # Pull the file from device and store on server
                output_line = cmd.pull_package(file, server_location)
                if output_line.__len__() >= 1 and output_line[0].__contains__("1 file pulled"):
                    log = "File pulled " + str(file)
                # Update the folder dictionary
                for folder in FileOp.get_dir_list(install_location):
                    self.folder_dict[folder] = folder
                # Generate priv-app permissions whitelist
                if file == self.primary_app_location and self.app_type == Constants.is_priv_app:
                    output_line = cmd.get_white_list_permissions(server_location)
                    if output_line.__len__() >= 1 and not output_line[0].__contains__("Exception"):
                        self.generate_priv_app_whitelist(app_set, output_line)
                self.file_dict[server_location] = install_location
            for file in self.predefined_file_list:
                # in some cases the files are present in /product folder instead of /system
                # we will try to pull from both the folder and make sure one of them pulls correctly
                if cmd.file_exists("/system/product/" + file):
                    source = "/system/product/" + file
                elif cmd.file_exists("/system/" + file):
                    source = "/system/" + file
                else:
                    self.failure_logs += self.package_title + ": " + file + "\n"
                    print("The file " + file + " does not exists!")
                    continue
                import_path = source
                server_location = Constants.get_import_path(app_set, self.package_title, import_path)
                output_line = cmd.pull_package(source, server_location)
                if output_line.__len__() >= 1 and output_line[0].__contains__("1 file pulled"):
                    log = "File pulled " + str(file)
                # Update the folder dictionary
                for folder in FileOp.get_dir_list(Constants.get_base_name(server_location).replace("___", "/")):
                    self.folder_dict[folder] = folder
                self.file_dict[server_location] = source
        if self.delete_files_list.__len__() > 0:
            del_str = ""
            for delete_folder in self.delete_files_list:
                del_str += delete_folder + "\n"
            # if FileOp.dir_exists(Constants.path.join(Constants.export_directory, app_set, self.package_title)):
            #     FileOp.write_string_file(del_str, Constants.path.join(Constants.export_directory, app_set,
            #                                                           self.package_title, Constants.DELETE_FILES_NAME))

    # validate the package
    def validate(self):
        print("Validating " + self.package_title)
        self.failure_logs = ""
        cmd = Cmd()
        if self.package_name is not None:
            package_path = cmd.get_package_path(self.package_name)
            if package_path.__contains__("Exception occurred"):
                print("Package " + self.package_name + " not found!")
                self.failure_logs += self.package_title + ": " + "Package " + self.package_name + " not found!" + "\n"
                self.validated = False
                return
            if package_path.__len__() > 0:  # Iterate through all the files to get the parent directory
                parent_folder = None
                for file in package_path:  # Need to add more validation rules here
                    if file.startswith("/data/app/") and file.endswith("base.apk"):
                        path = Path(file)
                        parent_folder = path.parent
                        self.primary_app_location = file  # This will be used to fetch priv-app whitelist permissions
                        break
                    elif not file.__contains__("split_config") and file.startswith("/system") and file.endswith(".apk"):
                        path = Path(file)
                        parent_folder = path.parent
                        self.primary_app_location = file  # This will be used to fetch priv-app whitelist permissions
                        self.target_folder = str(path.parent).replace("\\", "/")
                        break
                if parent_folder is not None:  # Fetch the list of files to pull
                    self.install_list = cmd.get_package_files_recursively(parent_folder, self.install_list)
        else:
            if self.title != "ExtraFiles" and self.title != "ExtraFilesGo":
                self.validated = False
                print("Something wrong happened!")
