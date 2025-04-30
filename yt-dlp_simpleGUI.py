import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import urllib as url
import urllib.request
import subprocess
import mutagen
import os
import platform
import shlex

# ______________

# VARIABLES and CHECKS
# ______________

browser_cookie_check = False
metadata_check = False
subs_check = False
move_to_folder_check = False

browser_cookies = ""
file_path = ""
video_link = ""
file_name = ""
output_folder_pth = ""

ytdlp_bin = ""

system = platform.system() # check for OS and change the yt-dlp binary name accordingly
if system == "Linux":
    ytdlp_bin = "./yt-dlp"
elif system == "Windows":
    ytdlp_bin = "yt-dlp.exe"

download_combo = ""

## SETUP FOR DOWNLOAD PROCESS
# "COMBO" is what I call the combination of flags, each option is set to a variable that is added to the subprocess.run() in the end as a text input

def set_combo():
    global download_combo, var_media, video_link, browser_cookies, browser_cookie_check, metadata_check, subs_check, move_to_folder_check
    
    video_link = entry.get()
    video_link = (" ")+video_link #fix for the variable not getting a space before the shlex process
    
    mp3_flag = " -x --audio-format mp3 --audio-quality 0"
    flac_flag = " -x --audio-format flac --audio-quality 0"
    mp4_flag = " -S ext:mp4:m4a"

    metadata_flag = " --embed-metadata --embed-thumbnail"
    cookies_flag = " --cookies-from-browser "
    cookies_flag+= browser_cookies
    subs_flag = " --all-subs"

    output = " -P "
    output+= output_folder_pth
    longname = str(' -o "%(title).200s.%(ext)s"') # fix for downloading files with titles with more than 256 caracthers, in this implementation is better to always set this first no matter what

    download_combo = ytdlp_bin + longname
    
    # process for setting the "combo"
    try:
        if var_media.get() == ".mp3":
            try:
                if browser_cookie_check == True:
                    download_combo+= cookies_flag + mp3_flag  + video_link
                elif metadata_check == True:
                    download_combo+= metadata_flag + mp3_flag + video_link
                else:
                    download_combo+= mp3_flag + video_link
            except subprocess.CalledProcessError as e:
                print(f"Error downloading {video_link}: {e}")

        elif var_media.get() == ".flac":
            try:
                if browser_cookie_check == True:
                    download_combo+= cookies_flag + flac_flag + video_link
                elif metadata_check == True:
                    download_combo+= metadata_flag + flac_flag + video_link
                else:
                    download_combo+= flac_flag + video_link
            except subprocess.CalledProcessError as e:
                print(f"Error downloading {video_link}: {e}")

        elif var_media.get() == ".mp4":
            try:
                if browser_cookie_check == True:
                    download_combo+= cookies_flag + mp4_flag + video_link
                elif metadata_check == True:
                    download_combo+= metadata_flag + mp4_flag + video_link
                elif subs_check == True:
                    download_combo+= mp4_flag + subs_flag + video_link
                else:
                    download_combo += mp4_flag + video_link
            except subprocess.CalledProcessError as e:
                print(f"Error downloading {video_link}: {e}")
    finally:
        if move_to_folder_check == True:
            download_combo+= output
        print ("Combo done as: ", download_combo)

    args = shlex.split(download_combo)
    subprocess.Popen(args)
    p=subprocess.Popen(args)
    p.wait()

    print("Download done!")
    tk.messagebox.showinfo(message="Download done!")
    
# MAIN PROCESSES
# ______________

# yt-dlp binary manipulation

def download_bin(): # downloads the yt-dlp binary from Github
    if system == "Linux":
        try:
            url.request.urlretrieve('https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp', "yt-dlp")
            tk.messagebox.showinfo(message="yt-dlp binary has been downloaded.")
        
        # Make the file executable
            subprocess.run(['chmod', '+x', ytdlp_bin], check=True)
            print(f"{ytdlp_bin} has been downloaded.")
            print(f"{ytdlp_bin} is now executable.")
        
        except subprocess.CalledProcessError as e:
            print(f"Error downloading yt-dlp: {e}")

    elif system == "Windows":
        try:
            url.request.urlretrieve('https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe', "yt-dlp.exe")
            tk.messagebox.showinfo(message="yt-dlp.exe has been downloaded.")
        
        except subprocess.CalledProcessError as e:
            print(f"Error downloading yt-dlp: {e}")

def update_run(): # Run the yt-dlp -U command
    if system == "Linux":
        try:
            subprocess.run(['./yt-dlp', '-U'], check=True)
            print("yt-dlp updated successfully.")
            tk.messagebox.showinfo(message="yt-dlp is now updated to the latest stable.")
        except subprocess.CalledProcessError as e:
            print(f"Error running yt-dlp update: {e}")
    
    elif system == "Windows":
        try:
            subprocess.run(['yt-dlp.exe', '-U'], check=True)
            print("yt-dlp updated successfully.")
            tk.messagebox.showinfo(message="yt-dlp.exe is now updated to the latest stable.")
        except subprocess.CalledProcessError as e:
            print(f"Error running yt-dlp update: {e}")
        
# ---        

def choose_filename ():
    global file_name
    file_name = custom_entry.get()
    print (file_name)

