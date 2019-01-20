import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import signal
from scipy.signal import argrelmin
from scipy.signal import argrelmax


x= [ 64,  18, 12,  31,  85,  91,  19,   4,  64,  83,  21,  43,  79,  80,  87,
  48,  23,   7,  19,  60,  49,  75,  23,  36,  54,  10,  94,  49,  32,   4,
  34,  37,  63,  10,  81,  20,  52,   8,  67,  46]



y = signal.resample(x, 80)


maximas = argrelmax(y)
maximas = maximas[0]
minimas = argrelmin(y)
minimas = minimas[0]
print(y)
print(maximas)
print(minimas)

#Variable Parameters
shift_const = 3
formant_index = maximas[1]
Shift_constarray = [ 5, 2, -5]
nos_peaks = 3 

########################################################################
#					HELPER FUNCTIONS 								   #	
########################################################################

def vpvarray(form_index,minimas, y):
	#vpv = valley-peak-valley peakarray
	leftvalley = [i for i in minimas if i < form_index]
	leftvalue = np.argmin(abs(leftvalley - form_index))
	leftvalue = leftvalley[leftvalue]
	rightvalley = [i for i in minimas if i > form_index]
	rightvalue = np.argmin(abs(rightvalley - form_index))
	rightvalue = rightvalley[rightvalue]
	peakarray = y[leftvalue:rightvalue+1]
	print(y[form_index])
	print(leftvalue)
	print(rightvalue)
	print(peakarray)
	
def ppparray(form_index,maximas, y):
	#ppp - leftpeak-peak-rightpeakarray
	#Uses list comprehension to split the array to the left and right of the 
	#formant index and find the min absolute difference
	#returns the ppp array values
	leftvalley = [i for i in maximas if i < form_index]
	leftvalue = np.argmin(abs(leftvalley - form_index))
	leftvalue = leftvalley[leftvalue]
	leftvalley = y[leftvalue:form_index]
	rightvalley = [i for i in maximas if i > form_index]
	rightvalue = np.argmin(abs(rightvalley - form_index))
	rightvalue = rightvalley[rightvalue]
	rightvalley = y[form_index:rightvalue+1]
	peakarray = y[leftvalue:rightvalue+1]
	print(leftvalley)
	print(rightvalley)
	print(peakarray)
	return leftvalley,rightvalley, leftvalue, rightvalue
	#print(y[form_index])
	#print(form_index)
	#print(leftvalue)
	#print(rightvalue)
	#print(peakarray)

#GOT THIS FROM STACKOVERFLOW SRC IN DOCUMENTATION
def nan_helper(y):
    """Helper to handle indices and logical indices of NaNs.
    Source stackoverflow https://stackoverflow.com/questions/6518811/interpolate-nan-values-in-a-numpy-array

    Input:
        - y, 1d numpy array with possible NaNs
    Output:
        - nans, logical indices of NaNs
        - index, a function, with signature indices= index(logical_indices),
          to convert logical indices of NaNs to 'equivalent' indices
    Example:
        >>> # linear interpolation of NaNs
        >>> nans, x= nan_helper(y)
        >>> y[nans]= np.interp(x(nans), x(~nans), y[~nans])
    """

    return np.isnan(y), lambda z: z.nonzero()[0]
########################################################################
#					SHIFT METHODS 									   #	
########################################################################
def resample(leftvalley, rightvalley, shift_const):
	if shift_const>= 0:
		print(1)
		left_array = signal.resample(leftvalley, len(leftvalley)+shift_const)
		right_array= signal.resample(rightvalley, len(rightvalley)-shift_const)
	else:
		print(0)
		left_array=signal.resample(leftvalley, len(leftvalley)-abs(shift_const))
		right_array= signal.resample(rightvalley, len(rightvalley)+abs(shift_const))
	return left_array,right_array



def interprolate(left_array, shift_const):
	y = left_array
	q = np.arange(len(y),dtype=float)
	for i in np.arange(len(y)):
		q[i] = float(y[i])
	k, m = divmod(len(q), shift_const)
	pos_nans = np.arange(1,len(q), k)
	q = np.insert(q, pos_nans, np.nan)
	nans, x= nan_helper(q)
	q[nans]= np.interp(x(nans), x(~nans), q[~nans])
	return q


def remove(right_array, shiftconst):
	q = right_array
	k, m = divmod(len(q), shift_const)
	pos_nans = np.arange(1,len(q), k)
	new_array =np.delete(q, pos_nans)
	return new_array


def insertshiftedarray(y, shift_const, form_index):
	new_array = np.zeros(len(y))
	print(new_array)

#RUNS
#vpvarray(formant_index,minimas, y)
#expand_compress(y, -1)
#fill_remove(y, shift_const, formant_index)

########################################################################
#					TEST EACH SHIFT 								#	
########################################################################
leftvalley,rightvalley, leftvalue, rightvalue = ppparray(formant_index,maximas, y)
left_array,right_array = resample(leftvalley, rightvalley, shift_const)
print('-----------------------------------------------------')
print(leftvalley)
print(left_array)
print('-----------------------------------------------------')
print(rightvalley)
print(right_array)
print('----#####-----#####-----------#####--------#####----------#####-------------')
left_valley = interprolate(leftvalley, shift_const)
ryt_valley = remove(rightvalley, shift_const)
print(left_valley)
print(ryt_valley)
print(np.append(left_array,right_array))
print(np.append(left_valley,ryt_valley))

plt.figure()
plt.plot(np.append(leftvalley,rightvalley))
plt.plot(np.append(left_array,right_array))
plt.plot(np.append(left_valley,ryt_valley))
plt.axvline(x=4, color='k', linestyle='--')
plt.show()

########################################################################
#					MAIN MULTI FORMANTS								#	
########################################################################
#Variable Parameters
shift_const = 3
formant_index = maximas[7]
nos_peaks = 3 

formant_indexarray = maximas[1:4]
Shift_constarray = [ 5, 2, -5]


# Sub-frame 
def frameshift(Shift_constarray, spec_env, nos_peaks):
	for i in np.arange(1, nos_peaks+1):
		leftvalley,rightvalley, leftvalue, rightvalue = ppparray(maximas[i],maximas, spec_env)
		left_array,right_array = resample(leftvalley, rightvalley, shift_const)	
		left_array.append(right_array)
		#starting at the left peak write all the new values 
		#create zero arrays and fill
		#do the same for all other formants 
	
def main(Shift_constarray, spectrogram, nos_peaks):
	new_spectrogram = []
	for i in np.arange(0, len(spectrogram)):
		new_specenv = frameshift(Shift_constarray, spec_env[i], nos_peaks)
		new_spectrogram.append(new_specenv)




