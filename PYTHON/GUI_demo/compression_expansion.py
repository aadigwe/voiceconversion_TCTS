import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import signal
from scipy.signal import argrelmin
from scipy.signal import argrelmax
import soundfile as sf
import scipy.io.wavfile as wav
import pyworld as pw
import math
import argparse
from audiolazy import *   
from audiolazy.lazy_stream import Stream
from audiolazy import Stream #for lpc
np.set_printoptions(threshold=np.inf)


path = "Audio_files/SpkBeng_0008.wav"
x, fs = sf.read(path)  
#fs, x = wav.read(path)
print(x.shape)
f0, t = pw.dio(x, fs, f0_floor=50.0, f0_ceil=600.0)
sp = pw.cheaptrick(x, f0, t, fs)
ap = pw.d4c(x, f0, t, fs)
f0_low_limit = 89
fft_size= 2**math.ceil(np.log2(3 * fs / f0_low_limit + 1))
frequency_axis=np.arange(0, fft_size+1)/fft_size*fs
shift_array = [13, 15, 17]
frequency_scale = fs/fft_size
nos_peaks = 2

########################################################################
#					HELPER FUNCTIONS							#	
########################################################################
#FORMANT DETECTION FUNCTION 
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
			fm.append(frqs)
			ft.append(pos/fs)
			pos = pos+ms10

	return fm,ft

#FUNCTION 1 FORMANT HELPER FUNCTIONS 
#INPUT: ENTIRE SPECTROGRAM 
#OUTPUT MATRIX OF FORMANTS 
def matrixformants(x, fs):
	fm, ft = cam_formants(x, fs)
	formants = []
	for i in np.arange(4):
		lstform = [item[i] for item in fm]
		formants.append(lstform)
	return formants



#FUNCTION 2: CALCULATE THE MAXIMAS IN EACH SPECTRAL ENNVELOPE FOR THE ENTIRE SPECTROGRAM 
#INPUT:  SPECTROGRAM 
#OUTPUT: MATRIX OF  OF MAXIMAS W/LENGTH OF SPECTROGRAM 
def maximas(sp, formants, frequency_axis):
	maximas_matrix =[]
	for i in np.arange(0,len(sp)): #length 156 column
		maximas = argrelmax(sp[i])
		maximas_matrix.append(maximas)
	return maximas_matrix

#FUNCTION 3: TO MAKE THE FORMANT EASIER TO READ BY FRAME
def func3(formants):
	formants_matrix = []
	for i in np.arange(len(formants[0])):
		formant_frame = []
		for j in np.arange(len(formants)):
			form = formants[j][i]
			formant_frame.append(form)
		formants_matrix.append(formant_frame)
	return formants_matrix

#FUNCTION 3/4: THIS FUNCTION RETURN THE MAXIMAS AND THE INDEX FOR EACH ENVELOPE
def func4(sp):
	maximas = []
	for i in np.arange(0,len(sp)): #length 156 column
		maximas_perframe = argrelmax(sp[i])
		maximas.append(maximas_perframe)
	return(maximas)

#FUNCTION: THIS FUNCTION FINDS THE MAXIMAS NEAREST TO FORMANTS AND TAKES THE UNIQUE
###IMPORTANT - GIVES THE INDEX OF THE MAXIMAS THAT ARE NEAREST THE FORMANTS
def normalize_maximas(maximas, formants_matrix, frequency_scale):
	norm_formant_matrix = []
	for i in np.arange(0, len(formants_matrix)): #length 159
		maximas_frame = maximas[i][0]
		norm_formant_frame= []
		for j in np.arange(0, len(formants_matrix[i])):
			norm_formant_frame.append(np.argmin(abs(maximas[i] -round(formants_matrix[i][j]/frequency_scale))))
		norm_formant_matrix.append(np.unique(maximas_frame[norm_formant_frame]))
	return(norm_formant_matrix)

#FUNCTION 3: FIND THE MAXIMAS NEAREST TO THE FORMANTS 
#INPUT: MAXIMAS, FORMANTS 
#OUTPUT: NEW MAXIMAS
def min_formants(sp, formants, frequency_axis):
	formants_matrix =[]
	for i in len(formants): #length 159 
		formant_frame= []
		for d in formant_frame: #row
			formants_frame.append(np.argmin(abs(frequency_axis-d)))
		formants_matrix.append(formant_frame)
	return formants_matrix

#FUNCTION 4: RETURNS LEFT AND RIGHT ARRAY 
#INPUT: SPEC_ENV,  MAXIMAS[i], MAXIMAS 
#OUTPUT: LEFT ARRAY, RIGHT ARRAY
def ppparray(spec_env, form_index,maximas):
	leftvalley = [i for i in maximas if i < form_index]
	#CONDITION: if array is empty make it the first element
	if len(leftvalley)==0: 
		leftvalue = 0
	else:
		leftvalue = np.argmin(abs(leftvalley - form_index))
		leftvalue = leftvalley[leftvalue]
	leftvalley = spec_env[leftvalue:form_index]
	leftvalley = np.append(leftvalley, spec_env[form_index])
	rightvalley = [i for i in maximas if i > form_index]
	rightvalue = np.argmin(abs(rightvalley - form_index))
	rightvalue = rightvalley[rightvalue]
	rightvalley = spec_env[form_index:rightvalue+1]
	return leftvalley,rightvalley, leftvalue, rightvalue

