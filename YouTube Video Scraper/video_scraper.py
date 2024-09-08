import yt_dlp
import tkinter as tk
from tkinter import simpledialog, filedialog
import threading

# Function to add colored messages to the text box
def add_message(text_widget, message, color_tag):
    text_widget.config(state=tk.NORMAL)
    text_widget.insert(tk.END, message + "\n", color_tag)
    text_widget.config(state=tk.DISABLED)
    text_widget.see(tk.END)

# Function to search and save song URLs
def search_and_save_song_urls(root, search_query, num_links, output_file, min_duration):
    ydl_opts = {
        'format': 'best/bestvideo+bestaudio',  # Choose the best available format
        'noplaylist': True,
        'cookiefile': r'C:/Users/India/OneDrive/Desktop/Python Automation/cookies.txt',  # Provide the cookies file for authentication
        'sleep_interval': 5,  # Sleep for 5 seconds between video downloads
        'max_sleep_interval': 10,  # Random sleep interval between 5 and 10 seconds
    }

    # List to store valid full-length URLs
    valid_urls = []

    try:
        # Initialize YT-DLP with options
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            page_number = 1
            while len(valid_urls) < num_links:
                # Perform YouTube search with pagination
                add_message(text_box, f"Searching for: {search_query} (Page {page_number})", "info")
                root.update()

                search_results = ydl.extract_info(f"ytsearch50:{search_query}", download=False)
                video_entries = search_results.get('entries', [])

                # Filter the videos based on duration and save valid URLs
                for video in video_entries:
                    video_url = video['webpage_url']
                    video_duration = video.get('duration', 0)

                    # Save only videos that meet the duration requirement (ignore short videos)
                    if video_duration >= min_duration:
                        valid_urls.append(video_url)
                        add_message(text_box, f"Saved URL: {video_url} (Duration: {video_duration}s)", "success")
                        root.update()

                    # Stop once we reach the desired number of links
                    if len(valid_urls) >= num_links:
                        break

                page_number += 1

            # Save valid URLs to a text file in parallel
            with open(output_file, 'w') as f:
                for url in valid_urls:
                    f.write(f"{url}\n")

        add_message(text_box, f"Saved {len(valid_urls)} full-length song URLs to {output_file}", "success")
        root.update()

    except yt_dlp.utils.DownloadError as e:
        add_message(text_box, f"Error: {str(e)}", "error")
        root.update()

# Function to start the search and save process in a new thread
def start_search_thread(root, search_query, num_links, output_file, min_duration):
    search_thread = threading.Thread(target=search_and_save_song_urls, args=(root, search_query, num_links, output_file, min_duration))
    search_thread.start()

def start_gui():
    global text_box, root
    root = tk.Tk()
    root.title("YouTube Full-Length Song URL Extractor")
    root.geometry("600x400")

    # Ask for a search query
    search_query = simpledialog.askstring("Search Query", "Enter a search query for YouTube songs:")

    # Ask for the number of full-length videos to extract URLs for (e.g., 20)
    num_links = simpledialog.askinteger("Number of Links", "Enter the number of full-length video URLs to extract:", minvalue=1, maxvalue=100)

    # Ask for the minimum duration for full-length songs (in seconds)
    min_duration = simpledialog.askinteger("Minimum Duration", "Enter the minimum duration for full-length songs (in seconds):", minvalue=60)

    # Ask for the output text file to save URLs
    output_file = filedialog.asksaveasfilename(title="Save URLs to File", defaultextension=".txt", filetypes=[("Text Files", "*.txt")])

    # Create a text box for displaying messages
    text_box = tk.Text(root, wrap=tk.WORD, height=15, state=tk.DISABLED, bg="black", fg="white")
    text_box.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    # Define color tags for different types of messages
    text_box.tag_configure("error", foreground="yellow")
    text_box.tag_configure("success", foreground="green")
    text_box.tag_configure("info", foreground="cyan")

    # Start searching and saving URLs in a separate thread
    start_search_thread(root, search_query, num_links, output_file, min_duration)
    
    root.mainloop()

if __name__ == "__main__":
    start_gui()