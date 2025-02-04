import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import urllib as url
import urllib.request
import subprocess
import mutagen
import os

# NOTES
# ______________
#
# Still need to think of a better way to make the cookie check, the current
# implementation works but looks bad to maintain when more options get included. (resolving this in 0.0.3)

# 27/01/2025
# now I will need to duplicate the code for both the simple download and the
# save-to-file option, but the code looks better now

# ______________

# VARIABLES
# ______________

browser_cookie_check = False
browser_cookies = ""
file_path = ""
video_link = ""
metadata_check = False
subs_check = False

# SUBPROCESSES

    # mp3
def mp3_process():
    video_link = entry.get()
    subprocess.run(['./yt-dlp', '-x', '--audio-format', 'mp3', '--audio-quality', '0', video_link], check=True)
    
def mp3_metadata():
    video_link = entry.get()
    subprocess.run(['./yt-dlp', '-x', '--embed-metadata', '--embed-thumbnail', '--audio-format', 'mp3', '--audio-quality', '0', video_link], check=True)
    
def mp3_cookies():
    video_link = entry.get()
    subprocess.run(['./yt-dlp', '--cookies-from-browser', browser_cookies, '-x', '--audio-format', 'mp3', '--audio-quality', '0', video_link], check=True)    
    

    # flac
def flac_process():
    video_link = entry.get()
    subprocess.run(['./yt-dlp', '-x', '--audio-format', 'flac', '--audio-quality', '0', video_link], check=True)
    
def flac_metadata():
    video_link = entry.get()
    subprocess.run(['./yt-dlp', '-x', '--embed-metadata', '--embed-thumbnail', '--audio-format', 'flac', '--audio-quality', '0', video_link], check=True)
    
def flac_cookies():
    video_link = entry.get()
    subprocess.run(['./yt-dlp', '--cookies-from-browser', browser_cookies, '-x', '--audio-format', 'flac', '--audio-quality', '0', video_link], check=True)


    # mp4
def mp4_process():
    video_link = entry.get()
    subprocess.run(['./yt-dlp', '-S', 'ext:mp4:m4a', video_link], check=True)
    
def mp4_subs_process():
    video_link = entry.get()
    subprocess.run(['./yt-dlp', '-S', 'ext:mp4:m4a', '--all-subs' ,video_link], check=True)
    
def mp4_cookies_plus_subs():
    video_link = entry.get()
    subprocess.run(['./yt-dlp', '--cookies-from-browser', browser_cookies,'-S', 'ext:mp4:m4a', '--all-subs' ,video_link], check=True)

def mp4_cookies():
    video_link = entry.get()
    subprocess.run(['./yt-dlp', '--cookies-from-browser', browser_cookies, '-S', 'ext:mp4:m4a', video_link], check=True)


    # webm
def webm_process():
    video_link = entry.get()
    subprocess.run(['./yt-dlp', video_link], check=True)

def webm_cookies():
    video_link = entry.get()
    subprocess.run(['./yt-dlp', '--cookies-from-browser', browser_cookies, video_link], check=True)


# MAIN PROCESSES
# ______________

# yt-dlp binary manipulation

def download_bin(): # downloads the yt-dlp binary from Github
    try:
        url.request.urlretrieve('https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp', "yt-dlp")
        tk.messagebox.showinfo(message="yt-dlp binary has been downloaded.")
    
        # Specify the file  to make executable
        ytdlp_bin = 'yt-dlp'
        
        # Make the file executable
        subprocess.run(['chmod', '+x', ytdlp_bin], check=True)
        print(f"{ytdlp_bin} has been downloaded.")
        print(f"{ytdlp_bin} is now executable.")
        
    except subprocess.CalledProcessError as e:
        print(f"Error downloading yt-dlp: {e}")

def update_run(): # Run the yt-dlp -U command
    try:
        subprocess.run(['./yt-dlp', '-U'], check=True)
        print("yt-dlp updated successfully.")
        tk.messagebox.showinfo(message="yt-dlp is now updated to the latest stable.")
    except subprocess.CalledProcessError as e:
        print(f"Error running yt-dlp update: {e}")
        
# ---

