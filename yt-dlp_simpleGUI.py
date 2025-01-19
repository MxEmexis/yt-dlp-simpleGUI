import tkinter as tk
from tkinter import ttk, messagebox
import subprocess

def download_bin(): # downloads the yt-dlp binary from Github
    try:
        subprocess.run(['wget', 'https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp'], check=True)
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
        
def clear_entry():  # Function to clear the entry field
    entry.delete(0, tk.END)  

def submit_link():
    user_input = entry.get()  # Get the video link from the entry field
    print(f"You entered: {user_input}")
    downloading_webm(user_input)

def downloading_mp3(video_link):  # Download audio as MP3 (best quality)
    try:
        subprocess.run(['./yt-dlp', '-x', '--audio-format', 'mp3', '--audio-quality', '0', video_link], check=True)
        print("Downloading audio (MP3)")
        print("Download done!")
        tk.messagebox.showinfo(message="MP3 download done!")
        
    except subprocess.CalledProcessError as e:
        print(f"Error downloading {video_link}: {e}")
        

def downloading_webm(video_link):  # Standard download (WebM)
    try:
        subprocess.run(['./yt-dlp', video_link], check=True)
        print("Downloading video (standard WebM)")
        print("Download done!")
        tk.messagebox.showinfo(message="WebM download done!")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading {video_link}: {e}")

def downloading_mp4(video_link):  # Download as MP4
    try:
        subprocess.run(['./yt-dlp', '-S', 'ext:mp4:m4a', video_link], check=True)
        print("Downloading video (MP4)")
        print("Download done!")
        tk.messagebox.showinfo(message="MP4 download done!")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading {video_link}: {e}")
        
def downloading_mp4_subs(video_link):  # Download as MP4 + All Subs
    try:
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
                                   "Version: 0.1 \n"
                                   "made by emexis \n"
                           )
    

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

# about button
about_button = tk.Button(root, text='about', command=about_info)
about_button.pack(side='right', padx=10)

# Tkinter event loop
root.mainloop()
