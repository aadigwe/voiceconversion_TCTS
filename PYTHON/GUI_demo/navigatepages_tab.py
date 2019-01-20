'''
May 2017
@author: Burkhard A. Meier
'''
#======================
# imports
#======================
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import messagebox as msg
from tkinter import Spinbox
from time import  sleep         # careful - this can freeze the GUI
from tkinter import filedialog
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
#from matplotlib.figure import Figure
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
#from matplotlib import style
import pygame
import time
import scipy.io.wavfile as wav 
import numpy as np
import pandas as pd
import pyworld as pw
import soundfile as sf
from shiftingui import cam_formants, shift_formants 
#from shiftingui3 import cam_formants, shift_formants --> allows us set increments in frequencyies
import webbrowser

#url = 'file:///Users/adaezeadigwe/Desktop/python_speech/table.html'
GLOBAL_CONST = 42
EPSILON = 1e-8

#===================================================================
class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tip_window = None

    def show_tip(self, tip_text):
        "Display text in a tooltip window"
        if self.tip_window or not tip_text:
            return
        x, y, _cx, cy = self.widget.bbox("insert")      # get size of widget
        x = x + self.widget.winfo_rootx() + 25          # calculate to display tooltip 
        y = y + cy + self.widget.winfo_rooty() + 25     # below and to the right
        self.tip_window = tw = tk.Toplevel(self.widget) # create new tooltip window
        tw.wm_overrideredirect(True)                    # remove all Window Manager (wm) decorations
