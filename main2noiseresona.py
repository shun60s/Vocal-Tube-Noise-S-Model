#coding:utf-8

#
# apply two tube model resonance effect to noise sound
#

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as patches
from scipy.io.wavfile import write as wavwrite

# alternative choice, twotube.py or twotube_downmix.py
from twotube import *
#from twotube_downmix import *


from glottal import *
from load_sourcewav import *
from HPF import *

# Check version
#  Python 3.6.4 on win32 (Windows 10)
#  numpy 1.14.0 
#  matplotlib  2.1.1
#  scipy 1.0.0


def plot_freq_res(twotube, label, glo, hpf):
	plt.xlabel('Hz')
	plt.ylabel('dB')
	plt.title(label)
	amp0, freq=glo.H0(freq_high=10000, Band_num=512)
	amp1, freq=twotube.H0(freq_high=10000, Band_num=512)
	amp2, freq=hpf.H0(freq_high=10000, Band_num=512)
	plt.plot(freq, (amp0+amp1+amp2))

def plot_waveform(twotube, label, glo, hpf):
	# you can get longer input source to set bigger repeat_num 
	yg_repeat=glo.make_N_repeat(repeat_num=1) # input source of two tube model
	y2tm=twotube.process(yg_repeat)
	yout=hpf.iir1(y2tm)
	plt.xlabel('mSec')
	plt.ylabel('level')
	plt.title('Waveform')
	plt.plot( (np.arange(len(yout)) * 1000.0 / glo.sr) , yout)
	return yout

def save_wav( yout, wav_path, sampling_rate=48000):
	wavwrite( wav_path, sampling_rate, ( yout * 2 ** 15).astype(np.int16))
	print ('save ', wav_path) 

def f_show( twotube, i):
	plt.subplot(MAX_PATTERNS * 2 ,1,int(2*i+1))
	plot_freq_res(twotube, 'Frequency response (whole span) '+str(i), glo, hpf)
	plt.subplot(MAX_PATTERNS * 2 ,1,int(2*i+2))
	yout=plot_waveform(twotube, 'Waveform', glo, hpf)
	return yout
	
def get_A2( A1, r1):
		# return cross section area A2 to meet the reflection ratio r1
		return ((1.0 + r1)/(1.0 - r1)) * A1

if __name__ == '__main__':
	
	MAX_PATTERNS=1  # number of display patterns
	
	# set some initial value
	"""
	# /u/ reference
	L1_u=10.0   # set list of 1st tube's length by unit is [cm]
	A1_u=7.0    # set list of 1st tube's area by unit is [cm^2]
	L2_u=7.0    # set list of 2nd tube's length by unit is [cm]
	A2_u=3.0    # set list of 2nd tube's area by unit is [cm^2]
	"""
	L1=np.ones(MAX_PATTERNS) * 10.0
	A1=np.ones(MAX_PATTERNS) * 7.0
	L2=np.ones(MAX_PATTERNS) * 7.0
	A2=np.ones(MAX_PATTERNS) * 3.0
	
	# get cross section area to specify reflection ratio
	A2[0]= get_A2( A1[0], -0.6)
	
	# set 1st and 2nd tube's length
	L1[0]=3.5
	L2[0]=2.5
	
	# load a wav file as source source
	glo=Class_WavSource('s_noise_narrow.wav') # instance noise sound
	hpf=Class_HPF()       # instance for mouth radiation effect
	
	# draw
	fig = plt.figure()
	
	# to search good pattern to fit /su/ sound by audition
	for i in range(MAX_PATTERNS): 
		twotube=  Class_TwoTube(L1[i],L2[i],A1[i],A2[i])
		print ('r1, L1, L2', twotube.r1, L1[i], L2[i])
		yout=f_show( twotube, i)
		wavname='s_noise_narrow_resona_' + str(i)+ '.wav'
		save_wav(yout, wavname)  # save generated waveform as a wav file
	
	fig.tight_layout()
	plt.show()
	
	
#This file uses TAB

