import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import urllib as url
import urllib.request
import subprocess
import os

# NOTES
# ______________
#
# Still need to think of a better way to make the cookie check, the current
# implementation works but looks bad to maintain when more options get included.

# ______________

# VARIABLES
# ______________

browser_cookie_check = False
browser_cookies = ""

# MAIN PROCESSES
# ______________

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
        
def clear_entry():  # Function to clear the entry field
    entry.delete(0, tk.END)  

def submit_link():
    user_input = entry.get()  # Get the video link from the entry field
    print(f"You entered: {user_input}")
    downloading_webm(user_input)
    
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
    
def downloading_mp3(video_link):  # Download audio as MP3 (best quality)
    try:
        if browser_cookie_check == True:
            subprocess.run(['./yt-dlp', '--cookies-from-browser', browser_cookies,'-x', '--audio-format', 'mp3', '--audio-quality', '0', video_link], check=True)
        else:
            subprocess.run(['./yt-dlp', '-x', '--audio-format', 'mp3', '--audio-quality', '0', video_link], check=True)
        print("Downloading audio (MP3)")
        print("Download done!")
        tk.messagebox.showinfo(message="MP3 download done!")
        
    except subprocess.CalledProcessError as e:
        print(f"Error downloading {video_link}: {e}")
        

def downloading_webm(video_link):  # Standard download (WebM)
    try:
        if browser_cookie_check == True:
            subprocess.run(['./yt-dlp', '--cookies-from-browser', browser_cookies, video_link], check=True)
        else:
            subprocess.run(['./yt-dlp', video_link], check=True)
        print("Downloading video (standard WebM)")
        print("Download done!")
        tk.messagebox.showinfo(message="WebM download done!")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading {video_link}: {e}")

def downloading_mp4(video_link):  # Download as MP4
    try:
        if browser_cookie_check == True:
            subprocess.run(['./yt-dlp', '--cookies-from-browser', browser_cookies, '-S', 'ext:mp4:m4a', video_link], check=True)
        else:
            subprocess.run(['./yt-dlp', '-S', 'ext:mp4:m4a', video_link], check=True)
        print("Downloading video (MP4)")
        print("Download done!")
        tk.messagebox.showinfo(message="MP4 download done!")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading {video_link}: {e}")
        
def downloading_mp4_subs(video_link):  # Download as MP4 + All Subs
    try:
        if browser_cookie_check == True:
            subprocess.run(['./yt-dlp', '--cookies-from-browser', browser_cookies, '-S', 'ext:mp4:m4a', '--all-subs', video_link], check=True)
        else:
            subprocess.run(['./yt-dlp', '-S', 'ext:mp4:m4a', '--all-subs', video_link], check=True)
        print("Downloading video (MP4 + Subtitles)")
        print("Download done!")
        tk.messagebox.showinfo(message="MP4 + Subtitles download done!")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading {video_link}: {e}")
        
def about_info():
    tk.messagebox.showinfo(title='About yt-dlp simpleGUI',
                           message="This is a simple GUI for yt-dlp. \n"
                                   ""
                                   "Credits to github.com/yt-dlp \n"
                                   ""
                                   "Version: 0.0.2 \n"
                                   "made by emexis \n"
                           )
    

# GUI INTERFACE
# _____________

# Main window
root = tk.Tk()
root.title("yt-dlp simpleGUI")

# Button to download the yt-dlp binary from Github
dl_bin = tk.Button (root, text="Download yt-dlp", command=download_bin)
dl_bin.pack(pady=10) 

# Button to run the update command
update_button = tk.Button(root, text="Update yt-dlp", command=update_run)
update_button.pack(pady=10)

#
separator = ttk.Separator(root, orient='horizontal')
separator.pack(fill='x', padx=10, pady=10)

# Button to clear the entry field
clear_button = tk.Button(root, text="Clear Entry", command=clear_entry)
clear_button.pack(pady=10)

# Entry to submit the link
entry = tk.Entry(root, width=30)
entry.pack(pady=10)

# Button to download audio (MP3)
mp3_button = tk.Button(root, text="Download Audio (MP3 - Best Quality)", command=lambda:downloading_mp3(entry.get()))
mp3_button.pack(pady=10)

# Button to download the video (WebM)
webm_button = tk.Button(root, text="Download Video (WebM)", command=submit_link)
webm_button.pack(pady=10)

# Button to download the video (MP4)
mp4_button = tk.Button(root, text="Download Video (MP4 - Best Quality)", command=lambda: downloading_mp4(entry.get()))
mp4_button.pack(pady=10)

# Button to download the video (MP4 + All subtitles)
mp4_subs_button = tk.Button(root, text="Download Video (MP4 + All Subtitles)", command=lambda: downloading_mp4_subs(entry.get()))
mp4_subs_button.pack(pady=10)

#
separator2 = ttk.Separator(root, orient='horizontal')
separator2.pack(fill='x', padx=10, pady=10)

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
