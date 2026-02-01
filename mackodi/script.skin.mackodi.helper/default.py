import sys
import xbmc
import xbmcgui
import xbmcaddon

ADDON = xbmcaddon.Addon()

# Default add-on IDs (can be overridden via Skin.String)
DEFAULT_ADDONS = {
    'movies': {'primary': 'plugin.video.fenlight', 'backup': 'plugin.video.umbrella'},
    'tvshows': {'primary': 'plugin.video.fenlight', 'backup': 'plugin.video.umbrella'},
    'sport': {'primary': 'plugin.video.madtitansports', 'backup': 'plugin.video.theloop'},
    'youtube': {'primary': 'plugin.video.youtube', 'backup': None}
}

def log(msg):
    xbmc.log(f'[Mackodi Helper] {msg}', xbmc.LOGINFO)

def get_addon_id(section, use_backup=False):
    """Get add-on ID from skin settings or defaults"""
    primary_key = f'{section}_addon_primary'
    backup_key = f'{section}_addon_backup'
    
    if use_backup:
        # Check if backup is set in skin
        backup_id = xbmc.getInfoLabel(f'Skin.String({backup_key})')
        if backup_id:
            return backup_id
        # Return default backup
        return DEFAULT_ADDONS.get(section, {}).get('backup')
    else:
        # Check if primary is set in skin
        primary_id = xbmc.getInfoLabel(f'Skin.String({primary_key})')
        if primary_id:
            return primary_id
        # Return default primary
        return DEFAULT_ADDONS.get(section, {}).get('primary')

def addon_exists(addon_id):
    """Check if an add-on is installed"""
    if not addon_id:
        return False
    return xbmc.getCondVisibility(f'System.HasAddon({addon_id})')

def open_addon(addon_id, fallback_text=None):
    """Open an add-on with error handling"""
    if not addon_id:
        xbmcgui.Dialog().ok('Not Configured', 'No add-on configured for this section.')
        return False
    
    if not addon_exists(addon_id):
        message = fallback_text or 'This section isn\'t installed yet.'
        xbmcgui.Dialog().ok(
            'Not installed',
            message,
            'Enable Admin mode to install it.'
        )
        return False
    
    # Open the add-on (prefer ActivateWindow with plugin root)
    xbmc.executebuiltin(f'ActivateWindow(Videos,plugin://{addon_id}/,return)')
    xbmc.sleep(200)
    if not xbmc.getCondVisibility('Window.IsVisible(Videos)'):
        xbmc.executebuiltin(f'RunAddon({addon_id})')
    return True

def handle_open_addon(section, use_backup=False):
    """Handle opening an add-on with primary/backup logic"""
    log(f'Opening {section} (backup={use_backup})')
    
    addon_id = get_addon_id(section, use_backup)
    
    if not addon_id:
        xbmcgui.Dialog().ok('Not Configured', f'No {"backup " if use_backup else ""}add-on configured for {section}.')
        return
    
    if addon_exists(addon_id):
        open_addon(addon_id)
    else:
        open_addon(addon_id, 'This section isn\'t installed yet.')

def show_admin_menu():
    """Show admin menu"""
    options = [
        'Add-on Browser',
        'File Manager',
        'System Settings',
        'Skin Settings',
        'Show Installed Video Add-ons'
    ]
    
    dialog = xbmcgui.Dialog()
    selected = dialog.select('Admin Menu', options)
    
    if selected == 0:
        xbmc.executebuiltin('ActivateWindow(AddonBrowser)')
    elif selected == 1:
        xbmc.executebuiltin('ActivateWindow(FileManager)')
    elif selected == 2:
        xbmc.executebuiltin('ActivateWindow(Settings)')
    elif selected == 3:
        xbmc.executebuiltin('ActivateWindow(SkinSettings)')
    elif selected == 4:
        xbmc.executebuiltin('ActivateWindow(AddonBrowser,addons://user/category.video_addons,return)')

def parse_args(raw_args):
    """Parse action/section/backup from script args"""
    action = None
    section = None
    use_backup = False

    for arg in raw_args:
        if arg.startswith('action='):
            action = arg.split('=', 1)[1]
        elif arg.startswith('addon='):
            section = arg.split('=', 1)[1]
        elif arg == 'backup' or arg == 'use_backup':
            use_backup = True
        elif action is None:
            action = arg
        elif section is None:
            section = arg

    return action, section, use_backup

def main():
    """Main entry point"""
    raw_args = sys.argv[1:]
    if not raw_args:
        log('No arguments provided')
        return

    action, section, use_backup = parse_args(raw_args)

    if action == 'open_addon':
        if section:
            handle_open_addon(section, use_backup)
        else:
            log('No section provided for open_addon')
    elif action == 'admin':
        show_admin_menu()
    else:
        log(f'Unknown action: {action}')

if __name__ == '__main__':
    main()
