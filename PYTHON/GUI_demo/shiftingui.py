import csv
import scipy.io.wavfile as wav
import pyworld as pw
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import argrelmin
import math
import peakutils
import soundfile as sf
import argparse
from audiolazy import *   
from audiolazy.lazy_stream import Stream
from audiolazy import Stream
np.set_printoptions(threshold=np.inf)





#################################
#DEFINE FORMANT DETECTION FUNCTION 
def cam_formants(x, fs):
	ms10=math.ceil(fs*0.005)
	ms30=math.floor(fs*0.03)
	ncoeff=2+fs/1000
	t = np.arange(0, len(x)-1)
	t = t/fs
	pos = 1
	fm =[]
	ft = []
	while (pos+ms10) <= len(x)+ms10:  #+ms10:
			y=x[pos:pos+ms10-1]
			y=y-np.mean(y)
			a=lpc(y, int(ncoeff))
			a = a.numerator
			rts=np.roots(a)
			rts = [r for r in rts if np.imag(r) >= 0.01]
			ang = np.arctan2(np.imag(rts), np.real(rts))
			frqs = sorted(ang * (fs / (2 * math.pi)))
			#print(frqs[0:4])

			fm.append(frqs)
			ft.append(pos/fs)
			pos = pos+ms10

	return fm,ft


####################################
####################################
def shift_formants(sp, ft, fm, fs, nos_of_peaks, shiftconst_test):
	multi_shiftedarrays = []
	new_sp=[]
	for q in np.arange(0, len(ft)):
		#print(q)- debug
		f0_low_limit = 89 
		fft_size= 2**math.ceil(np.log2(3 * fs / f0_low_limit + 1))
		frequency_axis=np.arange(0, fft_size)/fft_size*fs

		specenv_frame=sp[q,:]
		formant_frame=fm[q]
		test=specenv_frame
		minimas=[i for i in np.arange(1, len(test)-1) if test[i] <= test[i-1]  and test[i]<=test[i+1]]
		maximas= peakutils.indexes(specenv_frame) 
		formants_index=[];
		for d in formant_frame: 
		    formants_index.append(np.argmin(abs(frequency_axis-d)))
		new_formants=[];
		if len(maximas) == 0:
			#print('no maximas')
			maximass =[formants_index[0]]
		else:
			for k in formants_index:
				new_formants.append(np.argmin(abs(maximas-k)))
				maximass = maximas[np.unique(new_formants)]
		#print(maximass) 
		#print(minimas)- debug
		leftValley=[]
		rightValley=[]
		for j in maximass:
			if j <= minimas[0]: #ran into an instance of f1 same as minima[0]
				leftValley.append(0)
			else:  
				leftValley.append(np.amax([i for i in minimas if i < j]))
			if j > minimas[-1]:
				right_v=int(round(j+((len(specenv_frame)-j)/2)))
				rightValley.append(right_v) 
			else:  
				rightValley.append(np.amin([i for i in minimas if i > j]))

		multi_shiftedarrays = []
		for k in np.arange(0, len(maximass)):
			peakarray=[]
			peakindex=[]
			for j in np.arange(leftValley[k], rightValley[k]):
				peakarray.append(specenv_frame[j])
				peakindex.append(j)
			shiftconst=shiftconst_test[k]
			shifted_array =np.zeros(len(test))
			for i in peakindex:
				shifted_array[i+shiftconst]=test[i]
			if shiftconst<0:
				for k in np.arange(0, abs(shiftconst)):
					shifted_array[peakindex[-1]+k-1]=peakarray[-1]
			else:
				for k in np.arange(0, abs(shiftconst)):
					shifted_array[peakindex[0]+k]=peakarray[0]	

			multi_shiftedarrays.append(shifted_array)

		multi_shiftedarrays= np.max(multi_shiftedarrays,axis=0)
		for g in np.where(multi_shiftedarrays == 0)[0]:
			multi_shiftedarrays[g]=test[g]

		new_sp.append(multi_shiftedarrays)
	new_sp = np.array(new_sp)
	return new_sp



