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


path = "SpkBeng_0010.wav"
x, fs = sf.read('aaa.wav')  
#fs, x = wav.read(path)
print(x.shape)
f0, t = pw.dio(x, fs, f0_floor=50.0, f0_ceil=600.0)
sp = pw.cheaptrick(x, f0, t, fs)
ap = pw.d4c(x, f0, t, fs)
f0_low_limit = 89
fft_size= 2**math.ceil(np.log2(3 * fs / f0_low_limit + 1))
frequency_axis=np.arange(0, fft_size+1)/fft_size*fs
#shift_array = [7, 11, 17]
shift_array = [27, 21, 27]
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
			#frqs = frqs[0:4] #limited to four formants
			#print(frqs[0:4])

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
		#print(maximas)
		#print(sp[i,maximas])
	return(maximas)

###IMPORTANT - GIVES THE INDEX OF THE MAXIMAS THAT ARE NEAREST THE FORMANTS
def normalize_maximas(maximas, formants_matrix, frequency_scale):
	norm_formant_matrix = []
	for i in np.arange(0, len(formants_matrix)): #length 159
		maximas_frame = maximas[i][0]
		#print(maximas_frame)
		#print(formants_matrix[i])
		#print(np.array(formants_matrix[i])/frequency_scale)
		norm_formant_frame= []
		for j in np.arange(0, len(formants_matrix[i])):
			#print(round(formants_matrix[i][j]/frequency_scale)) #rounded scaled formants
			#print(np.argmin(abs(maximas[i] -round(formants_matrix[i][j]/frequency_scale))))
			norm_formant_frame.append(np.argmin(abs(maximas[i] -round(formants_matrix[i][j]/frequency_scale))))
		#print(norm_formant_frame)
		#print(maximas_frame[norm_formant_frame])
		#print(np.unique(maximas_frame[norm_formant_frame]))
		norm_formant_matrix.append(np.unique(maximas_frame[norm_formant_frame]))
		#print('++++++++++++++')
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
	print('Start here')
	print(maximas)
	leftvalley = [i for i in maximas if i < form_index]
	if len(leftvalley)==0: #if array is empty make it the first element
		print('yes left valley is empty')
		leftvalue = 0
	else:
		leftvalue = np.argmin(abs(leftvalley - form_index))
		leftvalue = leftvalley[leftvalue]
	print(leftvalue)
	leftvalley = spec_env[leftvalue:form_index]
	leftvalley = np.append(leftvalley, spec_env[form_index])
	print(leftvalley)
	rightvalley = [i for i in maximas if i > form_index]
	print(rightvalley)
	rightvalue = np.argmin(abs(rightvalley - form_index))
	rightvalue = rightvalley[rightvalue]
	print(rightvalue)
	rightvalley = spec_env[form_index:rightvalue+1]
	print(rightvalley)
	print(form_index)	#peakarray = spec_env[leftvalue:rightvalue+1]
	return leftvalley,rightvalley, leftvalue, rightvalue

#FUNCTION 5: INTRODUCES NAN FOR INTERPROLATION
def nan_helper(y):
    return np.isnan(y), lambda z: z.nonzero()[0]

#FUNCTION 6: EXPANDED ARRAY BY + SHIFT CONST
#INPUT: ARRAY TO BE EXPANDED
#OUTPUT: EXPANDED ARRAY, DIFFERENCE TO BE REMOVED
def interprolate(left_array, shift_const):
	y = left_array
	q = np.arange(len(y),dtype=float)
	for i in np.arange(len(y)):
		q[i] = float(y[i])
	k, m = divmod(len(q), shift_const)
	print(m)
	print(k)
	print(len(q))
	if k == 0:######!!!!!!!!!!!!!####
		k = 1 ######!!!!!!!!!!!!!####
	pos_nans = np.arange(1,len(q)-m, k)
	q = np.insert(q, pos_nans, np.nan)
	nans, x= nan_helper(q)
	q[nans]= np.interp(x(nans), x(~nans), q[~nans])
	diff = len(q) - len(y)
	return q, diff

#FUNCTION 7: COMPRESSES ARRAY BY EXPANDED DIFFERENCE
#INPUT: ARRAY TO BE COMPRESSED
#OUTPUT: COMPRESSED ARRAY
def remove_elements(right_array, diff_const):
	q = right_array
	orig_length = len(q)
	print(diff_const)
	print(len(q))
	if diff_const == 0:
		diff_const = 1
	k, m = divmod(len(q), diff_const)
	if k == 0: ######!!!!!!!!!!!!!####
		k = 1 ######!!!!!!!!!!!!!####
	pos_nans = np.arange(1,len(q), k)
	comp_array =np.delete(q, pos_nans)
	new_sig_size = orig_length-diff_const
	if new_sig_size != len(comp_array):
		print(new_sig_size)
		if new_sig_size < 2:######!!!!!!!!!!!!!####
			new_sig_size = 2######!!!!!!!!!!!!!####
		comp_array = signal.resample(comp_array, new_sig_size)
	return comp_array


