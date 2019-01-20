'''
May 2017
@author: Burkhard A. Meier
'''
#======================
# imports
#======================
import tkinter as tk
import os
from tkinter import ttk
from tkinter import font as tkfont
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import messagebox as msg
from tkinter import Spinbox
from time import  sleep         # careful - this can freeze the GUI
from tkinter import filedialog
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
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
#FOR TAB 4
from Amus_shifting import *
import webbrowser

#url = 'file:///Users/adaezeadigwe/Desktop/python_speech/table.html'
url = 'file:///Users/adaezeadigwe/Desktop/python_speech/table.html'
GLOBAL_CONST = 42
#title_font = tkfont.Font(family="Helvetica", size=12, weight="bold")
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
        self.win.title("Modification Speech Parameters in World")      
        self.create_widgets()
        

    def open_masker(self):
        global audio_file_name, x, fs
        audio_file_name = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file",filetypes=(("Audio Files", ".wav .ogg"),   ("All Files", "*.*")))
        print(audio_file_name)
        x, fs = sf.read(audio_file_name)
        self.file_label.configure(text=audio_file_name[-20:])

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
        fft_size  = 21
        #self.action.configure(text=self.vowel_chosen.get())
        forman1 = [280, 360, 600, 800, 560, 760, 740, 320, 380, 480, 560]
        forman2 = [2620, 2220, 2060, 1760, 1480, 1320, 1180, 920, 940, 760, 920]
        forman3 = [3380, 2960, 2840, 2500, 2520, 2500, 2640, 2200, 2300, 2620, 560]
        self.source_vowel['values'] = ('/iː/', '/ɪ/', '/e/', '/æ/','/ɜː/','/ʌ/', '/ɑː/', '/uː/', '/ʊ/','/ɔː/','/ɒ/')
        print("Source Vowel:",self.source_vowel.get())
        #Extract features for source vowel
        source_vowel = [i for i,x in enumerate(self.source_vowel['values']) if x == self.source_vowel.get()]
        print(source_vowel)
        print(forman1[source_vowel[0]])
        source_frm1=forman1[source_vowel[0]]
        source_frm2=forman2[source_vowel[0]]
        #Modifying the audio filename to open
        audio_vowel_path = list('Audio_files/vowels/00.wav')
        audio_vowel_path[20] = str(source_vowel[0])
        audio_vowel_path = "".join(audio_vowel_path)
        print(audio_vowel_path)
        x, fs = sf.read(audio_vowel_path)
        #Extract features for target vowel
        print("Target Vowel:",self.target_vowel.get())
        target_vowel = [i for i,x in enumerate(self.target_vowel['values']) if x == self.target_vowel.get()]
        print(target_vowel)
        print(forman1[target_vowel[0]])
        target_frm1=forman1[target_vowel[0]]
        target_frm2=forman2[target_vowel[0]]

        #Select Formant Difference Method 
        form_diff = self.formdiffVar.get()
        if   form_diff == 0: 
            print('Formant difference: Wikipedia Values')
            source_target_form1_diff = round((target_frm1 - source_frm1)/fft_size)
            source_target__form2_diff = round((target_frm2 - source_frm2)/fft_size)
            #convert this differences on an fftscale and let this be formant_shift_array[0]
            print('Formant 1 freq shift',source_target_form1_diff,"Hz")
            print('Formant 2 freq shift',source_target__form2_diff,"Hz")

        elif form_diff == 1: 
            print('Formant diffrence: Source-Target Formant Diffrence')
            fm,ft = cam_formants(x,fs)
            fm1 = [item[0] for item in fm]
            avg_fm1=sum(fm1)/float(len(fm1))
            shf_freq1=frm1-avg_fm1
            print(shf_freq1)
            #-----------#-------------#---------#
            fm2 = [item[1] for item in fm]
            avg_fm2=sum(fm2)/float(len(fm2))
            print(avg_fm2)
            shf_freq2=frm2-avg_fm2
            print(shf_freq2)
            
        shiftconst_array = [source_target_form1_diff, source_target__form2_diff]
        nos_of_peaks = 2
        #Select Shift Method 
        radSel = self.radVar.get()
        if   radSel == 0: 
            print('shift by constant selected')
            shifted_sp = shift_formants(_sp, ft, fm, fs, nos_of_peaks, shift_array)
        elif radSel == 1: 
            print('shift by resampling selected')
            shifted_sp = shiftspectrogram(_sp, formants_matrix, maximas,  nos_of_peaks, shift_array) # fix, maximas, formant_matrix
        elif radSel == 2: 
            print('shift by interpolation selected') 
            shifted_sp = shiftspectrogram(_sp, formants_matrix, maximas,  nos_of_peaks, shift_array) # similar for interprolation redifine function
        shifted_sp = shift_formants(_sp, ft, fm, fs, nos_of_peaks, shiftconst_test)
        new_y = pw.synthesize(new_f0[0:len(shifted_sp)], shifted_sp, _ap[0:len(shifted_sp)], fs)

        audio_out='testaudio/'+'source_target_conv' + '_' + str(self.fund.get()) + '_' + str(self.form1.get()) + '_' + str(self.form2.get()) + '_' + str(self.form3.get())+'.wav'
        wav.write(audio_out,fs, new_y)


        
        fm,ft = cam_formants(x,fs) #x, fs of the slected vowel 
        shifted_sp = shift_formants(_sp, ft, fm, fs, nos_of_peaks, shiftconst_array)

    
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
        if   radSel == 0: self.mighty2.configure(text='Shift using constant') # call a syntheis measure
        elif radSel == 1: self.mighty2.configure(text='Shift by resampling') #call synthesis resample
        elif radSel == 2: self.mighty2.configure(text='Shifting by interprolation')          
        
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
        global audio_file_name, x, fs, _f0, _sp, _ap, _y, audio_out, shifted_sp
        print(self.fund.get())
        print(self.form1.get())
        print(self.form2.get())
        print(self.form3.get())
        perc_inc=self.fund.get()
        new_f0 = _f0 + ((perc_inc/100) * _f0)
        fm,ft = cam_formants(x,fs)
        nos_of_peaks = self.form4.get()
        shift_array = [self.form1.get(), self.form2.get(), self.form3.get()]
        #Select Shift Method 
        radSel = self.radVar.get()
        if   radSel == 0: 
            print('shift by constant selected')
            shifted_sp = shift_formants(_sp, ft, fm, fs, nos_of_peaks, shift_array)
        elif radSel == 1: 
            print('shift by resampling selected')
            shifted_sp = shiftspectrogram(_sp, formants_matrix, maximas,  nos_of_peaks, shift_array) # fix, maximas, formant_matrix
        elif radSel == 2: 
            print('shift by interpolation selected') 
            shifted_sp = shiftspectrogram(_sp, formants_matrix, maximas,  nos_of_peaks, shift_array) # similar for interprolation redifine function
        shifted_sp = shift_formants(_sp, ft, fm, fs, nos_of_peaks, shiftconst_test)
        new_y = pw.synthesize(new_f0[0:len(shifted_sp)], shifted_sp, _ap[0:len(shifted_sp)], fs)

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
        plt.show()
        plt.savefig(audio_out+'.png')
        print('done')
        
        
 
    def plotrandom(self):
        global _sp, shifted_sp
        sp = _sp
        x=np.random.randint(len(sp), size=3)
        print(sp.shape)
        for i in x:
            plt.plot(sp[i,:])
            plt.plot(shifted_sp[i,:])
            plt.show()
        print('done')

    def open_masker_smiled(self):
        global smiled_audio_path
        smiled_audio_path= filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file",filetypes=(("Audio Files", ".wav .ogg"),   ("All Files", "*.*")))
        print(smiled_audio_path)
        self.fileaudio4_label .configure(text=smiled_audio_path[-20:])


    #Get iterable formany pecentages _Used for button Extract Parameters
    def printentries(self):
        global smiled_audio_path
        formant1_perc= [self.form1a.get(), self.form1b.get(), self.form1c.get(), self.form1d.get(), self.form1e.get()]
        formant2_perc= [self.form2a.get(), self.form2b.get(), self.form2c.get(), self.form2d.get(), self.form2e.get()]
        zyx = looptoweb(smiled_audio_path, formant1_perc, formant1_perc)
        for i in formant1_perc:
            print(i)
        print("Done with multi-formant shifting")

    def smile_openUrl(self):
        webbrowser.open('file:///Users/adaezeadigwe/Desktop/Final_Project_TCTS2017/PYTHON/GUI_demo/Amus_shifting.html', 2) # The second parameter is todo with proxies and other features. Number 2 is a normal open 

    def showtable(self):
        img=mpimg.imread('vowel-formant-table.png')
        imgplot = plt.imshow(img)
        plt.show()


    # Exit GUI cleanly
    def _quit(self):
        self.win.quit()
        self.win.destroy()
        exit() 


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
        mighty = ttk.LabelFrame(tab1, text="Analysis of Audio File") #font=title_font)
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

        self.form4_label = ttk.Label(self.mighty2, text="Nos. of formants*")
        self.form4_label.grid(column=0, row=6)
        self.form4 = tk.IntVar()
        form4_entered = ttk.Entry(self.mighty2, width=12, textvariable=self.form4)
        form4_entered.grid(column=1, row=6, sticky='W')

        # FRAME 2 TAB 2 ----------------------------------------------------------------------


        self.mighty2a = ttk.LabelFrame(tab2, text='Select Shift Method')
        self.mighty2a.grid(column=1, row=0, padx=8, pady=4)

        ####
        self.radVar = tk.IntVar()
        self.radVar.set(99)  
        colors = ["Shift method 1", "Shift method 2", "Shift method 3"] 
        for col in range(3):                             
            curRad = tk.Radiobutton(self.mighty2a, text=colors[col], variable=self.radVar, 
                                    value=col, command=self.radCall)          
            curRad.grid(column=0, row=col, sticky=tk.W)    
        ####

        self.mighty2b = ttk.LabelFrame(tab2, text='Apply Modification')
        self.mighty2b.grid(column=2, row=0, padx=8, pady=4)

        self.but1 = ttk.Button(self.mighty2b, text="Extract", command=self.extractparam)   
        self.but1.grid(column=0, row=0, sticky='W') 
        self.but2 = ttk.Button(self.mighty2b, text="Synthesize", command=self.synthesis_proc)   
        self.but2.grid(column=0, row=1, sticky='W')
        self.but6 = ttk.Button(self.mighty2b, text="Rand. Vis Shift", command=self.plotrandom)   
        self.but6.grid(column=0, row=2, sticky='W')
        ####
        
       

        # TAB CONTROL 3- Vowel Conversion ----------------------------------------------------------------------
        # We are creating a container frame to hold all other widgets -- Tab2 Formant and Pitch Modification
        self.mighty3 = ttk.LabelFrame(tab3, text='Select Source+Target Vowel')
        self.mighty3.grid(column=0, row=0, padx=8, pady=4)
        #Open two dialogs to select audio file and print labels
        #BUTTON 1 - OPEN AUDIO 1

        ttk.Label(self.mighty3, text="Choose source vowel:").grid(column=0, row=0, sticky='W')
        source_vowel = tk.StringVar()
        self.source_vowel = ttk.Combobox(self.mighty3, width=6, textvariable=source_vowel, state='readonly')
        #self.source_vowel['values'] = ('i', 'y', 'e', 'ø', 'ɛ','œ','a', 'ɶ', 'ɑ', 'ɒ','ʌ','ɔ','ɤ','o','ɯ','u')
        self.source_vowel['values'] = ('/iː/', '/ɪ/', '/e/', '/æ/','/ɜː/','/ʌ/', '/ɑː/', '/uː/', '/ʊ/','/ɔː/','/ɒ/')
        self.source_vowel.grid(column=1, row=0)
        self.source_vowel.current(0)

        ttk.Label(self.mighty3, text="Choose target vowel:").grid(column=0, row=1, sticky='W')
        target_vowel = tk.StringVar()
        self.target_vowel = ttk.Combobox(self.mighty3, width=6, textvariable=target_vowel, state='readonly')
        self.target_vowel['values'] = ('/iː/', '/ɪ/', '/e/', '/æ/','/ɜː/','/ʌ/', '/ɑː/', '/uː/', '/ʊ/','/ɔː/','/ɒ/')
        self.target_vowel.grid(column=1, row=1)
        self.target_vowel.current(0)

        # TAB 3 FRAME 2 ----------------------------------------------------------------------
        self.mighty3a = ttk.LabelFrame(tab3, text='Formant diffrence')
        self.mighty3a.grid(column=1, row=0, padx=8, pady=4)
        ####
        self.formdiffVar = tk.IntVar()
        self.formdiffVar.set(99)  
        vowel_formant_diff = ["Wikipedia_Defined", "Source-Targ Different"] 
        for col in range(2):                             
            curRad = tk.Radiobutton(self.mighty3a, text=vowel_formant_diff[col], variable=self.formdiffVar, 
                                    value=col, command=self.radCall) #change the command         
            curRad.grid(column=0, row=col, sticky=tk.W)    
        ####
        
        # TAB 3 FRAME 3 ----------------------------------------------------------------------
        self.mighty3b = ttk.LabelFrame(tab3, text='Shift Method')
        self.mighty3b.grid(column=2, row=0, padx=8, pady=4)
        ####
        self.radVar = tk.IntVar() #!!!!!!!might need to change VAR not sure yet
        self.radVar.set(99)  
        colors = ["Shift method 1", "Shift method 2", "Shift method 3"] 
        for col in range(3):                             
            curRad = tk.Radiobutton(self.mighty3b, text=colors[col], variable=self.radVar, 
                                    value=col, command=self.radCall)          
            curRad.grid(column=0, row=col, sticky=tk.W)    
        ####

        # TAB 3 FRAME 4 ---------------------------------------------------------------------
        self.mighty3c = ttk.LabelFrame(tab3, text='Analysis/Modification')
        self.mighty3c.grid(column=3, row=0, padx=8, pady=4)

        self.but1 = ttk.Button(self.mighty3c, text="Formant Freq. Table", command=self.showtable)   
        self.but1.grid(column=0, row=0, sticky='W') 
        self.but2 = ttk.Button(self.mighty3c, text="Conversion", command=self.conv3)   
        self.but2.grid(column=0, row=1, sticky='W')
        self.but3 = ttk.Button(self.mighty3c, text="Formant Contour/Scatter Plots", command=self.plotrandom)   
        self.but3.grid(column=0, row=2, sticky='W')
        self.but4 = ttk.Button(self.mighty3c, text="Listen in browser", command=self.plotrandom)   
        self.but4.grid(column=0, row=3, sticky='W')
        self.but5 = ttk.Button(self.mighty3c, text="Frame Visualization", command=self.plotrandom)   
        self.but5.grid(column=0, row=4, sticky='W')

        #Dynamic Time Warping
        #Find diffrence and shift accordingly 
        #plot scatterplots & contour for formants before 
        #plot scatterplots & contour for formants after        



        # TAB CONTROL 4- Smiled Speech - Percentages ----------------------------------------------------------------------
        # We are creating a container frame to hold all other widgets -- Tab2 Formant and Pitch Modification
        self.mighty4 = ttk.LabelFrame(tab4, text='Neutral/Smiling/Amused Speech')
        self.mighty4.grid(column=0, row=0, padx=8, pady=4)
        self.note2_label = ttk.Label(self.mighty4, text="Iterate different formant frequency increase for source audio")
        self.note2_label.grid(column=0, row=0)

        self.fileaudio4btn = ttk.Button(self.mighty4, text="Open speech file", command=self.open_masker_smiled)   
        self.fileaudio4btn.grid(column=0, row=1, sticky='W') 
        self.fileaudio4_label = ttk.Label(self.mighty4, text="source file name")
        self.fileaudio4_label.grid(column=1, row=1)

        # TAB 4 FRAME 2 ----------------------------------------------------------------------
        self.mighty4a = ttk.LabelFrame(tab4, text='Formant percentages')
        self.mighty4a.grid(column=0, row=1, padx=8, pady=4)

        self.note2_label = ttk.Label(self.mighty4a, text="Formant 1")
        self.note2_label.grid(column=0, row=0)

        self.note2_label = ttk.Label(self.mighty4a, text="Formant 2")
        self.note2_label.grid(column=0, row=1)
        ####
        self.form1a = tk.IntVar()
        self.form1b = tk.IntVar()
        self.form1c = tk.IntVar()
        self.form1d = tk.IntVar()
        self.form1e = tk.IntVar()
        formant1_perc= [self.form1a, self.form1b, self.form1c, self.form1d, self.form1e]
        self.form2a = tk.IntVar()
        self.form2b = tk.IntVar()
        self.form2c = tk.IntVar()
        self.form2d = tk.IntVar()
        self.form2e = tk.IntVar()
        formant2_perc= [self.form2a, self.form2b, self.form2c, self.form2d, self.form2e]
        for row in range(5):                             
            form1_array = ttk.Entry(self.mighty4a, width=8,textvariable=formant1_perc[row])         
            form1_array.grid(column=row+1, row=0, sticky=tk.W)  
            form2_array = ttk.Entry(self.mighty4a, width=8,textvariable=formant2_perc[row])         
            form2_array.grid(column=row+1, row=1, sticky=tk.W)   
        ####

        self.form3_label = ttk.Label(self.mighty2, text="Formant 3")
        self.form3_label.grid(column=0, row=5)
        self.form3 = tk.IntVar()
        form3_entered = ttk.Entry(self.mighty2, width=12, textvariable=self.form3)
        form3_entered.grid(column=1, row=5, sticky='W')
        #Open dialog to select file
        #Find diffrence and shift accordingly 
        #plot scatterplots & contour for F1 and F2 before and after
        #plot fundamental frequency  
        #apply mean percent enter both extremes increase 

        # TAB 4 FRAME 3 ----------------------------------------------------------------------
        self.mighty4c = ttk.LabelFrame(tab4, text='Analysis/Modification')
        self.mighty4c.grid(column=2, row=0, padx=8, pady=4)

        self.but1 = ttk.Button(self.mighty4c, text="Extract parameteres", command=self.extractparam)   
        self.but1.grid(column=0, row=0, sticky='W') 
        self.but2 = ttk.Button(self.mighty4c, text="Conversion", command=self.conv3)   
        self.but2.grid(column=0, row=1, sticky='W')
        self.but3 = ttk.Button(self.mighty4c, text="Formant Contour/Scatter Plots", command=self.plotrandom)   
        self.but3.grid(column=0, row=2, sticky='W')
        self.but4 = ttk.Button(self.mighty4c, text="Listen in browser", command=self.smile_openUrl)   
        self.but4.grid(column=0, row=3, sticky='W')
        self.but5 = ttk.Button(self.mighty4c, text="Frame Visualization", command=self.plotrandom)   
        self.but5.grid(column=0, row=4, sticky='W')    
        
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
