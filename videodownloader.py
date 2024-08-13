import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import yt_dlp as ytdlp

def progress_hook(d):
    if d['status'] == 'downloading':
        downloaded = d.get('downloaded_bytes', 0)
        total = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
        if total > 0:
            percent = int(downloaded * 100 / total)
            progress_bar['value'] = percent
            root.update_idletasks()

def download_video():
    video_url = url_entry.get()
    save_path = filedialog.askdirectory()

    if not video_url or not save_path:
        messagebox.showerror("Error", "enter the video URL AND the save location.")
        return

    ydl_opts = {
        'format': 'best',
        'outtmpl': f'{save_path}/%(title)s.%(ext)s',
        'progress_hooks': [progress_hook],
    }

    try:
        progress_bar['value'] = 0
        with ytdlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        messagebox.showinfo("Success", "Download complete!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download video: {e}")

root = tk.Tk()
root.title("Py Video Downloader")

#widgets
tk.Label(root, text="Enter Video URL:").grid(row=0, column=0, padx=10, pady=10)

url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)

download_button = tk.Button(root, text="Download", command=download_video)
download_button.grid(row=1, column=1, padx=10, pady=10, sticky="e")

progress_bar = ttk.Progressbar(root, length=400, mode='determinate')
progress_bar.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
