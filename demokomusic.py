# my first project
#January project

import tkinter
from tkinter import *
import os
import tkinter.messagebox
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import themed_tk as tk
from pygame import mixer
from mutagen.mp3 import MP3
import time
import threading






'''the root window and its settings'''


root = tk.ThemedTk()
root.get_themes() #to invoke the theme 
root.set_theme('equilux')# this is the theme used
root.title('koMusic Player') # title of our root window
root.config(bg = 'gray') # root background




'''The main menu bar and it's properties'''



def about():
    tkinter.messagebox.showinfo('About Us', 'This is koMusic player. An mp3 player built with python @ Komolehin Israel')
    

def browse():
    global filename
    filename = filedialog.askopenfilename(filetypes = [('All supported', '.mp3'), ('All files','*.*')])
    print(filename)

def destroy():
    stop()
    root.destroy()


menubar = Menu(root, bg = 'skyblue3')
root.config(menu = menubar)



submenu = Menu(menubar, tearoff = 0)
menubar.add_cascade(label = 'File', menu = submenu)

submenu.add_command(label = 'Open', command = browse)
submenu.add_command(label = 'Exit', command = destroy)

submenu = Menu(menubar, tearoff = 0)
menubar.add_cascade(label = 'Help', menu = submenu)
submenu.add_command(label = 'About Us', command= about)


submenu = Menu(menubar, tearoff = 0)
menubar.add_cascade(label = 'View', menu = submenu)

minimenu = Menu(submenu,tearoff = 0)
submenu.add_cascade(label = 'themes', menu = minimenu)



'''The display picture'''

logo_photo = PhotoImage(file = 'earphones.png')

logo_label = Label(root, image = logo_photo, relief = FLAT, bg = 'gray').grid(column = 0, row = 2)

'''The frame used to pack the buttons, the buttons are still below the code'''
frame2 = Frame(root, bg = 'gray', width = 500,height = 80)
frame2.place(x = 100, y = 650)


# status bar
global status
status = Label(root, text = 'Music player',relief = SUNKEN, anchor = W, bg = 'skyblue3', font = "Times 10 italic")
status.place(x = 800, y = 720)
    
#create frame for the playlist
playlist = []

playlistbox = Listbox(root, bg = 'gray', activestyle = 'none' , cursor = 'hand2', selectmode = EXTENDED, fg = 'lightgoldenrod', font = 'Times 10 roman')
playlistbox.place(relwidth = 0.3,relheight = 0.5, relx = 0.617, rely = 0.08 )

scrollbar = ttk.Scrollbar(playlistbox)# set the scroll bar in the listbox
scrollbar.pack(side = RIGHT, fill = Y)#the position of the scrollbar


#configure the play list scrollbar
playlistbox.config(yscrollcommand = scrollbar.set)
scrollbar.config(command = playlistbox.yview)


#playlist functions. this is the function to get the lists into our playlist
def get_playlist():
    global filename
    filename = filedialog.askopenfilename(filetypes = [('All supported', '.mp3'), ('All files','*.*')])
    fileBaseName = os.path.basename(filename)
    print(fileBaseName)
    index = 0
    playlistbox.insert(index,fileBaseName)#playlist box only contains the basename and we can't load basename without the full path
    playlist.insert(index,filename )#this will enable us to load the full path and to ensure that it is in sync with the playlistBox having same index
    index +=1


addplaylist = ttk.Button(root, text = '+ Add',cursor = 'hand2', command = get_playlist).place(x = 790, y = 425)


# initializing mixer

mixer.init()
global progressBar
progressBar = ttk.Progressbar(root, length = 1, mode = 'determinate') #.place(x = 45, y = 600)
#progressBar.grid(row = 13, columnspan = 10, sticky = 'ew', padx = 5, pady = 8 )
progressBar.place(x = 42, y = 622, width = 450)


#this is to configure the songs play
def music_details():
    global filename
    global song_length
    global timeformat
   
    try:
        music_data = os.path.splitext(play_song)
        music = MP3(play_song)
        
    except:
        music_data = os.path.splitext(filename)
        music = MP3(filename)
    song_length = music.info.length

    mins,secs = divmod(song_length,60)
    
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    time_label = Label(root, text = 'Total Length ' + ': ' + timeformat, font = 'Times 10 roman', bg = 'grey',fg = 'lightgoldenrod').place(x = 800, y = 680)

    timedown = threading.Thread(target = time_countdown,args =(song_length,))
    timeup = threading.Thread(target = time_countup,args =(song_length,))
    timedown.start()
    timeup.start()

    
#count down of the songs
count_down = Label(root, text = '--:--',bg = 'gray', font = 'Times 10 roman')
count_down.place(x = 495, y = 617)

#count down function
def time_countdown(Time):
    global paused
    while Time and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins,secs = divmod(Time,60)
            mins = round(mins)
            secs = round(secs)
            timeformat1 = '{:02d}:{:02d}'.format(mins, secs)
            count_down['text'] = '-'+ timeformat1        
        
            time.sleep(1)
            Time -= 1


#count up of the songs and its function

countup = Label(root, text = '--:--', font = 'Times 10 roman',bg = 'gray')
countup.place(x = 6, y = 617)

