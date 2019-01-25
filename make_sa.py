#coding:utf-8

# making like /sa/ sound

import numpy as np
from scipy.io.wavfile import read as wavread
from scipy.io.wavfile import write as wavwrite
from matplotlib import pyplot as plt

# Check version
#  Python 3.6.4 on win32 (Windows 10)
#  numpy 1.14.0 
#  matplotlib  2.1.1
#  scipy 1.0.0


def load_wav(path0):
	sr, y = wavread(path0)
	y = y / (2 ** 15)
	print ('loading , sampling rate ', path0, sr)
	return y
	
def save_wav( yout, wav_path, sampling_rate=48000):
	wavwrite( wav_path, sampling_rate, ( yout * 2 ** 15).astype(np.int16))
	print ('save ', wav_path) 
	
def make_zero(duration, sampling_rate=48000):
	# duration unit is [msec]
	return np.zeros( int((duration / 1000.) * sampling_rate) )
	
def rfade_out(xin, duration=10, sampling_rate=48000):
	n= int((duration / 1000.) * sampling_rate)
	l0=len(xin)
	yout=np.copy(xin)
	if len(xin) > n:
		for i in range(n):
			yout[l0-1-i] = xin[l0-1-i] * ((1.0 * i ) / n)
	return yout
	
def ltrim(xin, thres=1.0):
	l0=len(xin)
	icode=0
	for i in range(l0):
		if xin[i] > (thres / (2 ** 15)):
			icode=i
			break
	yout=np.copy(xin[icode:])
	return yout
	
def plot_waveform(y1, label1, y2=None, label2=None, sampling_rate=48000):
	fig = plt.figure()
	plt.subplot(2,1,1)
	plt.xlabel('mSec')
	plt.ylabel('level')
	plt.title( label1 )
	plt.plot( (np.arange(len(y1)) * 1000.0 / sampling_rate) , y1)
	
	if y2 is not None:
		plt.subplot(2,1,2)
		plt.xlabel('mSec')
		plt.ylabel('level')
		plt.title( label2 )
		plt.plot( (np.arange(len(y2)) * 1000.0 / sampling_rate) , y2)
	
	fig.tight_layout()
	plt.show()


if __name__ == '__main__':
	
	# load high noise with resonance effect
	y1=load_wav( 's_noise_narrow_resona_0.wav' )
	y1fadeout=rfade_out(y1)
	plot_waveform(y1, 'input', y1fadeout,  'fadeout')
	
	# load  simulated opening mouth /a/
	y2=load_wav( 'yout_a_var.wav' )
	y2ltrim= ltrim(y2)
	plot_waveform(y2, 'input', y2ltrim,  'ltrim')
	
	# combining
	yout= np.concatenate( (y1fadeout, y2ltrim ) )
	plot_waveform(yout, 'Waveform combined (/sa/)')
	
	# save as a wav file
	save_wav(yout, 'sa_like.wav')

#This file uses TAB

