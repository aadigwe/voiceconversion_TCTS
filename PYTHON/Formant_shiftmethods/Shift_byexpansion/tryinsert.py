import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

shift_const = 6
def interprolate(left_array, shift_const):
	y = left_array
	q = np.arange(len(y),dtype=float)
	for i in np.arange(len(y)):
		q[i] = float(y[i])
	k, m = divmod(len(q), shift_const)
	pos_nans = np.arange(1,len(q)-m, k)
	q = np.insert(q, pos_nans, np.nan)
	nans, x= nan_helper(q)
	q[nans]= np.interp(x(nans), x(~nans), q[~nans])
	diff = len(q) - len(y)
	return q, diff

def nan_helper(y):
    return np.isnan(y), lambda z: z.nonzero()[0]

def remove_elements(right_array, diff_const):
	q = right_array
	orig_length = len(q)
	k, m = divmod(len(q), diff_const)
	print('----')
	print(k)
	print('----')
	print(m)
	print('----')
	pos_nans = np.arange(1,len(q), m)
	print(pos_nans)
	new_array =np.delete(q, pos_nans)
	print('----')
	print(new_array)
	new_sig_size = orig_length-diff_const
	if new_sig_size != len(new_array):
		new_array = signal.resample(new_array, new_sig_size)
	return new_array



q=[2,4,6,8, 10,  28, 30, 32, 12, 14, 18, 20, 22, 24, 26, 34, 36, 38, 40, 42]
p = [22, 30, 32, 34, 36, 38, 24, 26, 28, 40, 42]
d, diff_const = interprolate(q, shift_const)
f = remove_elements(p, diff_const)


print(d)

plt.figure()
plt.plot(q+p, label="original")
plt.plot(np.append(d,f), label="modified")
plt.legend()
plt.show()

length = len(q)
print('Original array size:',length)
length2 = len(d)
print('expanded size:',length2)
print('Shift Constant:',shift_const)
print('difference in left', diff_const)
print('------REMOVE------------')
print('Original right size:',len(p))
print('compressed size:',len(f))
print('Shift Constant:',shift_const)
print(f)