# Simple Save - this can be used to save the audio/video in the same folder
# of the program.
def download():
    print (var_media.get())
    if var_media.get() == ".mp3":
        try:
            if browser_cookie_check == True:
                mp3_cookies()
            elif metadata_check == True:
                mp3_metadata()
            else:
                mp3_process()
            print(f"Downloading MP3 to {file_path}")
            print("Download done!")
            tk.messagebox.showinfo(message="MP3 download done!")

        except subprocess.CalledProcessError as e:
            print(f"Error downloading {video_link}: {e}")
            
    elif var_media.get() == ".flac":
            try:
                if browser_cookie_check == True:
                    flac_cookies()
                elif metadata_check == True:
                    flac_metadata()
                else:
                    flac_process()
                print((f"Downloading FLAC to {file_path}"))
                print("Download done!")
                tk.messagebox.showinfo(message="FLAC download done!")

            except subprocess.CalledProcessError as e:
                print(f"Error downloading {video_link}: {e}")
        
    elif var_media.get() == ".mp4":
        try:
            if browser_cookie_check == True:
                mp4_cookies()
            elif subs_check == True:
                mp4_subs_process()
            elif browser_cookie_check and subs_check == True:
                mp4_cookies_plus_subs()
            else:
                mp4_process()
            print((f"Downloading MP4 to {file_path}"))
            print("Download done!")
            tk.messagebox.showinfo(message="MP4 download done!")
        except subprocess.CalledProcessError as e:
            print(f"Error downloading {video_link}: {e}")
        
    elif var_media.get() == ".webm":
        try:
            if browser_cookie_check == True:
                webm_cookies()
            else:
                webm_process()
            print((f"Downloading standard WebM to {file_path}"))
            print("Download done!")
            tk.messagebox.showinfo(message="WebM download done!")
        except subprocess.CalledProcessError as e:
            print(f"Error downloading {video_link}: {e}")

# ---

# Save to file - this can be used to save the audio/video to a specified
# folder, and also bypass a error when trying to download Twitter videos
# that have a lot of caracthers on the tweet.

def save_to_file():
    global file_path, subs_check, browser_cookie_check, mp3_subprocess, mp4_subprocess, webm_subprocess, mp3_cookies, mp4_subs_process, mp4_cookies, webm_cookies
    if file_path == "":
        file_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP3 Audio", "*.mp3"),("FLAC Audio", "*.flac"),("MP4 Video", "*.mp4"), ("WebM", "*.webm"), ("All files", "*.*")])
        if file_path:  # Check if the user selected a file
            with open(file_path, 'w') as file:
                
                # Determine the default text based on the file extension
                
                if file_path.endswith('.mp3'):
                    try:
                        if browser_cookie_check == True:
                            mp3_cookies()
                        elif metadata_check == True:
                            mp3_metadata()
                        else:
                            mp3_process()
                        print(f"Downloading MP3 to {file_path}")
                        print("Download done!")
                        tk.messagebox.showinfo(message="MP3 download done!")
        
                    except subprocess.CalledProcessError as e:
                        print(f"Error downloading {video_link}: {e}")
                        
                elif file_path.endswith('.flac'):
                    try:
                        if browser_cookie_check == True:
                            flac_cookies()
                        elif metadata_check == True:
                            flac_metadata()
                        else:
                            flac_process()
                        print((f"Downloading FLAC to {file_path}"))
                        print("Download done!")
                        tk.messagebox.showinfo(message="FLAC download done!")
        
                    except subprocess.CalledProcessError as e:
                        print(f"Error downloading {video_link}: {e}")
                        
                        
                elif file_path.endswith('.mp4'):
                    try:
                        if browser_cookie_check == True:
                            mp4_cookies()
                        elif subs_check == True:
                            mp4_subs_process()
                        elif browser_cookie_check and subs_check == True:
                            mp4_cookies_plus_subs()
                        else:
                            mp4_process()
                        print((f"Downloading MP4 to {file_path}"))
                        print("Download done!")
                        tk.messagebox.showinfo(message="MP4 download done!")
                    except subprocess.CalledProcessError as e:
                        print(f"Error downloading {video_link}: {e}")
                
                elif file_path.endswith('.webm'):
                    try:
                        if browser_cookie_check == True:
                            webm_cookies()
                        else:
                            webm_process()
                        print((f"Downloading standard WebM to {file_path}"))
                        print("Download done!")
                        tk.messagebox.showinfo(message="WebM download done!")
                    except subprocess.CalledProcessError as e:
                        print(f"Error downloading {video_link}: {e}")
                
    else:
        messagebox.showinfo("Information", "No content to save.")
        
# ---

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
        
def clear_entry():  # Function to clear the entry field
    entry.delete(0, tk.END)

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
                                   "Version: 0.0.3 \n"
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

media_options = [".mp3", ".flac", ".mp4", ".webm"]
menu = tk.OptionMenu(root, var_media, *media_options)
menu.pack()

# Entry to submit the link
entry = tk.Entry(root, width=30)
entry.pack(pady=10)

# Main Download Button
main_download = tk.Button(root, text="Download!", command=download)
main_download.pack(pady=10)

# Button to clear the entry field
clear_button = tk.Button(root, text="Clear Entry", command=clear_entry)
clear_button.pack(pady=10)

#
separator2 = ttk.Separator(root, orient='horizontal')
separator2.pack(fill='x', padx=10, pady=10)

    # extra options
    
label = tk.Label(root, text="Extra Options")
label.pack()

# Save result to file button
save_button = tk.Button(root, text="Save file to...", command=save_to_file)
save_button.pack(pady=10)

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
