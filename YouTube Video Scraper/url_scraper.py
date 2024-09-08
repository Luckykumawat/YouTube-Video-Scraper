import yt_dlp
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os

# Function to add colored messages to the text box
def add_message(text_widget, message, color_tag):
    text_widget.config(state=tk.NORMAL)
    text_widget.insert(tk.END, message + "\n", color_tag)
    text_widget.config(state=tk.DISABLED)
    text_widget.see(tk.END)

# Function to download videos from URLs provided in a text file
def download_videos_from_file(root, base_folder, url_file, folder_name):
    # Ensure the file exists before proceeding
    if not url_file:
        add_message(text_box, "Error: No file selected. Please select a valid text file.", "error")
        return

    try:
        # Read URLs from the text file
        with open(url_file, 'r') as file:
            urls = [line.strip() for line in file.readlines()]

        if not urls:
            add_message(text_box, "Error: The file is empty. Please provide a file with URLs.", "error")
            return

        # Create a new folder for the downloads
        new_folder = os.path.join(base_folder, folder_name)
        os.makedirs(new_folder, exist_ok=True)

        ydl_opts = {
            'format': 'best',
            'outtmpl': f'{new_folder}/%(title)s.%(ext)s',
            'noplaylist': True,
            'postprocessors': [{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}],
        }

        # Initialize YT-DLP with options
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            downloaded_count = 0
            for url in urls:
                add_message(text_box, f"Downloading Video: {url}", "info")
                root.update()

                try:
                    # Download the video
                    ydl.download([url])
                    downloaded_count += 1
                    add_message(text_box, f"Downloaded: {url}", "success")
                    root.update()
                except Exception as e:
                    add_message(text_box, f"Failed to download {url}: {e}", "error")
                    root.update()

        add_message(text_box, f"Success: Downloaded {downloaded_count} videos to folder: {new_folder}", "success")
    
    except FileNotFoundError:
        add_message(text_box, "Error: File not found. Please check the file path and try again.", "error")
    except Exception as e:
        add_message(text_box, f"An error occurred: {str(e)}", "error")

def start_gui():
    global text_box, root
    root = tk.Tk()
    root.title("URL Video Downloader")
    root.geometry("600x400")
    root.configure(bg="black")  # Set the background color to black

    # Ask for base download folder
    base_folder = filedialog.askdirectory(title="Select Base Folder to Save Videos")

    # Ensure a valid folder is selected
    if not base_folder:
        messagebox.showerror("Error", "No folder selected. Please select a valid base folder.")
        return

    # Ask for folder name manually
    folder_name = simpledialog.askstring("Folder Name", "Enter the name for the new folder to save the videos:")

    # Ensure a valid folder name is entered
    if not folder_name:
        messagebox.showerror("Error", "No folder name provided. Please enter a valid folder name.")
        return

    # Ask for the text file containing video URLs
    url_file = filedialog.askopenfilename(title="Select Text File with URLs", filetypes=[("Text Files", "*.txt")])

    # Create a text box for displaying messages
    text_box = tk.Text(root, wrap=tk.WORD, height=15, state=tk.DISABLED, bg="black", fg="white")
    text_box.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    # Define color tags for different types of messages
    text_box.tag_configure("error", foreground="yellow")
    text_box.tag_configure("success", foreground="green")
    text_box.tag_configure("info", foreground="cyan")

    # Start downloading videos from the URLs in the text file
    download_videos_from_file(root, base_folder, url_file, folder_name)
    
    root.mainloop()

if __name__ == "__main__":
    start_gui()
