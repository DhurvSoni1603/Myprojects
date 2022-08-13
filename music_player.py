# This is an application works as a Music Player.
# Application features are:
# >  Allows to add songs to the playlist
# >  Allows to delete one or multiple song fro the playlist
# >  Allows to Play, Pause, Move to Next or Previous song, and to Stop.
# >  Allows to traverse through the song with a slider, also displays current time and song duration.
# >  Allows to manage the Volume with a slider.

# from imp import load_compiled

from tkinter import *
from turtle import title
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

base = Tk()
base.title('Music Player')
base.iconbitmap('E:/Dhruv/Python/GUI/')
base.geometry("650x450")

# Initialize Pygame Mixer

pygame.mixer.init()

# Grab song time info
def song_len():
    # Check for double timing
    if stopped:
        return
    # Grab the current song elapsed time
    curr_song = pygame.mixer.music.get_pos() / 1000
    # throw up temp label to get data
    # slider_label.config(text=f'Slider: {int(my_slider.get())} and Song pos: {int(curr_song)}')
    # convert time format
    converted_time = time.strftime('%M:%S', time.gmtime(curr_song))
    # Grab the song title from the playlist
    song = song_list.get(ACTIVE)
    # Add directory stucture and mp3 to song title 
    song = f'E:/Dhruv/songs/{song}.mp3'
    # Load song with mutagen
    song_mut = MP3(song)
    # Get song length
    global song_length
    song_length = song_mut.info.length
    # Convert to time format
    converted_len = time.strftime('%M:%S', time.gmtime(song_length))
    # Increase current time by 1 second
    curr_song+=1
    
    if int(my_slider.get()) == int(song_length):
        status_bar.config(text=f'Time Elapsed: {converted_len}  of  {converted_len}  ')
    elif paused:
        pass
    elif int(my_slider.get()) == int(curr_song):
        # update slider to position
        slider_pos = int(song_length)
        my_slider.config(to=slider_pos, value=int(curr_song))
    else:
        # update slider to position
        slider_pos = int(song_length)
        my_slider.config(to=slider_pos, value=int(my_slider.get()))
        # convert time format
        converted_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))
        # Output time to staus bar
        status_bar.config(text=f'Time Elapsed: {converted_time}  of  {converted_len}  ')
        # Move this thing along by 1 second
        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)

    # Output time to staus bar
    # status_bar.config(text=f'Time Elapsed: {converted_time}  of  {converted_len}  ')
    
    # Update slider value to current position value to current song position...  
    # my_slider.config(value=curr_song)
    
    # Upadate time
    status_bar.after(1000, song_len)
    
# add one song to playlist function
def add_one():
    song = filedialog.askopenfilename(initialdir='E:\Dhruv\songs',title='Choose a Song', filetypes=(("MP3 File", "*.mp3"), ))
    
    # Removes the directory and .mp3 extension from the song name
    song = song.replace('E:/Dhruv/songs/','')
    song = song.replace('.mp3','')
    
    # Add song to the list
    song_list.insert(END, song)
    
# add many songs to playlist function
def add_many():
    songs = filedialog.askopenfilenames(initialdir='E:\Dhruv\songs',title='Choose a Song', filetypes=(("MP3 File", "*.mp3"), ))
    
    # Loop through song list and replace directory info and mp3
    for song in songs:
        song = song.replace('E:/Dhruv/songs/','')
        song = song.replace('.mp3','')
        # Insert into playlist
        """ for i in song_list:
            if i != song:
                continue
            else:
                song_list.insert(END, song) """
        song_list.insert(END, song)
        
# Remove one song from the playlist
def remove_one():
    stop()
    # Delete currently selected song
    song_list.delete(ANCHOR)
    # Stop music if it's playing 
    pygame.mixer.music.stop()
    
# Remove all songs from the playlist
def remove_all():
    stop()
    # Delete all songs
    song_list.delete(0, END) 
    # Stop music if it's playing
    pygame.mixer.music.stop()

# Play the selected song
def play():
    global stopped
    stopped = False
    # Plays the selected song
    song = song_list.get(ACTIVE)
    song = f'E:/Dhruv/songs/{song}.mp3'
    # Loads and plays current song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    
    # Call the time function for song length
    song_len()
    
    # Update slider to position
    # slider_position = int(song_length)
    # my_slider.config(to=slider_position, value=0)

    current_volume = pygame.mixer.music.get_volume()
    # slider_label.config(text=current_volume * 100) 
    
# Stop playig song
global stopped
stopped = False
def stop():
    status_bar.config(text='')
    my_slider.config(value=0)
    # Stops  the current song
    pygame.mixer.music.stop()
    song_list.selection_clear(ACTIVE)
    
    # Set the stop varible to true
    global stopped
    stopped = True

# pause the playing button
global paused
paused = False

def pause(is_paused):

    global paused
    paused = is_paused
    if paused:
        # Unpause
        pygame.mixer.music.unpause()
        paused = False
    else:
        # Pause
        pygame.mixer.music.pause() 
        paused = True
        
#  move to next song in the playlist
def next():
    status_bar.config(text='')
    my_slider.config(value=0)
    # Get the current song tuple number
    next_one = song_list.curselection()
    # Add one to the current song number
    next_one = next_one[0]+1
    song = song_list.get(next_one)
    
    # Add directory structure and mp3 to song title
    song = f'E:/Dhruv/songs/{song}.mp3'
    # Play the selected song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    
    # Clear active bar in the playlist
    song_list.selection_clear(0, END)
    
    # Activate new song bar
    song_list.activate(next_one)
    
    # Set active bar to next song
    song_list.selection_set(next_one, last=None)  
    