#FUNCTION 6: ZEROED FULL LENGTH SPEC ENV ARRAY 
#INPUT: PEAKLEFTINDEX, PEAKRIGHTINDEX, RESAAMPLED ARRAY, LEN(SPEC_ENV)
#OUTPUT: ZEROEDRESSAMPLEDARRAY 
def zeroresampledarray(spec_env, leftvalue, rightvalue, shift_const, exp_comparray):
	print(leftvalue)
	print(rightvalue)
	print(len(resampledarray))
	if shift_const>= 0:
		#rightvalue = rightvalue+shift_const
		print('yes')
	else:
		leftvalue = leftvalue-shift_const #what if leftvalue is 0 ?? 
	zeroresampled_array = np.zeros(len(spec_env))
	print(len(zeroresampled_array))
	print(type(resampledarray))
	rightvalue = leftvalue+len(resampledarray)
	print(len(zeroresampled_array[leftvalue:rightvalue]))
	print(leftvalue)
	print(rightvalue-1)
	zeroresampled_array[leftvalue:rightvalue] = resampledarray
	print('passed this section')
	return zeroresampled_array, leftvalue, rightvalue
########################################################################
#					MAIN FUNCTIONS							        #	
########################################################################

def shiftspectrogram(sp, formants_matrix, maximas,  nos_peaks, shift_array):
	shiftedspectrogram = []
	for i in np.arange(0,len(sp)):
		spec_env = sp[i,:]
		maximas = maximas[i][0]
		shiftedspecframe = []
		for j in np.arange(0,nos_peaks):
			leftvalley,rightvalley = ppparray(spec_env, formants_matrix[j], maximas)
			resampledarray = resample(leftvalley, rightvalley, shift_const[j])
			zeroresampledarray = zeroresampledarray(peakleftindex, peakrightindex[-1], resampledarray)
		shiftedspecframe = np.max(multi_shiftedarrays,axis=0)
		for g in np.where(shiftedspecframe == 0)[0]:
			shiftedspecframe[g]=test[g]
		shiftedspectrogram.append(shiftedspecframe)
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

print(len(formants))
print(len(formants_matrix))
print(len(norm_formant_matrix))
print(len(maximas))

shiftedspectrogram = []
for i in np.arange(0,len(norm_formant_matrix)):
	formant_frame = norm_formant_matrix[i]
	print(formant_frame)
	maximas_frame = maximas[i][0]
	print(maximas_frame)
	spec_env = sp[i,:]
	mintoloop = min([nos_peaks, len(formant_frame)])#incase number of maximas is les than mintoloop
	multi_shiftedarrays = []
	for j in np.arange(0,mintoloop):
		leftvalley,rightvalley,leftvalue, rightvalue = ppparray(spec_env, formant_frame[j], maximas_frame)
		exp_array, comp_const = interprolate(leftvalley, shift_array[j])
		comp_array=remove_elements(rightvalley, comp_const)
		resampledarray = np.append(exp_array, comp_array)
		zeroresampled_array, leftvalue, rightvalue = zeroresampledarray(spec_env, leftvalue, rightvalue, shift_array[j], resampledarray)
		multi_shiftedarrays.append(zeroresampled_array)
	print(len(multi_shiftedarrays))
	#Maximum of all shifted arrays 
	shiftedspecframe = np.max(multi_shiftedarrays,axis=0)
	#Replace zeros with original spec envelope values
	for g in np.where(shiftedspecframe == 0)[0]:
		shiftedspecframe[g]=spec_env[g]
	shiftedspectrogram.append(shiftedspecframe)
	print(i)
	print('######################')
shiftedspectrogram = np.array(shiftedspectrogram)

def randomlyplot(n, sp, shiftedspectrogram):
	x=np.random.randint(len(sp), size=n)
	for i in x:
		plt.plot(sp[i,:])
		plt.plot(shiftedspectrogram[i,:])
		plt.show()

randomlyplot(15, sp, shiftedspectrogram)

#new_y = pw.synthesize(f0[0:len(f0)-1], shiftedspectrogram, ap[0:len(f0)-1], fs)
new_y = pw.synthesize(f0[0:len(shiftedspectrogram)], shiftedspectrogram, ap[0:len(shiftedspectrogram)], fs)
new_yy = pw.synthesize(f0, sp, ap, fs)
wav.write('orig_audio.wav',fs, new_yy)
wav.write('resynthesized_audio.wav',fs, new_y)