def choose_path():
    global output_folder_pth, move_to_folder_check
    output_folder_pth = filedialog.askdirectory()
    move_to_folder_check = True
    if move_to_folder_check == True:
        print("Move to Folder set to: True ")

    # Split the input into components based on '/' 
    component_split = output_folder_pth.split('/')
    # Add quotes around components that contain spaces
    formatted_components = [f"'{component}'" if ' ' in component else component for component in component_split]
    # Join the components back together - so that the script finds the correct filepath
    formatted_path = '/'.join(formatted_components)
    output_folder_pth = formatted_path

    print ("Folder to download set to:",output_folder_pth)
    tk.messagebox.showinfo("Information", f"Folder set to: {output_folder_pth}")

# Common use specifications

def subs(): # set the flag to download subtitles with the video
    global subs_check
    print("Subtitles set to ",var_subs.get())
    if var_subs.get() == True:
        subs_check = True
        
def get_meta(): # set the flag to insert metadata in the file
    global metadata_check
    print("Get metadata set to ",var_metadata.get())
    if var_metadata.get() == True:
        metadata_check = True

# ---
        
def clear_entry():  # Function to clear the entry field and reset the "combo" process
    global download_combo
    entry.delete(0, tk.END)
    download_combo = ""


def submit_link():
    user_input = entry.get()  # Get the video link from the entry field
    print(f"You entered: {user_input}")
    #downloading_webm(user_input)
    
def insert_cookies_dialog(): # download with cookies-from-browser flag
    global browser_cookies, browser_cookie_check
    browser_input = simpledialog.askstring("Browser from cookies Input","Supported browsers are: brave, chrome, chromium, edge, firefox, opera, safari, vivaldi, whale. You must be logged in on the target website.")
    blank = ""
    if browser_input is blank:
        messagebox.showwarning("Warning", "No input provided!")
    else:
        messagebox.showinfo("Information", f"You entered: {browser_input}")
    browser_cookie_check = True
    browser_cookies = browser_input
    print ("Browser set to: ", browser_input)
        
# ---

def about_info():
    tk.messagebox.showinfo(title='About yt-dlp simpleGUI',
                           message="This is a simple GUI for yt-dlp. \n"
                                   ""
                                   "Credits to github.com/yt-dlp \n"
                                   "Logo by yt-dlp \n"
                                   ""
                                   "Version: 0.0.5 \n"
                                   "made by MxEmexis \n"
                                   "https://github.com/MxEmexis"
                           )
    

# GUI INTERFACE
# _____________

# Main window
root = tk.Tk()
root.title("yt-dlp simpleGUI")
root.geometry("350x820")

# banner
img = tk.PhotoImage(file="banner.png")
show_img = tk.Label(root, image=img)
show_img.pack(pady=20)

# yt-dlp binary management

# Button to download the yt-dlp binary from Github
dl_bin = tk.Button (root, text="Download yt-dlp", command=download_bin, activebackground='#404B56', activeforeground='white')
dl_bin.pack(pady=10) 

# Button to run the update command
update_button = tk.Button(root, text="Update yt-dlp", command=update_run, activebackground='#404B56', activeforeground='white')
update_button.pack(pady=10)

#
separator1 = tk.Frame(root, bg='#7F7F7F', height=2)
separator1.pack(fill=tk.X, pady=10)

# Drop-down menu to select file format (this saves in the same folder)
var_media = tk.StringVar()
var_media.set("Choose a media format...")

media_options = [".mp3", ".flac", ".mp4"]
menu = tk.OptionMenu(root, var_media, *media_options)
menu.configure(activebackground='#404B56', activeforeground='white')
menu.pack()

	# Entry to submit the link
entry_label = tk.Label(root, text="Insert URL:")
entry_label.pack(pady=10)

entry = tk.Entry(root, width=30, bd=5)
entry.pack(pady=10)

# Main Download Button
main_download = tk.Button(root, text="Download!", command=set_combo, bg='#32353B', activebackground='#404B56', fg='white', activeforeground='white')
main_download.pack(pady=10)

# Button to clear the entry field
clear_button = tk.Button(root, text="Clear Entry & Reset", command=clear_entry, activebackground='#404B56', activeforeground='white')
clear_button.pack(pady=10)

#
separator2 = tk.Frame(root, bg='#7F7F7F', height=2)
separator2.pack(fill=tk.X, pady=10)

    # extra options
    
label = tk.Label(root, text="Extra Options")
label.pack()

# Specify where to save button dialog
sav_button = tk.Button(root, text="Specify where to save...", command=choose_path, activebackground='#404B56', activeforeground='white')
sav_button.pack(pady=10)

# Save Subtitles button
var_subs = tk.BooleanVar()
check_subs = tk.Checkbutton(root, text="Get Subtitles (Video Only)", variable = var_subs ,command=subs, activebackground='#404B56', activeforeground='white')
check_subs.pack()

# Save metadata button
var_metadata = tk.BooleanVar()
check_metadata = tk.Checkbutton(root, text="Get metadata (Audio Only)", variable = var_metadata ,command=get_meta, activebackground='#404B56', activeforeground='white')
check_metadata.pack()

# Cookies-from-browser 
cookie_insert_button = tk.Button(root, text="Specify cookies from browser... \n (Age Restricted Content)", command = insert_cookies_dialog, activebackground='#404B56', activeforeground='white')
cookie_insert_button.pack(pady=10)

#
separator2 = tk.Frame(root, bg='#7F7F7F', height=2)
separator2.pack(fill=tk.X, pady=10)

# about button
about_button = tk.Button(root, text='about', command=about_info, height=1, fg='#999999', activeforeground='#B5B5B5')
about_button.pack(side='right', padx=5)

# Tkinter event loop
root.mainloop()
