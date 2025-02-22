import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import urllib as url
import urllib.request
import subprocess
import mutagen
import os
import platform
import shlex


# NOTES
# ______________
#
# Still need to think of a better way to make the cookie check, the current
# implementation works but looks bad to maintain when more options get included. (resolving this in 0.0.3)

# 27/01/2025
# now I will need to duplicate the code for both the simple download and the
# save-to-file option, but the code looks better now

# 07/02/2025
# Solving a bug with the save-to-file feature, currently it downloads the file in the same folder as the program and creates a empty file on the target directory...bruh
# I think that it's best to make the user set the variable for the filepath and then make the output to the specified location

# 11/02/2025
# finally managed to make a better implementation of the download process that solves both issues, neat!

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

system = platform.system()
if system == "Linux":
    ytdlp_bin = "./yt-dlp"
elif system == "Windows":
    ytdlp_bin = "yt-dlp.exe"

download_combo = ""

# SETUP FOR DOWNLOAD PROCESS
# "COMBO" is what I call the combination of flags, each option is set to a variable that is added to the subprocess.run() in the end

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
                                   ""
                                   "Version: 0.0.4 \n"
                                   "made by emexis \n"
                           )
    

# GUI INTERFACE
# _____________

# Main window
root = tk.Tk()
root.title("yt-dlp simpleGUI")

# yt-dlp binary management

# Button to download the yt-dlp binary from Github
dl_bin = tk.Button (root, text="Download yt-dlp", command=download_bin)
dl_bin.pack(pady=10) 

# Button to run the update command
update_button = tk.Button(root, text="Update yt-dlp", command=update_run)
update_button.pack(pady=10)

#
separator = ttk.Separator(root, orient='horizontal')
separator.pack(fill='x', padx=10, pady=10)

# Drop-down menu to select file format (this saves in the same folder)
var_media = tk.StringVar()
var_media.set("Choose a media format...")

media_options = [".mp3", ".flac", ".mp4"]
menu = tk.OptionMenu(root, var_media, *media_options)
menu.pack()

# Entry to submit the link
entry_label = tk.Label(root, text="Insert URL:", fg="grey")
entry_label.pack(pady=10)

entry = tk.Entry(root, width=30)
entry.pack(pady=10)

# Main Download Button
main_download = tk.Button(root, text="Download!", command=set_combo)
main_download.pack(pady=10)

# Button to clear the entry field
clear_button = tk.Button(root, text="Clear Entry & Reset", command=clear_entry)
clear_button.pack(pady=10)

#
separator2 = ttk.Separator(root, orient='horizontal')
separator2.pack(fill='x', padx=10, pady=10)

    # extra options
    
label = tk.Label(root, text="Extra Options")
label.pack()

# Specify where to save button dialog
sav_button = tk.Button(root, text="Specify where to save...", command=choose_path)
sav_button.pack(pady=10)

# Save Subtitles button
var_subs = tk.BooleanVar()
check_subs = tk.Checkbutton(root, text="Get Subtitles (Video Only)", variable = var_subs ,command=subs)
check_subs.pack()

# Save metadata button
var_metadata = tk.BooleanVar()
check_metadata = tk.Checkbutton(root, text="Get metadata (Audio Only)", variable = var_metadata ,command=get_meta)
check_metadata.pack()

# Cookies-from-browser 
cookie_insert_button = tk.Button(root, text="Specify cookies from browser (Age Restricted Content)", command = insert_cookies_dialog)
cookie_insert_button.pack(pady=10)

#
separator3 = ttk.Separator(root, orient='horizontal')
separator3.pack(fill='x', padx=10, pady=10)

# about button
about_button = tk.Button(root, text='about', command=about_info)
about_button.pack(side='right', padx=10)

# Tkinter event loop
root.mainloop()
