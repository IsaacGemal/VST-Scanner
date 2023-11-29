import os
import tkinter as tk
from collections import defaultdict
from tkinter import scrolledtext

# Function to scan VST directories and summarize the results
def scan_vsts():
    vst_directories = [
        "C:\\Program Files\\Common Files\\VST3",
        "C:\\Program Files (x86)\\Common Files\\VST3",
        "C:\\Program Files\\VSTPlugins",
        "C:\\Program Files\\Steinberg\\VstPlugins",
        "C:\\Program Files\\Common Files\\VST2",
        "C:\\Program Files\\Common Files\\Steinberg\\VST2",
        "C:\\Program Files (x86)\\Steinberg\\VstPlugins",
    ]

    third_party_vsts = defaultdict(list)
    total_files = 0
    total_folders = 0
    error_messages = ""
    summary_text = "3rd Party VSTs Installed:\n"

    for vst_directory in vst_directories:
        directory_text = ""
        if os.path.exists(vst_directory):
            directory_text += f"\nNow reading: {vst_directory}\n"
            try:
                for root, dirs, files in os.walk(vst_directory):
                    total_folders += 1
                    for file_name in files:
                        total_files += 1
                        if file_name.endswith(".dll") or file_name.endswith(".vst3"):
                            category = os.path.basename(root)
                            third_party_vsts[category].append(file_name)
            except Exception as e:
                error_messages += f"An error occurred while scanning {vst_directory}: {e}\n"
        else:
            error_messages += f"Directory does not exist: {vst_directory}\n"
        
        # Append the directory and the VSTs found there to summary_text
        if directory_text:
            summary_text += directory_text
            for category, vsts in third_party_vsts.items():
                summary_text += f"\n{category}:\n"
                for vst in vsts:
                    summary_text += f"  - {vst}\n"

    summary_text += "\nSummary:\n"
    summary_text += f"Total number of folders scanned: {total_folders}\n"
    summary_text += f"Total number of files scanned: {total_files}\n"
    summary_text += f"Total number of 3rd party VSTs found: {sum(len(vsts) for vsts in third_party_vsts.values())}\n"
    summary_text += "\nErrors:"
    summary_text += "\n" + error_messages

    return summary_text


# Function to update text in the GUI
def update_text():
    status_label.config(text="Scanning... Please wait.")
    summary = scan_vsts()
    text_area.config(state=tk.NORMAL)
    text_area.delete('1.0', tk.END)
    text_area.insert(tk.INSERT, summary)
    text_area.config(state=tk.DISABLED)
    status_label.config(text="Scanning Complete.")

# Setting up the GUI with a light blue color scheme
root = tk.Tk()
root.title("VST Scanner")
root.geometry('1280x720')  # Adjust the size of the window as needed

# Define colors
light_blue = '#D7EAF6'
dark_blue = '#1C5D99'
white = '#FFFFFF'

# Apply color scheme
root.configure(bg=light_blue)

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20, font=("Helvetica", 11), bg=white)
text_area.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
text_area.config(state=tk.DISABLED)

scan_button = tk.Button(root, text="Scan for VSTs", command=update_text, font=("Helvetica", 12), width=20, height=2, bg=dark_blue, fg=white)
scan_button.pack(pady=20)

status_label = tk.Label(root, text="", font=("Helvetica", 10), bg=light_blue, fg=dark_blue)
status_label.pack()

root.mainloop()