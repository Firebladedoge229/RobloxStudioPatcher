import os
import re
import json
import requests

# Load configuration from robloxstudiopatcherconfig.json
config_file_path = "robloxstudiopatcherconfig.json"
with open(config_file_path, 'r') as config_file:
    config = json.load(config_file)

optimize_roblox = config.get("optimize_roblox", False)
menu_type = config.get("menu_type", "Version 4")
topbar_type = config.get("topbar_type", "New")
msaa_level = config.get("msaa_level", "4x")
graphics_type = config.get("graphics_type", "21")
max_fps = config.get("max_fps", "9999")
log_requests = config.get("log_requests", False)
enable_proxy = config.get("enable_proxy", False)
enable_internal = config.get("enable_internal", True)
show_flags = config.get("show_flags", False)
log_all = config.get("log_all", False)
code_assist = config.get("code_assist", False)
disable_telemetry = config.get("disable_telemetry", True)
rainbow_ui = config.get("rainbow_ui", False)
rainbow_ui = config.get("force_high_graphics", True)

# Define the experimental features or optimizations to enable
flags = {
    "FFlagDebugGraphicsPreferD3D11": "true",  # directx 11 usage
    "DFIntTaskSchedulerTargetFps": int(max_fps)  # max fps
}

if menu_type == "Version 1":
    flags["FFlagDisableNewIGMinDUA"] = "true" # disable version 2 menu 
    flags["FFlagEnableInGameMenuControls"] = "false" # version 4 menu
    flags["FFlagEnableMenuControlsABTest"] = "false" # ab test
    flags["FFlagEnableMenuModernizationABTest"] = "false" # ab test
    flags["FFlagEnableMenuModernizationABTest2"] = "false" # ab test
    flags["FFlagEnableV3MenuABTest3"] = "false" # ab test
elif menu_type == "Version 2":
    flags["FFlagDisableNewIGMinDUA"] = "false" # disable version 2 menu 
    flags["FFlagEnableInGameMenuControls"] = "false" # version 4 menu
    flags["FFlagEnableMenuControlsABTest"] = "false" # ab test
    flags["FFlagEnableMenuModernizationABTest"] = "false" # ab test
    flags["FFlagEnableMenuModernizationABTest2"] = "false" # ab test
    flags["FFlagEnableV3MenuABTest3"] = "false" # ab test
elif menu_type == "Version 4":
    flags["FFlagDisableNewIGMinDUA"] = "true" # disable version 2 menu 
    flags["FFlagEnableInGameMenuControls"] = "true" # version 4 menu
    flags["FFlagEnableMenuControlsABTest"] = "false" # ab test
    flags["FFlagEnableMenuModernizationABTest"] = "false" # ab test
    flags["FFlagEnableMenuModernizationABTest2"] = "false" # ab test
    flags["FFlagEnableV3MenuABTest3"] = "false" # ab test

if topbar_type == "Old":
    flags["FFlagEnableInGameMenuChrome"] = "false" # version 4 menu
elif topbar_type == "New":
    flags["FFlagEnableInGameMenuChrome"] = "true" # version 4 menu

if log_requests == True:
    flags["DFLogHttpTraceLight"] = 12
elif log_requests == "False":
    flags["DFLogHttpTraceLight"] = 6

if enable_proxy == True:
    flags["FFlagStudioReEnableNetworkProxy_Dev"] = "true" # proxy settings
    flags["DFFlagHideProxySettings"] = "false" # proxy settings
    flags["DFFlagDebugEnableHttpProxy"] = "true" # proxy settings"
elif enable_proxy == "False":
    flags["FFlagStudioReEnableNetworkProxy_Dev"] = "false" # proxy settings
    flags["DFFlagHideProxySettings"] = "true" # proxy settings
    flags["DFFlagDebugEnableHttpProxy"] = "false" # proxy settings"

if msaa_level == "1x":
    flags["DebugForceMSAASamples"] = 1 # msaa level
elif msaa_level == "2x":
    flags["DebugForceMSAASamples"] = 2 # msaa level
elif msaa_level == "4x":
    flags["DebugForceMSAASamples"] = 4 # msaa level
elif msaa_level == "8x":
    flags["DebugForceMSAASamples"] = 8 # msaa level

if graphics_type == "10":
    flags["FFlagFixGraphicsQuality"] = "false" # 21 levels
elif graphics_type == "21":
    flags["FFlagFixGraphicsQuality"] = "true" # 21 levels

if show_flags == True:
    flag_list = ""
    for flag in flags:
        flag_list += flag + ","
    flags["FStringDebugShowFlagState"] = flag_list[:-1]

