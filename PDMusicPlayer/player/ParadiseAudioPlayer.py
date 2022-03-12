from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from pygame import mixer
import os
import time
from tkinter import ttk
from ttkthemes import themed_tk as tk

#window creation, settings, themes, and menu
mixer.init()
root = tk.ThemedTk()
root.get_themes()
root.set_theme('plastik')

root.iconbitmap('icon.ico')
root.title('PD Audio Player')

menubar = Menu(root)
root.config(menu=menubar)

statusBar = Label(root, text='Welcome to PD Audio Player!', relief=SUNKEN, anchor=W, font='Times 12 italic', fg='red')   
statusBar.pack(side=BOTTOM, fill=X)

playlist = []

def open_file(): #opens the file
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)
    
def add_to_playlist(filename): #adds file to playlist
    filename = os.path.basename(filename)
    index = 0
    playListBox.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1
    
subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=subMenu)
subMenu.add_command(label='Open', command=open_file)
subMenu.add_command(label='Exit', command = root.destroy)

def about_us():
    tkinter.messagebox.showinfo('Information', "This program is a music player coded on Python. You may contact the developer on Instagram @paradoxial8172 or on Discord at 'Paradoxial#8172'")
def versions():
    tkinter.messagebox.showinfo('Versions', 'Your current build version is 1.0')
def have_a_bug():
    tkinter.messagebox.showinfo('Bugs & How to Report Them', 'Bugs are a very frustrating thing to have when using a software. Sadly though, bugs do occur, however, you can help fix them!. To report a bug, you can contact the developer (contact information is under the "about us" section)')

subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label='About Us', command=about_us)
subMenu.add_command(label='Versions', command=versions)
subMenu.add_command(label='Have a bug?', command=have_a_bug)

leftFrame = Frame(root)
leftFrame.pack(side=LEFT, padx=30)

playListBox = Listbox(leftFrame)
playListBox.pack()

addButton = ttk.Button(leftFrame, text='+ Add', command = open_file)
addButton.pack(side=LEFT)

def del_song(): #deletes song from playlist
    selected_song = playListBox.curselection()
    selected_song = int(selected_song[0])
    playListBox.delete(selected_song)
    playlist.pop(selected_song)     

delButton = ttk.Button(leftFrame, text='- Del', command = del_song)
delButton.pack(side=LEFT)

rightFrame = Frame(root)
rightFrame.pack(pady=30)

topFrame = Frame(rightFrame)
topFrame.pack()

caption = Label(topFrame, text="Welcome to PD Audio Player, let's play some tunes!", font='Arial 10 bold')
caption.pack()

lengthText = Label(topFrame, text='Total Length: --:--', font='Arial 8 bold',fg='red', relief=GROOVE)
lengthText.pack(pady=10)

#functions

def song_details(): #shows song length in 00:00
    sound = mixer.Sound(filename_path)
    total_length = sound.get_length()
    mins, secs = divmod(total_length, 60) #div - total_length/60 and - total_length%60
    mins = round(mins)
    secs = round(secs)
    timeFormat = '{:02d}:{:02d}'.format(mins, secs)
    lengthText['text'] = 'Total Length: ' + timeFormat

def play_song(): #plays file
    global paused
    if paused:
        mixer.music.unpause()
        statusBar['text'] = "Currently playing" + ' | ' + os.path.basename(filename_path)
        paused = FALSE
    else:
        try:
            selected_song = playListBox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusBar['text'] = "Currently playing" + ' | ' + os.path.basename(play_it)
            song_details()
        except:
            tkinter.messagebox.showerror('Error', 'The selected file you have chosen is not supported. :(')
                        
def stop_song(): #stops file
        mixer.music.stop()
        statusBar['text'] = "Song stopped."
        
paused = FALSE

def pause_song(): #pauses file
    global paused
    paused = TRUE            
    mixer.music.pause()
    statusBar['text'] = "Song paused."
    
def rewind_song(): #rewinds file
    play_song()
    statusBar['text'] = 'Song restarted' + " | " + os.path.basename(filename_path)

def set_volume(val): #sets the volume of audio
    volume = float(val)/100
    mixer.music.set_volume(volume)

muted = FALSE
    
def mute_volume():
    global muted
    if muted: #unmute music
        mixer.music.set_volume(0.7)
        volumeButton.configure(image=unmutePhoto)
        scale.set(70)
        muted = FALSE
    else: #mute music
        mixer.music.set_volume(0)
        volumeButton.configure(image=mutePhoto)
        scale.set(0)
        muted = TRUE
        
middleFrame = Frame(rightFrame, relief=RAISED, borderwidth=0)
middleFrame.pack(padx=10, pady=10)
 
playPhoto = PhotoImage(file='play.png')    
playButton = ttk.Button(middleFrame, image=playPhoto, command = play_song)
playButton.grid(row=0, column=0, padx=10)

pausePhoto = PhotoImage(file='pause.png')
pauseButton = ttk.Button(middleFrame, image=pausePhoto, command = pause_song)
pauseButton.grid(row=0, column=1, padx=10)

stopPhoto = PhotoImage(file='stop.png')
stopButton = ttk.Button(middleFrame, image=stopPhoto, command = stop_song)
stopButton.grid(row=0, column=2, padx=10)

bottomFrame = Frame(rightFrame, relief=RAISED, borderwidth=0)
bottomFrame.pack()

rewindPhoto = PhotoImage(file='rewind.png')
rewindButton = ttk.Button(bottomFrame, image=rewindPhoto, command=rewind_song)
rewindButton.grid(row=0, column=0)

mutePhoto = PhotoImage(file='mute.png')
unmutePhoto = PhotoImage(file='unmute.png')
volumeButton = ttk.Button(bottomFrame, image=unmutePhoto, command=mute_volume)
volumeButton.grid(row=0, column=1)

scale = ttk.Scale(bottomFrame, from_=0, to=100, orient = HORIZONTAL, command = set_volume)
scale.set(50)
mixer.music.set_volume(0.5)
scale.grid(row=0, column=2, pady=15, padx=30)

#events and bindings
def on_closing():
    stop_song()
    root.destroy()
    
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()