def time_countup(Time):
    global paused
    global progressBar
    #global song_length
    
    Timeup = 0
    while Timeup <= Time and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins,secs = divmod(Timeup,60)
            mins = round(mins)
            secs = round(secs)
            

            timeformat2 = '{:02d}:{:02d}'.format(mins, secs)
            #countup = Label(root, text = timeformat2, bg = 'gray', font = 'Times 10 roman').place(x = 6, y = 617)
            countup['text'] = timeformat2
                        
        
            time.sleep(1)
            Timeup += 1


            global song_length
            progressBar['maximum'] = song_length # the progress bar of the songs
            progressBar['value'] = Timeup
            if Timeup == song_length:
                progressBar['value'] = 0
            else:
                progressBar['value'] = Timeup







# the play function

global paused
paused = FALSE

def play():
    global status
    global paused
    played = TRUE
    global play_song
    
    if paused:
        mixer.music.unpause()
        status['text'] = 'playing ' + os.path.basename(filename)
        #status = Label(root, text = 'playing ' +os.path.basename(filename),relief = SUNKEN, anchor = W, bg = 'skyblue3', font = "Times 10 italic").place(x = 800, y = 720)
        paused = FALSE
    else:
        try:
            if played:
                try:
                    selected_song = playlistbox.curselection()
                    int(selected_song[0])
                    selected_song = int(selected_song[0])
                    play_song = playlist[selected_song]
                    mixer.music.load(play_song)
                    #mixer.music.load(filename)
                    mixer.music.play()
                    played = TRUE
                    music_details()
                    #status = Label(root, text = 'playing ' +os.path.basename(play_song),relief = SUNKEN, anchor = W, bg = 'skyblue3', font = "Times 10 italic").place(x = 800, y = 720)
                    status['text'] = 'playing ' +os.path.basename(play_song)
                   
                except:
                    mixer.music.load(filename)
                    mixer.music.play()
                    played = TRUE
                    music_details()
                    status['text'] = 'playing ' +os.path.basename(filename)
                                        
                
        except:
            tkinter.messagebox.showerror('File not found','please select a file')
        
    


    
   
#the pause function

def pause():
    global paused
    global status
    paused = TRUE
    mixer.music.pause()
    status['text'] = 'music paused'
    #status = Label(root, text = 'music paused',relief = SUNKEN, anchor = W, bg = 'skyblue3', font = "Times 10 italic").place(x = 800, y = 720)


# the stop function
def stop():
    global stoped
    global progressBar
    global paused
    
    stoped = TRUE
    mixer.music.stop()
    progressBar['value'] = 0
    countup = Label(root, text = '00:00', bg = 'gray', font = 'Times 10 roman').place(x = 6, y = 617)
    count_down['text'] = '00:00'
    status['text'] = 'music stoped'
        
    #status = Label(root, text = 'music stoped',relief = SUNKEN, anchor = W, bg = 'skyblue3', font = "Times 10 italic").place(x = 800, y = 720)

#volume function
def vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)


#mute function
mute = FALSE
def mute_unmute():
    global mute
    global stoped

    if mute:
        
        
        mixer.music.set_volume(0.4)
        muteb.configure(image = unmute)
        scale.set(40)
        mute = FALSE
        try:
            status['text'] = 'playing ' +os.path.basename(filename)
        except NameError:
            status['text'] = 'playing ' +os.path.basename(play_song)

    else:
        
        muteb.configure(image = mutepic)
        mixer.music.set_volume(0)
        scale.set(0)
        mute = TRUE
        status['text'] = 'muted'
        #status = Label(root, text = 'muted',relief = SUNKEN, anchor = W, bg = 'skyblue3', font = "Times 10 italic").place(x = 800, y = 720)

        while mute == TRUE:
            if mixer.music.set_volume(0) == False:
                muteb.configure(image = unmute)
            else:
                muteb.configure(image = mutepic)
                mixer.music.set_volume(0)
                scale.set(0)
                mute = TRUE
            break
                
        
#still on the playlist, this fuction deletes songs from the playlist
def Delete():
    selected_song = playlistbox.curselection()
    int(selected_song[0])
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)



    
    
        
delplaylist = ttk.Button(root, text = '- Del', cursor = 'hand2', command = Delete).place(x = 920, y = 425)





#root.geometry('300x300')
root.minsize(300,300)
icon = Image('photo', file = '003-music-note.png')
root.tk.call('wm','iconphoto',root._w,icon)





#objects for playing, i.e the pictures to be used s buttons
rewind = PhotoImage(file = '019-rewind.png')
playp = PhotoImage(file = '001-play-button.png')
stopp = PhotoImage(file = '005-stop.png')
pausep = PhotoImage(file = '011-pause.png')
fastforward = PhotoImage(file = '008-fast.png')
mutepic = PhotoImage(file = 'mute1.png')
unmute = PhotoImage(file = 'unmute2.png')




#the necessary buttons to play, pause, stop, 
playb = ttk.Button(frame2, image = playp, command = play)
playb.grid(column = 1,row = 1)

pauseb = ttk.Button(frame2, image = pausep, command = pause)
pauseb.grid(column = 2,row = 1)



stopb = ttk.Button(frame2, image = stopp, command = stop)
stopb.grid(column = 3,row = 1)

#fastb = ttk.Button(frame2, image = fastforward)
#fastb.grid(column = 4,row = 1)


muteb = Button(root, image = unmute, command = mute_unmute, bg = 'gray', relief = FLAT, bd = 0.9)
muteb.place(x = 153, y = 120)


# scale button

scale = ttk.Scale(root, from_ = 0, to = 100, orient = HORIZONTAL, command =vol)
scale.set(40)
mixer.music.set_volume(0.4)
scale.place(x = 460, y = 650)



root.mainloop()#to run the GUI


