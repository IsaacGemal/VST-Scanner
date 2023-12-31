import tkinter as tk
from tkinter import scrolledtext
import winreg

def enum_keys(hive, subkey):
    with winreg.OpenKey(hive, subkey) as key:
        i = 0
        while True:
            try:
                yield winreg.EnumKey(key, i)
                i += 1
            except OSError:
                break

def get_installed_programs():
    subkeys = [
        r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',
        r'SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall'
    ]
    roots = [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]
    installed_programs = set()

    for root in roots:
        for subkey in subkeys:
            try:
                for key_name in enum_keys(root, subkey):
                    with winreg.OpenKey(root, f"{subkey}\\{key_name}") as subkey_obj:
                        try:
                            program_name, _ = winreg.QueryValueEx(subkey_obj, "DisplayName")
                            installed_programs.add(program_name)
                        except OSError:
                            continue
            except FileNotFoundError:
                continue

    installed_programs_list = sorted(installed_programs)
    summary_text = "Installed Programs:\n" + "\n".join(f"- {prog}" for prog in installed_programs_list)
    return summary_text

def update_text():
    status_label.config(text="Scanning... Please wait.")
    installed_programs_summary = get_installed_programs()
    text_area.config(state=tk.NORMAL)
    text_area.delete('1.0', tk.END)
    text_area.insert(tk.INSERT, installed_programs_summary)
    text_area.config(state=tk.DISABLED)
    status_label.config(text="Scanning Complete.")

# Define colors
light_blue = '#D7EAF6'
dark_blue = '#1C5D99'
white = '#FFFFFF'

root = tk.Tk()
root.title("Installed Programs Scanner")
root.geometry('1280x720')

# Apply color scheme
root.configure(bg=light_blue)

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20, font=("Helvetica", 11), bg=white)
text_area.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
text_area.config(state=tk.DISABLED)

scan_button = tk.Button(root, text="Scan for Installed Programs", command=update_text, font=("Helvetica", 12), width=25, height=2, bg=dark_blue, fg=white)
scan_button.pack(pady=20)

status_label = tk.Label(root, text="", font=("Helvetica", 10), bg=light_blue, fg=dark_blue)
status_label.pack()

root.mainloop()