# Play previous song in the playlist
def prev_song():
    status_bar.config(text='')
    my_slider.config(value=0)
    # Get the current song tuple number
    prev_one = song_list.curselection()
    # Add one to the current song number
    prev_one = prev_one[0]-1
    song = song_list.get(prev_one)
    
    # Add directory structure and mp3 to song title
    song = f'E:/Dhruv/songs/{song}.mp3'
    # Play the selected song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    
    # Clear active bar in the playlist
    song_list.selection_clear(0, END)
    
    # Activate new song bar
    song_list.activate(prev_one)
    
    # Set active bar to next song
    song_list.selection_set(prev_one, last=None)  
    
# Play current song in Loop
global clicked
clicked = True
global i
i = 0
def loop(is_looped):
    global clicked
    clicked = is_looped
    global i 
    i = 0
    # When the button is clicked once
    if clicked and i == 0:
        # looped = False
        Flag = 'y'
        while Flag == 'y':
            play()
            Flag = 'n'
            i = 1
            print("Song will play in loop")
    # When the button is clicked twice
    if clicked and i == 1:
        Flag = 'n'
        i = 0
        print("Song will exit from the loop")
            
        # Selects the current song in the playlist
    
# Create slider function
def slide(x):
    # slider_label.config(text=f'{int(my_slider.get())} of {int(song_length)}' )
    song = song_list.get(ACTIVE)
    song = f'E:/Dhruv/songs/{song}.mp3'
    # Loads and plays current song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(my_slider.get()))

# Create a volume slider function
def vol(x):
    pygame.mixer.music.set_volume(volume_slider.get())
    current_volume = pygame.mixer.music.get_volume()
    # slider_label.config(text=current_volume * 100) 
# Create Master frame
master_frame = Frame(base)
master_frame.pack(pady=20)

# Create a button switch mode
def switch():
    
    if play_btn['state'] == 'normal':
        play_btn['state'] = 'disable'
        pause_btn['state'] = 'normal'
    else:
        play_btn['state'] = 'normal'
        pause_btn['state'] = 'disable'

# Create playlist box
song_list = Listbox(master_frame, bg = 'black', fg = 'white', width=80, selectbackground= 'green', selectforeground= 'white')
song_list.grid(row=0, column=0)

# Define Player control button images
stop_btn_img = PhotoImage(file='C:/Users/Yatri/Desktop/stop1.png')
prev_btn_img = PhotoImage(file='C:/Users/Yatri/Desktop/previous1.png')
pause_btn_img = PhotoImage(file='C:/Users/Yatri/Desktop/pause1.png')
play_btn_img = PhotoImage(file='C:/Users/Yatri/Desktop/start2.png')
next_btn_img = PhotoImage(file='C:/Users/Yatri/Desktop/next1.png')
loop_btn_img = PhotoImage(file='C:/Users/Yatri/Desktop/loop11.png')

# Create Player control frames
song_control = Frame(master_frame)
song_control.grid(pady=20, row=1, column=0)

# Display message on hover to the button
class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = 0
        self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

# Create Player control Buttons
stop_btn = Button(song_control, image=stop_btn_img, borderwidth=0, command=stop)
prev_btn = Button(song_control, image=prev_btn_img, borderwidth=0, command=prev_song)
pause_btn = Button(song_control, image=pause_btn_img, borderwidth=0, command=lambda : pause(paused))
play_btn = Button(song_control, image=play_btn_img, borderwidth=0, command=play)
next_btn = Button(song_control, image=next_btn_img, borderwidth=0, command=next)
loop_btn = Button(song_control, image=loop_btn_img, borderwidth=0, command=lambda : loop(clicked))

stop_btn.grid(row=0, column=0, padx=10)
CreateToolTip(stop_btn, text='Stop')
prev_btn.grid(row=0, column=1, padx=10)
CreateToolTip(prev_btn, text='Previous Song')
play_btn.grid(row=0, column=2, padx=10)
CreateToolTip(play_btn, text='Play')
pause_btn.grid(row=0, column=3, padx=10)
CreateToolTip(pause_btn, text='Pause')
next_btn.grid(row=0, column=4, padx=10)
CreateToolTip(next_btn, text='Next Song')
loop_btn.grid(row=0, column=5, padx=10)
CreateToolTip(loop_btn, text='To play song in Loop')

# Create menu bar
menu_bar = Menu(base)
base.config(menu=menu_bar)

# Add song menu
add_song = Menu(menu_bar)
menu_bar.add_cascade(label='Add song', menu=add_song)
add_song.add_command(label='Add one song to playlist', command=add_one)

# Add many songs menu
add_song.add_command(label='Add many song to playlist', command=add_many)

# Create delete song menu
remove_song = Menu(menu_bar)
menu_bar.add_cascade(label='Remove Song', menu=remove_song)
remove_song.add_command(label='Delete a song from playlist', command=remove_one)
remove_song.add_command(label='Delete all songs from playlist', command=remove_all)

# Create Status Bar
status_bar = Label(base, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

# Clear the status bar
status_bar.config(text='')

# Create a Music slider
my_slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length= 360)
my_slider.grid(pady=10, row=2, column=0)

# Create a volume frame
volume_frame = LabelFrame(master_frame, text='Volume')
volume_frame.grid(row=0, column=1)
# Create Volume slider
volume_slider = ttk.Scale(volume_frame, from_=1, to_=0, orient=VERTICAL, value=1, command=vol, length=125)
volume_slider.pack(pady=10)

# Create temporary slider label
# slider_label = Label(base, text='0')
# slider_label.pack(pady=10)

base.mainloop()