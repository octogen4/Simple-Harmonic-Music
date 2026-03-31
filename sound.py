import pygame
import numpy as np
import time

pygame.display.set_mode((200, 200))
fs = 44100
pygame.mixer.init(frequency=fs)
pygame.mixer.set_num_channels(1)

duration = 100  # duration of the sound in seconds
freq1 = 680  # frequency of the sine wave in Hz
freq2 = 680
phi1=0
phi2=np.pi*1 #2*np.pi #np.pi*89/100
buf1 = np.sin(2*np.pi*np.arange(fs*duration)*freq1/fs+phi1).astype(np.float32)
buf2 = np.sin(2*np.pi*np.arange(fs*duration)*freq2/fs+phi2).astype(np.float32)
# reshape the waveform to have a second dimension of 1 for mono sound
buf1 = np.reshape(buf1, (-1, 1))
buf2 = np.reshape(buf2, (-1, 1))

# normalize the waveform and convert to 16-bit integer
buf1 *= 0.5 / np.max(buf1)
buf1 = (buf1 * 32767).astype(np.int16)
buf2 *= 0.5 / np.max(buf2)
buf2 = (buf2 * 32767).astype(np.int16)

buf1 = buf1+buf2
buf2 = 0*buf2

#buf = np.concatenate((buf, np.zeros_like(buf)), axis=1)  # concatenate buf with a 2D array of zeros
buf = np.concatenate((buf1,buf2), axis=1)  # concatenate buf with a 2D array of zeros
# create a Sound object from the waveform and play it indefinitely
sound = pygame.sndarray.make_sound(buf)
sound.play(-1)

time.sleep(300)