if log_all == True:
    jsonData = requests.get("https://raw.githubusercontent.com/MaximumADHD/Roblox-FFlag-Tracker/main/PCStudioApp.json").json()
    for flag, value in jsonData.items():
        if flag.startswith("FLog") or flag.startswith("DFLog"):
            flags[flag] = 12

if code_assist == True:
    flags["FFlagRelatedScriptsCodeAssist"] = "true"
    flags["FFlagCodeAssistFeature"] = "true"
    flags["FFlagAICOChatBot"] = "true"

if disable_telemetry == True:
    response = requests.get("https://raw.githubusercontent.com/MaximumADHD/Roblox-Client-Tracker/roblox/FVariables.txt")
    if response.status_code == 200:
        telemetryFlags = re.findall(r'\[.*\]\s*(\w+Telemetry\w*)', response.text)
        for flag in telemetryFlags:
            flag_name = re.sub(r'\[.*\]\s*', '', flag)
            flags[flag_name] = "false"

if rainbow_ui == True:
    flags["FFlagDebugDisplayUnthemedInstances"] = "true"

if force_high_graphics == True:
    flags["DFFlagDisableDPIScale"] = "true"
    flags["FIntTextureCompositorLowResFactor"] = 4
    flags["DFFlagEnableRequestAsyncCompression"] = "false"

# Specify the path to the Roblox version directory
versions_dir = os.path.join(os.environ['LOCALAPPDATA'], 'Roblox', 'Versions')

# Initialize variables to keep track of the version with the most files and folders
max_files_count = 0
selected_version = None

# Iterate through all the directories in the versions directory
for version in os.listdir(versions_dir):
    version_dir = os.path.join(versions_dir, version)
    
    # Check if the version directory contains RobloxStudioBeta.exe
    exe_path = os.path.join(version_dir, 'RobloxStudioBeta.exe')
    if os.path.exists(exe_path):
        # Count the number of files and folders in the version directory
        num_files = len([name for name in os.listdir(version_dir)])
        
        # Update if this version has more files/folders than the previous maximum
        if num_files > max_files_count:
            max_files_count = num_files
            selected_version = version_dir

# Check if a version with RobloxStudioBeta.exe was found
if selected_version is not None:
    # Construct the path to ClientAppSettings.json
    app_settings_path = os.path.join(selected_version, 'ClientSettings', 'ClientAppSettings.json')
    
    # Create the ClientSettings directory if it doesn't exist
    if not os.path.exists(os.path.join(selected_version, 'ClientSettings')):
        os.makedirs(os.path.join(selected_version, 'ClientSettings'))
    
    open(app_settings_path, "w").close()
    open(app_settings_path, "w+").write("{}")

    # Open the ClientAppSettings.json file and update the settings
    with open(app_settings_path, 'r+') as f:
        app_settings = json.load(f)
        if optimize_roblox == True:
            request = requests.get("https://web.archive.org/web/20231022202217if_/https://raw.githubusercontent.com/Kaiddd/Roblox-Client-Optimizer/8b892138f869092d545434e2769518dab399f89b/ClientAppSettings.json").json()
            for k, v in request.items():
                v = re.sub(r'https://web\.archive\.org/web/\d+/', "", v)
                app_settings[k] = v
        for k, v in flags.items():
            app_settings[k] = v
        f.seek(0)
        json.dump(app_settings, f, indent=4)
        f.truncate()
    
    # Open the RobloxStudioBeta.exe file and perform the hex patching
    if enable_internal == True:
        exe_path = os.path.join(selected_version, 'RobloxStudioBeta.exe')
        with open(exe_path, 'r+b') as f:
            content = f.read()
            index = content.find(b"\x00\x00\x00\x74\x05\xE8\xD0")
            while index != -1:
                f.seek(index)
                f.write(b"\x00\x00\x00\x90\x90\xE8\xD0")
                index = content.find(b"\x00\x00\x00\x74\x05\xE8\xD0", index + 1)
    elif enable_internal == False:
        exe_path = os.path.join(selected_version, 'RobloxStudioBeta.exe')
        with open(exe_path, 'r+b') as f:
            content = f.read()
            index = content.find(b"\x00\x00\x00\x90\x90\xE8\xD0")
            while index != -1:
                f.seek(index)
                f.write(b"\x00\x00\x00\x74\x05\xE8\xD0")
                index = content.find(b"\x00\x00\x00\x90\x90\xE8\xD0", index + 1)
    
else:
    print("No version with RobloxStudioBeta.exe found.")
