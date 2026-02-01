import xbmc
import xbmcgui
import xbmcaddon
import xbmcvfs
import os
import json
import urllib.request
import zipfile
import shutil

ADDON = xbmcaddon.Addon()
ADDON_PATH = ADDON.getAddonInfo('path')
USERDATA_PATH = xbmcvfs.translatePath('special://userdata/')
ADDON_DATA_PATH = os.path.join(USERDATA_PATH, 'addon_data')
TEMP_PATH = xbmcvfs.translatePath('special://temp/')

# For local testing, we might want to change this, but for prod it's GitHub
# In this bundled version, we read local build.json
BUILD_FILE = os.path.join(ADDON_PATH, 'resources', 'build.json')

def log(msg):
    xbmc.log(f"[Mackodi Installer] {msg}", xbmc.LOGINFO)

def show_notification(header, message):
    xbmcgui.Dialog().notification(header, message, xbmcgui.NOTIFICATION_INFO, 5000)

def download_file(url, dest):
    try:
        log(f"Downloading {url} to {dest}")
        # Ensure temp directory exists
        if not os.path.exists(os.path.dirname(dest)):
            os.makedirs(os.path.dirname(dest))
            
        with urllib.request.urlopen(url) as response, open(dest, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        return True
    except Exception as e:
        log(f"Error downloading {url}: {e}")
        return False

def install_direct_zip(base_url, filename):
    url = f"{base_url}repo/zips/{filename}"
    zip_path = os.path.join(TEMP_PATH, filename)
    
    if download_file(url, zip_path):
        addons_path = xbmcvfs.translatePath('special://home/addons/')
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(addons_path)
            log(f"Installed direct zip {filename}")
            return True
        except Exception as e:
            log(f"Failed to unzip direct zip {filename}: {e}")
            return False
    return False

def install_repository(base_url, repo_info):
    filename = repo_info['filename']
    url = f"{base_url}repo/zips/{filename}"
    zip_path = os.path.join(TEMP_PATH, filename)
    
    if download_file(url, zip_path):
        # Extract to special://home/addons/
        addons_path = xbmcvfs.translatePath('special://home/addons/')
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(addons_path)
            log(f"Installed repo {repo_info['id']}")
            return True
        except Exception as e:
            log(f"Failed to unzip repo {filename}: {e}")
            return False
    return False

def install_addon(addon_id):
    if xbmc.getCondVisibility(f'System.HasAddon({addon_id})'):
        log(f"Addon {addon_id} already installed.")
        return True
    
    log(f"Attempting to install {addon_id}")
    xbmc.executebuiltin(f'InstallAddon({addon_id})')
    # We can't easily wait for completion in a script without complex monitoring
    # So we just trigger it and hope.
    return True

def install_config_file(base_url, filepath):
    url = f"{base_url}{filepath}"
    filename = os.path.basename(filepath)
    # Special handling for splash.png location vs others
    if filename == 'splash.png':
        dest = os.path.join(USERDATA_PATH, 'splash.png')
    else:
        dest = os.path.join(USERDATA_PATH, filename)
        
    return download_file(url, dest)

def install_addon_data(base_url, addon_id):
    # Expecting a zip file: userdata/addon_data/plugin.video.foo.zip
    zip_name = f"{addon_id}.zip"
    url = f"{base_url}userdata/addon_data/{zip_name}"
    dest_zip = os.path.join(TEMP_PATH, zip_name)
    
    if download_file(url, dest_zip):
        try:
            if not os.path.exists(ADDON_DATA_PATH):
                os.makedirs(ADDON_DATA_PATH)
            # Extract
            with zipfile.ZipFile(dest_zip, 'r') as zip_ref:
                zip_ref.extractall(ADDON_DATA_PATH)
            log(f"Restored data for {addon_id}")
            return True
        except Exception as e:
            log(f"Failed to extract data for {addon_id}: {e}")
            return False
    return False

def run_installer():
    if not os.path.exists(BUILD_FILE):
        log("build.json not found!")
        xbmcgui.Dialog().ok("Error", "build.json missing from installer!")
        return

    with open(BUILD_FILE, 'r') as f:
        build_data = json.load(f)

    if not xbmcgui.Dialog().yesno("Mackodi Installer", f"Install {build_data['name']} v{build_data['version']}?\nThis will overwrite your settings."):
        return

    # Setup progress
    pDialog = xbmcgui.DialogProgress()
    pDialog.create('Mackodi Installer', 'Initializing...')
    
    base_url = build_data['base_url']
    
    # 1. Install Repositories
    repos = build_data['repositories']
    for i, repo in enumerate(repos):
        pDialog.update(int((i / len(repos)) * 15), f"Installing {repo.get('id', 'Repo')}...")
        install_repository(base_url, repo)
        
    # 1b. Install Direct Zips (e.g. Fen Light)
    direct_zips = build_data.get('direct_zips', [])
    for i, zip_file in enumerate(direct_zips):
        pDialog.update(15 + int((i / len(direct_zips)) * 10), f"Installing {zip_file}...")
        install_direct_zip(base_url, zip_file)
    
    # Force Repo Update
    pDialog.update(25, "Updating Repositories...")
    xbmc.executebuiltin('UpdateLocalAddons')
    xbmc.executebuiltin('UpdateAddonRepos')
    xbmc.sleep(2000) 
    
    # 2. Trigger Addon Installs (Dependencies should now resolve)
    # This is async, so we just trigger them.
    all_addons = []
    for repo in repos:
        if 'addons' in repo:
            all_addons.extend(repo['addons'])
    
    for addon in all_addons:
        pDialog.update(35, f"Requesting install: {addon}...")
        install_addon(addon)

    # 3. Install Config Files
    files = build_data['configuration']['required_files']
    for f in files:
        pDialog.update(50, f"Installing {os.path.basename(f)}...")
        install_config_file(base_url, f)
        
    # 4. Install Addon Data
    data_folders = build_data['configuration']['addon_data']
    for i, folder in enumerate(data_folders):
        percent = 60 + int((i / len(data_folders)) * 30)
        pDialog.update(percent, f"Restoring settings: {folder}...")
        install_addon_data(base_url, folder)

    pDialog.update(100, "Finalizing...")
    xbmc.sleep(1000)
    pDialog.close()
    
    xbmcgui.Dialog().ok("Complete", "Installation finished.\nPLEASE FORCE CLOSE KODI NOW to apply changes.")

if __name__ == '__main__':
    run_installer()
