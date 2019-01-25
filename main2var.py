#coding:utf-8

#
# variable two tube model, draw waveform, considering glottal voice source and mouth radiation
#                          save generated waveform as a wav file

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as patches
from scipy.io.wavfile import write as wavwrite
from twotubevariable import *
from glottal import *
from HPF import *
from tube_A1 import *

# Check version
#  Python 3.6.4 on win32 (Windows 10)
#  numpy 1.14.0 
#  matplotlib  2.1.1
#  scipy 1.0.0


def plot_freq_res(twotube, label, glo, hpf):
	plt.xlabel('Hz')
	plt.ylabel('dB')
	plt.title(label)
	amp0, freq=glo.H0(freq_high=5000, Band_num=256)
	amp1, freq=twotube.H0(freq_high=5000, Band_num=256)
	amp2, freq=hpf.H0(freq_high=5000, Band_num=256)
	plt.plot(freq, (amp0+amp1+amp2))

def plot_waveform(twotube, label, glo, hpf, repeat_num=5):
	# you can get longer input source to set bigger repeat_num 
	yg_repeat=glo.make_N_repeat(repeat_num) # input source of two tube model
	y2tm=twotube.process(yg_repeat)
	yout=hpf.iir1(y2tm)
	plt.xlabel('mSec')
	plt.ylabel('level')
	plt.title( label )
	plt.plot( (np.arange(len(yout)) * 1000.0 / glo.sr) , yout)
	return yout

def save_wav( yout, wav_path, sampling_rate=48000):
	wavwrite( wav_path, sampling_rate, ( yout * 2 ** 15).astype(np.int16))
	print ('save ', wav_path) 

if __name__ == '__main__':
	
	# instance
	A=Class_A()  # simulated opening mouth /a/
	A.draw_cross_section_area()
	A.f_show_all()
	
	# instance variable two tube model
	tube=Class_TwoTube_variable( A )
	
	glo=Class_Glottal()   # instance as glottal voice source
	hpf=Class_HPF()       # instance for mouth radiation effect
	
	# draw
	fig = plt.figure()
	
	# /a/
	plt.subplot(2,1,1)
	yout_a=plot_waveform(tube, 'Waveform  (Mouth open toward /a/)', glo, hpf, repeat_num=13)
	save_wav(yout_a, 'yout_a_var.wav')  # save generated waveform as a wav file
	plt.subplot(2,1,2)
	plot_freq_res(tube, 'frequency response at target', glo, hpf)
	#
	fig.tight_layout()
	plt.show()
	
#This file uses TAB