#         tw.wm_overrideredirect(False)                 # uncomment to see the effect
        tw.wm_geometry("+%d+%d" % (x, y))               # create window size

        label = tk.Label(tw, text=tip_text, justify=tk.LEFT,
                      background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tip(self):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()
            
#===================================================================          
def create_ToolTip(widget, text):
    toolTip = ToolTip(widget)       # create instance of class
    def enter(event):
        toolTip.show_tip(text)
    def leave(event):
        toolTip.hide_tip()
    widget.bind('<Enter>', enter)   # bind mouse events
    widget.bind('<Leave>', leave)



#=================================================================== 
class OOP():
    def __init__(self):         # Initializer method
        # Create instance
        self.win = tk.Tk()   
        
        create_ToolTip(self.win, 'Hello GUI')
        
        # Add a title       
        self.win.title("Python GUI")      
        self.create_widgets()

    def open_masker(self):
        global audio_file_name, x, fs
        audio_file_name = filedialog.askopenfilename(filetypes=(("Audio Files", ".wav .ogg"),   ("All Files", "*.*")))
        print(audio_file_name)
        x, fs = sf.read(audio_file_name)
        self.file_label.configure(text=audio_file_name)

    def playfile(self):
        global audio_file_name
        pygame.init()
        pygame.mixer.music.load(audio_file_name)
        pygame.mixer.music.play()
        time.sleep(10)


    # Modified Button Click Function
    def click_me(self): 
        self.action.configure(text='Hello ' + self.name.get() + ' ' + 
                         self.number_chosen.get())

    #TAB 3 - Vowel Conversion
    def conv3(self): 
        global audio_file_name, x, fs
        #self.action.configure(text=self.vowel_chosen.get())
        forman1 = [240, 235, 390, 370, 610, 585, 850, 820, 750, 700, 600, 500, 460, 360, 300, 250]
        forman2 = [2400, 2100, 2300, 1900, 1900, 1710, 1610, 1530, 940, 760, 1170, 700, 1310, 640, 1390, 595]
        print(self.vowel_chosen.get())
        r = [i for i,x in enumerate(self.vowel_chosen['values']) if x == self.vowel_chosen.get()]
        print(r)
        print(forman1[r[0]])
        frm1=forman1[r[0]]
        fm,ft = cam_formants(x,fs)
        fm1 = [item[0] for item in fm]
        avg_fm1=sum(fm1)/float(len(fm1))
        shf_freq1=frm1-avg_fm1
        print(shf_freq1)
        #repeat for formants 2
        frm2=forman2[r[0]]
        print(frm2)
        fm2 = [item[1] for item in fm]
        avg_fm2=sum(fm2)/float(len(fm2))
        print(avg_fm2)
        shf_freq2=frm2-avg_fm2
        print(shf_freq2)
        #Call the shift function
        nos_of_peaks = 2
        shiftconst_test = [shf_freq1,shf_freq2]
        print(shiftconst_test)
        f1_perc = [10,20,30,40,50]
        f2_perc = [5,10,15,20,25]
        #shifted_sp = shift_formants(_sp, ft, fm, fs, nos_of_peaks, shiftconst_test)
        #use shiftingui3 to increase by frequecies
    
    #Open Url Callback
    def openUrl(self):
        global url 
        webbrowser.open(url, 2) # The second parameter is todo with proxies and other features. Number 2 is a normal open 

    
    # Spinbox callback 
    def _spin(self):
        value = self.spin.get()
        print(value)
        self.scrol.insert(tk.INSERT, value + '\n')
        
    # GUI Callback  
    def checkCallback(self, *ignored_args):
        # only enable one checkbutton
        if self.chVarUn.get(): self.check3.configure(state='disabled')
        else:                  self.check3.configure(state='normal')
        if self.chVarEn.get(): self.check2.configure(state='disabled')
        else:                  self.check2.configure(state='normal') 
        
    # Radiobutton Callback- change it to adjust to shift methods
    def radCall(self):
        radSel = self.radVar.get()
        if   radSel == 0: self.mighty2.configure(text='Blue')
        elif radSel == 1: self.mighty2.configure(text='Gold')
        elif radSel == 2: self.mighty2.configure(text='Red')          
        
    # update progressbar in callback loop
    def run_progressbar(self):
        self.progress_bar["maximum"] = 100
        for i in range(101):
            sleep(0.05)
            self.progress_bar["value"] = i   # increment progressbar
            self.progress_bar.update()       # have to call update() in loop
        self.progress_bar["value"] = 0       # reset/clear progressbar  
    
    def start_progressbar(self):
        self.progress_bar.start()
        
    def stop_progressbar(self):
        self.progress_bar.stop()
     
    def progressbar_stop_after(self, wait_ms=1000):    
        self.win.after(wait_ms, self.progress_bar.stop)        

    def usingGlobal(self):
        global GLOBAL_CONST
        print(GLOBAL_CONST)
        GLOBAL_CONST = 777
        print(GLOBAL_CONST)
                    
    # Exit GUI cleanly
    def _quit(self):
        self.win.quit()
        self.win.destroy()
        exit() 

    def extractparam(self):
        global audio_file_name, x, fs, _f0, _sp, _ap
        x, fs = sf.read(audio_file_name)
        _f0, t = pw.dio(x, fs, f0_floor=50.0, f0_ceil=600.0)
        _sp = pw.cheaptrick(x, _f0, t, fs)
        _ap = pw.d4c(x, _f0, t, fs)
        print("done")

    def savefig(self):
        global audio_file_name, x, fs, _f0, _sp, _ap
        plt.figure()
        plt.subplot(4,1,1)
        plt.plot(x)
        plt.subplot(4,1,2)
        plt.plot(_f0)
        plt.subplot(4,1,3)
        plt.imshow(_sp.transpose(), origin='lower', interpolation='none', aspect='auto', extent=(0, _sp.shape[0], 0, _sp.shape[1]))
        plt.subplot(4,1,4)
        plt.imshow(_ap.transpose(), origin='lower', interpolation='none', aspect='auto', extent=(0, _ap.shape[0], 0, _ap.shape[1]))
        plt.savefig('testaudio/originalaudio.png')
        print('done')

    def plotfile(self):
        print('xyz')
 
    def synthesis_proc(self):
        global audio_file_name, x, fs, _f0, _sp, _ap, _y, audio_out
        print(self.fund.get())
        print(self.form1.get())
        print(self.form2.get())
        print(self.form3.get())
        perc_inc=self.fund.get()
        new_f0 = _f0 + ((perc_inc/100) * _f0)
        fm,ft = cam_formants(x,fs)
        nos_of_peaks = self.form4.get()
        shiftconst_test = [self.form1.get(), self.form2.get(), self.form3.get()]
        shifted_sp = shift_formants(_sp, ft, fm, fs, nos_of_peaks, shiftconst_test)
        new_y = pw.synthesize(new_f0[0:len(_f0)-1], shifted_sp, _ap[0:len(_f0)-1], fs)
        audio_out='testaudio/'+'audio-out' + '_' + str(self.fund.get()) + '_' + str(self.form1.get()) + '_' + str(self.form2.get()) + '_' + str(self.form3.get())+'.wav'
        wav.write(audio_out,fs, new_y)
        wav.write('testaudio/origfile.wav',fs, x)
        print('done')
        plt.figure()
        plt.subplot(4,1,1)
        plt.title('Waveform')
        plt.plot(x)
        plt.plot(new_y)
        plt.subplot(4,1,2)
        plt.plot(_f0)
        plt.plot(new_f0)
        plt.subplot(4,1,3)
        plt.imshow(shifted_sp.transpose(), origin='lower', interpolation='none', aspect='auto', extent=(0, _sp.shape[0], 0, _sp.shape[1]))
        plt.subplot(4,1,4)
        plt.imshow(_ap.transpose(), origin='lower', interpolation='none', aspect='auto', extent=(0, _ap.shape[0], 0, _ap.shape[1]))
        plt.savefig(audio_out+'.png')
        print('done')

 
                  
    #####################################################################################       
    def create_widgets(self):    
        tabControl = ttk.Notebook(self.win)          # Create Tab Control
        
        tab1 = ttk.Frame(tabControl)            # Create a tab 
        tabControl.add(tab1, text='Analysis')      # Add the tab
        tab2 = ttk.Frame(tabControl)            # Add a second tab
        tabControl.add(tab2, text='Modification')      # Make second tab visible
        tab3 = ttk.Frame(tabControl)            # Add a second tab
        tabControl.add(tab3, text='Vowel Conversion')      # Make second tab visible
        tab4 = ttk.Frame(tabControl)            # Add a second tab
        tabControl.add(tab4, text='Smiled Speech')      # Make second tab visible
        
        tabControl.pack(expand=1, fill="both")  # Pack to make visible
        
        # LabelFrame using tab1 as the parent
        mighty = ttk.LabelFrame(tab1, text=' Analysis of Audio File')
        mighty.grid(column=0, row=0, padx=8, pady=4)
        
        #BUTTON 1, TAB 1 to open file
        self.action = ttk.Button(mighty, text="Open File", command=self.open_masker)   
        self.action.grid(column=0, row=0, sticky='W') 

        #LABEL 1, TAB 1, WRITE FILENAME 
        self.file_label = ttk.Label(mighty, text="file name")
        self.file_label.grid(column=1, row=0)

        #BUTTON 2, TAB 1 to play file
        self.action2 = ttk.Button(mighty, text="Play file", command=self.playfile)   
        self.action2.grid(column=0, row=1, sticky='W') 

        #BUTTON 3, Extract Parametres
        self.action3 = ttk.Button(mighty, text="Extract Parameters", command=self.extractparam)   
        self.action3.grid(column=0, row=2, sticky='W') 

        #BUTTON 4, Plot FO contour, spectrogram, aperiodicity
        self.action3 = ttk.Button(mighty, text="Save plots", command=self.savefig)   
        self.action3.grid(column=0, row=3, sticky='W') 
        
        # TAB CONTROL 2 ----------------------------------------------------------------------
        # We are creating a container frame to hold all other widgets -- Tab2 Formant and Pitch Modification
        self.mighty2 = ttk.LabelFrame(tab2, text='Set Parameters')
        self.mighty2.grid(column=0, row=0, padx=8, pady=4)
        ####
        chVarDis = tk.IntVar()
        check1 = tk.Checkbutton(self.mighty2, text="Percent(%)", variable=chVarDis, state='disabled')
        check1.select()
        check1.grid(column=0, row=0, sticky=tk.W)                   
        chVarUn = tk.IntVar()
        check2 = tk.Checkbutton(self.mighty2, text="Set Freq", variable=chVarUn)
        check2.deselect()
        check2.grid(column=1, row=0, sticky=tk.W)  
        ####
        self.radVar = tk.IntVar()
        self.radVar.set(99)  
        colors = ["Shift method 1", "Shift method 2"] 
        for col in range(2):                             
            curRad = tk.Radiobutton(self.mighty2, text=colors[col], variable=self.radVar, 
                                    value=col, command=self.radCall)          
            curRad.grid(column=col, row=1, sticky=tk.W)    
        ####
        self.fund_label = ttk.Label(self.mighty2, text="f0 %increase")
        self.fund_label.grid(column=0, row=2)
        self.fund = tk.IntVar()
        fund_entered = ttk.Entry(self.mighty2, width=12, textvariable=self.fund)
        fund_entered.grid(column=1, row=2, sticky='W')  

        self.form1_label = ttk.Label(self.mighty2, text="Formant 1")
        self.form1_label.grid(column=0, row=3)
        self.form1 = tk.IntVar()
        form1_entered = ttk.Entry(self.mighty2, width=12, textvariable=self.form1)
        form1_entered.grid(column=1, row=3, sticky='W')

        self.form2_label = ttk.Label(self.mighty2, text="Formant 2")
        self.form2_label.grid(column=0, row=4)
        self.form2 = tk.IntVar()
        form2_entered = ttk.Entry(self.mighty2, width=12, textvariable=self.form2)
        form2_entered.grid(column=1, row=4, sticky='W')

        self.form3_label = ttk.Label(self.mighty2, text="Formant 3")
        self.form3_label.grid(column=0, row=5)
        self.form3 = tk.IntVar()
        form3_entered = ttk.Entry(self.mighty2, width=12, textvariable=self.form3)
        form3_entered.grid(column=1, row=5, sticky='W')

        self.form4_label = ttk.Label(self.mighty2, text="Nos of formants to modify*")
        self.form4_label.grid(column=0, row=6)
        self.form4 = tk.IntVar()
        form4_entered = ttk.Entry(self.mighty2, width=12, textvariable=self.form4)
        form4_entered.grid(column=1, row=6, sticky='W')

        # FRAME 2 TAB 2 ----------------------------------------------------------------------
        self.mighty2b = ttk.LabelFrame(tab2, text='Apply Modification')
        self.mighty2b.grid(column=1, row=0, padx=8, pady=4)

        self.but1 = ttk.Button(self.mighty2b, text="Extract", command=self.playfile)   
        self.but1.grid(column=0, row=0, sticky='W') 
        self.but2 = ttk.Button(self.mighty2b, text="Synthesize", command=self.synthesis_proc)   
        self.but2.grid(column=0, row=1, sticky='W')
        self.but3 = ttk.Button(self.mighty2b, text="Play Orig Audio", command=self.playfile)   
        self.but3.grid(column=0, row=2, sticky='W')
        self.but4 = ttk.Button(self.mighty2b, text="Play Mod. Audio", command=self.playfile)   
        self.but4.grid(column=0, row=3, sticky='W')
        self.but5 = ttk.Button(self.mighty2b, text="CSV output", command=self.playfile)   
        self.but5.grid(column=0, row=4, sticky='W')
        self.but6 = ttk.Button(self.mighty2b, text="Rand. Vis Shift", command=self.playfile)   
        self.but6.grid(column=0, row=4, sticky='W')
        ####
        
       

        # TAB CONTROL 3- Vowel Conversion ----------------------------------------------------------------------
        # We are creating a container frame to hold all other widgets -- Tab2 Formant and Pitch Modification
        self.mighty3 = ttk.LabelFrame(tab3, text='Set Parameters')
        self.mighty3.grid(column=0, row=0, padx=8, pady=4)
        self.note_label = ttk.Label(self.mighty3, text="Vowel conversion based on wikipedia")
        #Open two dialogs to select audio file and print labels
        #BUTTON 1 - OPEN AUDIO 1
        self.fileaudio3btn = ttk.Button(self.mighty3, text="Open source vowel", command=self.open_masker)   
        self.fileaudio3btn.grid(column=0, row=1, sticky='W') 
        self.fileaudio3_label = ttk.Label(self.mighty3, text="source file name")
        self.fileaudio3_label.grid(column=1, row=1)

        self.extract3 = ttk.Button(self.mighty3, text="Extract Parameters", command=self.extractparam)   
        self.extract3.grid(column=0, row=2, sticky='W') 

        ttk.Label(self.mighty3, text="Choose target vowel:").grid(column=0, row=3, sticky='W')
        vowel = tk.StringVar()
        self.vowel_chosen = ttk.Combobox(self.mighty3, width=12, textvariable=vowel, state='readonly')
        self.vowel_chosen['values'] = ('i', 'y', 'e', 'ø', 'ɛ','œ','a', 'ɶ', 'ɑ', 'ɒ','ʌ','ɔ','ɤ','o','ɯ','u')
        self.vowel_chosen.grid(column=1, row=3)
        self.vowel_chosen.current(0)
        
        self.conv3 = ttk.Button(self.mighty3, text="Conversion", command=self.conv3)   
        self.conv3.grid(column=0, row=4, sticky='W') 

        #Dynamic Time Warping
        #Find diffrence and shift accordingly 
        #plot scatterplots & contour for formants before 
        #plot scatterplots & contour for formants after        
        self.note_label.grid(column=0, row=0)



        # TAB CONTROL 4- Smiled Speech - Percentages ----------------------------------------------------------------------
        # We are creating a container frame to hold all other widgets -- Tab2 Formant and Pitch Modification
        self.mighty4 = ttk.LabelFrame(tab4, text='Neutral/Smiling/Amused Speech')
        self.mighty4.grid(column=0, row=0, padx=8, pady=4)
        self.note2_label = ttk.Label(self.mighty4, text="Iterate different formant frequency increase for source audio")
        self.note2_label.grid(column=0, row=0)

        self.fileaudio4btn = ttk.Button(self.mighty4, text="Open source vowel", command=self.open_masker)   
        self.fileaudio4btn.grid(column=0, row=1, sticky='W') 
        self.fileaudio4_label = ttk.Label(self.mighty4, text="source file name")
        self.fileaudio4_label.grid(column=1, row=1)
     
        self.scatterbtn = ttk.Button(self.mighty4, text="Scatter Plots", command=self.open_masker)   
        self.scatterbtn.grid(column=0, row=4, sticky='W') 

        self.webButton = ttk.Button(self.mighty4, text='Open URL', command=self.openUrl)
        self.webButton.grid(column=0, row=5, sticky='W') 
        #Open dialog to select file
        #Find diffrence and shift accordingly 
        #plot scatterplots & contour for F1 and F2 before and after
        #plot fundamental frequency  
        #apply mean percent enter both extremes increase     
        
        # WHOLE Creating a Menu Bar----------------------------------------------------------------------
        menu_bar = Menu(self.win)
        self.win.config(menu=menu_bar)
        
        # Add menu items
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        # Change the main windows icon
        #self.win.iconbitmap('pyc.ico')

        
        
        # It is not necessary to create a tk.StringVar() 
        # strData = tk.StringVar()
        
        # call function
        self.usingGlobal()
            
         
#======================
# Start GUI
#======================
oop = OOP()
oop.win.mainloop()