#FUNCTION 5: DOES THE SHIFT/RESAMPLING AND RETURNS RESAMPLED ARRAY 
#INPUT: LEFT ARRAY, RIGHT ARRAY, SHIFT CONST
#NOTE IS PEAK1_ind + SHIFT CONST > PEAK2_IND, THEN SHIFT CONST = DIFF
#OUTPUT: RESAMPLED ARRAY 
def resample(leftvalley, rightvalley, form_index, formant_frame, shift_const):
	resampledarray = []
	#To check if the shift diff is greater than the next formant 
	if len(formant_frame) > i: 
		if shift_const + form_index>formant_frame[i+1]:
			shift_const =  formant_frame[i+1]- form_index
	#To avoid resampling down to only one element
	if shift_const >= 0:
		checkthis = len(rightvalley)-shift_const
	else:
		checkthis = abs(len(rightvalley)+shift_const)
	if checkthis>1: # cannot resample down to one element 
		#negative = abs(len(rightvalley)+shift_const)>1 
		#positive = len(rightvalley)-shift_const > 1 or 
		if shift_const>= 0:
			left_array = signal.resample(leftvalley, abs(len(leftvalley)+shift_const))
			right_array= signal.resample(rightvalley, abs(len(rightvalley)-shift_const))
			#print(len(left_array)+len(right_array))
			#print(len(leftvalley)+len(rightvalley)) # make sure their dimension and preseved 
		else:
			left_array=signal.resample(leftvalley, abs(len(leftvalley)-shift_const))
			right_array= signal.resample(rightvalley, abs(len(rightvalley)+shift_const))
		resampledarray= np.append(left_array,right_array)
	return resampledarray

#FUNCTION 6: ZEROED FULL LENGTH SPEC ENV ARRAY 
#INPUT: PEAKLEFTINDEX, PEAKRIGHTINDEX, RESAAMPLED ARRAY, LEN(SPEC_ENV)
#OUTPUT: ZEROEDRESSAMPLEDARRAY, LEFTVALUEINDEX, RIGHTVALUEINDEX 
def zeroresampledarray(spec_env, leftvalue, rightvalue, shift_const, resampledarray):
	if shift_const>= 0:
		rightvalue = leftvalue+len(resampledarray)
	else:
		leftvalue = leftvalue-shift_const #what if leftvalue is 0 ?? 
		#leftvalue = leftvalue-len(resampledarray) --> could this be more appropriate
	zeroresampled_array = np.zeros(len(spec_env))
	zeroresampled_array[leftvalue:rightvalue] = resampledarray
	return zeroresampled_array, leftvalue, rightvalue

#FUNCTION 6: RANDOMLY PLOT ANY N NUMBER OF FRAMES SHOWING THE SHIFTS
#INPUT: PEAKLEFTINDEX, PEAKRIGHTINDEX, RESAAMPLED ARRAY, LEN(SPEC_ENV)
#OUTPUT: ZEROEDRESSAMPLEDARRAY, LEFTVALUEINDEX, RIGHTVALUEINDEX 
def randomlyplot(n, sp, shiftedspectrogram):
	x=np.random.randint(len(sp), size=n)
	for i in x:
		plt.plot(sp[i,:])
		plt.plot(shiftedspectrogram[i,:])
		plt.show()
########################################################################
#					MAIN FUNCTIONS							        #	
########################################################################

def shiftspectrogram(sp, formants_matrix, maximas,  nos_peaks, shift_array):
	shiftedspectrogram = []
	for i in np.arange(0,len(norm_formant_matrix)):
		formant_frame = norm_formant_matrix[i]
		maximas_frame = maximas[i][0]
		spec_env = sp[i,:]
		mintoloop = min([nos_peaks, len(formant_frame)])#incase number of maximas is les than mintoloop
		multi_shiftedarrays = []
		for j in np.arange(0,mintoloop):
			leftvalley,rightvalley,leftvalue, rightvalue = ppparray(spec_env, formant_frame[j], maximas_frame)
			resampledarray = resample(leftvalley, rightvalley, formant_frame[j], formant_frame, shift_array[j])
			zeroresampled_array, leftvalue, rightvalue = zeroresampledarray(spec_env, leftvalue, rightvalue, shift_array[j], resampledarray)
			multi_shiftedarrays.append(zeroresampled_array)
		#Maximum of all shifted arrays 
		shiftedspecframe = np.max(multi_shiftedarrays,axis=0)
		#Replace zeros with original spec envelope values
		for g in np.where(shiftedspecframe == 0)[0]:
			shiftedspecframe[g]=spec_env[g]
		shiftedspectrogram.append(shiftedspecframe)
	shiftedspectrogram = np.array(shiftedspectrogram)
	return shiftedspectrogram

########################################################################
#					TEST							        #	
########################################################################
#1. 
fm, ft = cam_formants(x, fs)
#2. 
formants = matrixformants(x, fs)
#3.
formants_matrix = func3(formants)
#4. 
maximas = func4(sp)
#5.
norm_formant_matrix = normalize_maximas(maximas, formants_matrix, frequency_scale)

#6. Builds new shifted spectrogram 
shiftedspectrogram = shiftspectrogram(sp, formants_matrix, maximas,  nos_peaks, shift_array)

#7. Randomly visualises n amount of spectrogram shifts
randomlyplot(15, sp, shiftedspectrogram)

#8. Synthesizes new audio 
#new_y = pw.synthesize(f0[0:len(f0)-1], shiftedspectrogram, ap[0:len(f0)-1], fs)
new_yy = pw.synthesize(f0, sp, ap, fs)
wav.write('orig_audio.wav',fs, new_yy)
new_y = pw.synthesize(f0[0:len(shiftedspectrogram)], shiftedspectrogram, ap[0:len(shiftedspectrogram)], fs)
wav.write('resynthesized_audio.wav',fs, new_y)
