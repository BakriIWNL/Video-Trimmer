import datetime
import tkinter as tk
from tkinter import filedialog
from tkVideoPlayer import TkinterVideo
import os
import time
import subprocess

def create_buttons():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    folder_names = [name for name in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, name))]

    for folder_name in folder_names:
        button = tk.Button(button_frame, text=folder_name, command=lambda name=folder_name: handle_folder_button(name), width=20, height=5)
        button.pack(side=tk.LEFT,padx=10)

def handle_folder_button(folder_name):
    # Add your code to handle the button click for each folder here
    progress_value1 = progress_slider.get()
    progress_value2 = progress_slider2.get()
    if(progress_value2>progress_value1):
        dir_path = os.path.dirname(os.path.realpath(__file__))

        start_time = progress_value1
        end_time = progress_value2
        # Assuming the video is in the folder
        input_video_path = "\"" + mp4_files[idx] + "\""
        # Get the number of files in the folder_name directory
        folder_path = os.path.join(dir_path, folder_name)
        num_files = len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])
        output_video_path = "\"" + os.path.join(dir_path, folder_name, f"{folder_name}_{num_files+1}.mp4") + "\""

        command = f"ffmpeg -i {input_video_path} -ss {progress_value1} -to {progress_value2} -c copy {output_video_path}"
        subprocess.call(command, shell=True)
    else:
        pass
    
def update_duration(event):
    # updates the duration after finding the duration 
    duration = vid_player.video_info()["duration"]
    end_time["text"] = str(datetime.timedelta(seconds=duration))
    progress_slider["to"] = duration
    progress_slider2["to"] = duration

def update_scale(event):
    progress_slider.set(vid_player.current_duration())
    if progress_slider2.get() <= vid_player.current_duration():
        progress_slider2.set(vid_player.current_duration())


def load_video(video_path: str):
    # loads the video
    if video_path:
        vid_player.load(video_path)
        progress_slider.config(to=0, from_=0)
        play_pause()
        progress_slider.set(0)
        progress_slider2.set(0)

def load_folder():
    # loads the folder
    folder_path = filedialog.askdirectory()

    if folder_path:
        global mp4_files
        global idx
        mp4_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.mp4')]
        idx = 0
        load_video(mp4_files[idx])

def load_next_video():
    # loads the next video
    global idx
    play_pause()
    time.sleep(0.01) # avoid race condition
    if(idx+1 < len(mp4_files)):
        idx += 1
        load_video(mp4_files[idx])

def load_prev_video():
    # loads the previous video
    global idx
    play_pause()
    time.sleep(0.01) # avoid race condition
    if(idx-1 >=0):
        idx -= 1
        load_video(mp4_files[idx])

def seek(event=None):
    # used to seek a specific timeframe
    vid_player.seek(int(progress_slider.get()))


def skip(value: int):
    # skip seconds
    vid_player.seek(int(progress_slider.get())+value)
    progress_slider.set(progress_slider.get() + value)

def play_pause():
    # pauses and plays
    if vid_player.is_paused():
        vid_player.play()
        play_pause_btn["text"] = "Pause"

    else:
        vid_player.pause()
        play_pause_btn["text"] = "Play"


def video_ended(event):
    # handle video ended
    progress_slider.set(progress_slider["to"])
    play_pause_btn["text"] = "Play"
    progress_slider.set(0)
    progress_slider2.set(0)

root = tk.Tk()
root.state('zoomed')
root.title("Video Trimmer")

button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM)

create_buttons()

load_btn = tk.Button(root, text="Load", command=load_folder)
load_btn.pack()

vid_player = TkinterVideo(scaled=True, master=root)
vid_player.pack(expand=True, fill="both")

play_pause_btn = tk.Button(root, text="Play", command=play_pause)
play_pause_btn.pack()

skip_plus_5sec = tk.Button(root, text="Load previous video", command=lambda: load_prev_video())
skip_plus_5sec.pack(side="left")

start_time = tk.Label(root, text=str(datetime.timedelta(seconds=0)))
start_time.pack(side="left")

progress_slider = tk.Scale(root, from_=0, to=0, orient="horizontal")
progress_slider.bind("<ButtonRelease-1>", seek)
progress_slider.pack(side="left", fill="x", expand=True)

end_time = tk.Label(root, text=str(datetime.timedelta(seconds=0)))
end_time.pack(side="left")

progress_slider2 = tk.Scale(root, from_=0, to=0, orient="horizontal")
progress_slider2.pack(side="left", fill="x", expand=True)

vid_player.bind("<<Duration>>", update_duration)
vid_player.bind("<<SecondChanged>>", update_scale)
vid_player.bind("<<Ended>>", video_ended )

skip_plus_5sec = tk.Button(root, text="Load next video", command=lambda: load_next_video())
skip_plus_5sec.pack(side="left")

root.mainloop()