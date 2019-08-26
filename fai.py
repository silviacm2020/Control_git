import pyaudio  
import wave
import random
import numpy as np
import cv2
import struct
import math

#define stream chunk   
chunk = 1024
SHORT_NORMALIZE = (1.0/32768.0)

#open a wav format music  
f = wave.open("samples/FAI_amplified.wav","rb")
#f = wave.open("samples/sample.wav","rb")

#instantiate PyAudio  
p = pyaudio.PyAudio()  

#open stream  
stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                channels = f.getnchannels(),  
                rate = f.getframerate(),  
                output = True)  

#read data  
img = np.zeros([512, 512, 3], np.uint8)
data = f.readframes(chunk)  



def get_rms( block ):
    # RMS amplitude is defined as the square root of the 
    # mean over time of the square of the amplitude.
    # so we need to convert this string of bytes into 
    # a string of 16-bit samples...

    # we will get one short out for each 
    # two chars in the string.
    count = len(block)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, block )

    # iterate over the block.
    sum_squares = 0.0
    for sample in shorts:
        # sample is a signed short in +/- 32768. 
        # normalize it to 1.0
        n = sample * SHORT_NORMALIZE
        sum_squares += n*n

    return math.sqrt( sum_squares / count )

def hex_color(data_str,color):
    if color=="r":
        return int(data_str[0:2],16)
    elif color=="g":
        return int(data_str[2:4],16)
    elif color=="b":
        return int(data_str[4:6],16)

#play stream
vel = 1
while len(data) > 0: 
    cv2.imshow('FAI', img)
    cv2.waitKey(1)
    hex = str(data.hex())
    if get_rms(data)>0.03:
        vel = 30
    elif get_rms(data)>0.015 and get_rms(data)<=0.03:
        vel = 10
    elif get_rms(data)>0.010 and get_rms(data)<=0.015:
        vel = 1
    elif get_rms(data)<=0.010:
        vel = 0
    for i in range(0,vel):
        data_aux = hex[i*16:(i*16)+16]
        red = hex_color(data_aux,"r")
        green = hex_color(data_aux,"g")
        blue = hex_color(data_aux,"b")
        img = cv2.circle(img, (random.randint(0,512), random.randint(0,512)), random.randint(0,(vel*3)+100), (red, green, blue), -1)
    stream.write(data)
    data = f.readframes(chunk)
    
   
#stop stream  
stream.stop_stream()  
stream.close()  

#close PyAudio  
p.terminate()   
cv2.destroyAllWindows() 






