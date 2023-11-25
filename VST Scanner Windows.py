import os
from collections import defaultdict

# List of directories where VSTs might be installed
vst_directories = [
    "C:\\Program Files\\Common Files\\VST3",
    "C:\\Program Files (x86)\\Common Files\\VST3",
    "C:\\Program Files\\VSTPlugins",
    "C:\\Program Files\\Steinberg\\VstPlugins",
    "C:\\Program Files\\Common Files\\VST2",
    "C:\\Program Files\\Common Files\\Steinberg\\VST2",
    "C:\\Program Files (x86)\\Steinberg\\VstPlugins",
]

# Initialize a dictionary to hold the names of 3rd party VSTs, categorized by folder
third_party_vsts = defaultdict(list)

# Counters for summary
total_files = 0
total_folders = 0

# Open a text file to write the output
with open('vst_output.txt', 'w') as file:
    # Scan each directory for VST files
    for vst_directory in vst_directories:
        if os.path.exists(vst_directory):
            try:
                for root, dirs, files in os.walk(vst_directory):
                    total_folders += 1
                    for file_name in files:
                        total_files += 1
                        if file_name.endswith(".dll") or file_name.endswith(".vst3"):
                            category = os.path.basename(root)
                            third_party_vsts[category].append(file_name)
            except Exception as e:
                file.write(f"An error occurred while scanning {vst_directory}: {e}\n")
        else:
            file.write(f"Directory does not exist: {vst_directory}\n")

    # Output the list of VSTs, categorized by folder
    file.write("3rd Party VSTs Installed:\n")
    for category, vsts in third_party_vsts.items():
        file.write(f"\n{category}:\n")
        for vst in vsts:
            file.write(f"  - {vst}\n")

    # Output summary information
    file.write("\nSummary:\n")
    file.write(f"Total number of folders scanned: {total_folders}\n")
    file.write(f"Total number of files scanned: {total_files}\n")
    file.write(f"Total number of 3rd party VSTs found: {sum(len(vsts) for vsts in third_party_vsts.values())}\n")
