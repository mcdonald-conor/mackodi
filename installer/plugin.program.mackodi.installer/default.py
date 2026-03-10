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

def json_rpc(method, params=None):
    payload = {
        'jsonrpc': '2.0',
        'id': 1,
        'method': method
    }
    if params is not None:
        payload['params'] = params
    try:
        response = xbmc.executeJSONRPC(json.dumps(payload))
        return json.loads(response)
    except Exception as e:
        log(f"JSON-RPC error for {method}: {e}")
        return None

def has_addon(addon_id):
    return xbmc.getCondVisibility(f'System.HasAddon({addon_id})')

def enable_addon(addon_id):
    result = json_rpc('Addons.SetAddonEnabled', {'addonid': addon_id, 'enabled': True})
    if not result or 'error' in result:
        log(f"Failed to enable addon {addon_id}: {result}")

def wait_for_addon(addon_id, timeout=120):
    if has_addon(addon_id):
        return True
    monitor = xbmc.Monitor()
    elapsed = 0
    while elapsed < timeout:
        if monitor.abortRequested():
            return False
        if has_addon(addon_id):
            return True
        xbmc.sleep(1000)
        elapsed += 1
    return False

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
            repo_id = repo_info.get('id')
            if repo_id:
                enable_addon(repo_id)
            log(f"Installed repo {repo_info['id']}")
            return True
        except Exception as e:
            log(f"Failed to unzip repo {filename}: {e}")
            return False
    return False

def install_addon(addon_id, timeout=120):
    if has_addon(addon_id):
        log(f"Addon {addon_id} already installed.")
        return True

    log(f"Attempting to install {addon_id}")
    xbmc.executebuiltin(f'InstallAddon({addon_id})')
    if wait_for_addon(addon_id, timeout=timeout):
        log(f"Addon {addon_id} installed.")
        return True
    log(f"Timed out installing {addon_id}")
    return False

def install_config_file(base_url, filepath):
    url = f"{base_url}{filepath}"
    filename = os.path.basename(filepath)
    # Special handling for splash.png location vs others
    if filename == 'splash.png':
        media_dir = os.path.join(USERDATA_PATH, 'media')
        if not os.path.exists(media_dir):
            os.makedirs(media_dir)
        dest = os.path.join(media_dir, 'Splash.png')
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

def addon_id_from_zip(filename):
    if '/' in filename:
        return filename.split('/')[0]
    return os.path.splitext(os.path.basename(filename))[0]

def show_post_install_dialog(failed_addons):
    steps = [
        "Real Debrid auth is per addon; repeat for each:",
        "1) Fen Light: Settings -> Accounts -> Real Debrid -> Authorize",
        "2) Umbrella: Settings -> Accounts -> Real Debrid -> Authorize",
        "3) YouTube: Sign in when prompted",
        "4) Force close Kodi to apply changes"
    ]
    if failed_addons:
        message = "Missing addons:\n" + "\n".join(failed_addons) + "\n\nNext steps:\n" + "\n".join(steps)
        xbmcgui.Dialog().ok("Complete (Action needed)", message)
    else:
        message = "Installation finished.\n\nNext steps:\n" + "\n".join(steps)
        xbmcgui.Dialog().ok("Complete", message)

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

    direct_addons = [addon_id_from_zip(z) for z in direct_zips]
    all_addons = []
    for repo in repos:
        if 'addons' in repo:
            all_addons.extend(repo['addons'])
    all_addons.extend(build_data.get('extra_addons', []))
    all_addons.extend(direct_addons)
    all_addons = list(dict.fromkeys(all_addons))
    
    failed_addons = []
    for i, addon in enumerate(all_addons):
        percent = 35 + int((i / max(1, len(all_addons))) * 20)
        pDialog.update(percent, f"Installing addon: {addon}...")
        if not install_addon(addon, timeout=180):
            failed_addons.append(addon)

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

    # 5. Switch to Mackodi skin
    skin_id = build_data.get('configuration', {}).get('skin', 'skin.mackodi')
    pDialog.update(95, f"Applying skin: {skin_id}...")
    if has_addon(skin_id) or wait_for_addon(skin_id, timeout=60):
        xbmc.executebuiltin(f'LoadSkin({skin_id})')
        xbmc.sleep(1000)
        xbmc.executebuiltin('Skin.SetBool(splash_enabled)')
    else:
        failed_addons.append(skin_id)

    pDialog.update(100, "Finalizing...")
    xbmc.sleep(1000)
    pDialog.close()
    
    show_post_install_dialog(failed_addons)

if __name__ == '__main__':
    run_installer()
