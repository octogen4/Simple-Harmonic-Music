import pygame
import numpy as np
import time
import sys

note = 2
note2=note/2
note4=note/4
note8=note/8

# The following code calculates the frequency values for the 12-tone equal temperament tuning system, also known as 12-tone equal temperament or 12-TET.
# In this system, the octave is divided into 12 equal parts, with each part being a semitone. 
# The frequency ratio between two adjacent semitones is the twelfth root of 2, which is approximately 1.0594630943592953.
# The frequency of A4 (the A above middle C) is usually set to 440 Hz in this system.

A4 = 440  # frequency of A4
C0 = A4 * pow(2, -4.75)  # frequency of C0
note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']  # list of note names
freqs = {}  # dictionary to store frequency values for each note

for i in range(9):  # iterate over octaves 0 to 8
    for j, name in enumerate(note_names):  # iterate over note names
        freq = C0 * pow(2, i + (j / 12))  # calculate frequency value
        freqs[name + str(i)] = freq  # store frequency value in dictionary with note name and octave number


# Example usage: freqs['A4'] returns the frequency of A4 in Hz. 

# To use these frequency values in the make_sound function, you can pass the desired frequency value as an argument to the function. 
# For example, to create a sound with the frequency of A4 for a duration of 1 second, you can call the function like this:

pygame.display.set_mode((200, 200))
fs = 44100
pygame.mixer.init(frequency=fs)
pygame.mixer.set_num_channels(1)


def make_sound(freq1,freq2,mute1,mute2):
    global note
    duration1=note
    duration2=note
    buf1 = np.sin(2 * np.pi * np.arange(fs * duration1) * freq1 / fs).astype(np.float32)
    buf2 = np.sin(2 * np.pi * np.arange(fs * duration2) * freq2 / fs).astype(np.float32)
# reshape the waveform to have a second dimension of 1 for mono sound
    buf1 = np.reshape(buf1, (-1, 1))
    buf2 = np.reshape(buf2, (-1, 1))

# normalize the waveform and convert to 16-bit integer
    buf1 *= 0.5 / np.max(buf1)
    buf1 = (buf1 * 32767).astype(np.int16)
    buf2 *= 0.5 / np.max(buf2)
    buf2 = (buf2 * 32767).astype(np.int16)
    if mute1:
        buf1=0*buf1
    if mute2:
        buf2=0*buf2

#buf = np.concatenate((buf, np.zeros_like(buf)), axis=1)  # concatenate buf with a 2D array of zeros
    buf = np.concatenate(( buf1,buf2), axis=1)  # concatenate buf with a 2D array of zeros
    return buf

# create a Sound object from the waveform and play it indefinitely

def leftSing(freq,dura):
    buf = make_sound(freq,freq,False, False)
    sound = pygame.sndarray.make_sound(buf)
    sound.play(-1)
    time.sleep(dura)
    sound.stop()

for i, name in enumerate(freqs):
    print(name, freqs[name],'Hz')
#    leftSing(freqs[name], note2)




leftSing(freqs['E5'], note4)
leftSing(freqs['E5'], note4)
leftSing(freqs['F5'], note4)
leftSing(freqs['G5'], note4)
leftSing(freqs['G5'], note4)
leftSing(freqs['F5'], note4)
leftSing(freqs['E5'], note4)
leftSing(freqs['D5'], note4)
leftSing(freqs['C5'], note4)
leftSing(freqs['C5'], note4)
leftSing(freqs['D5'], note4)
leftSing(freqs['E5'], note4)
leftSing(freqs['E5'], note4)
leftSing(freqs['D5'], note4)
leftSing(freqs['D5'], note4)

leftSing(freqs['E5'], note4)
leftSing(freqs['E5'], note4)
leftSing(freqs['F5'], note4)
leftSing(freqs['G5'], note4)
leftSing(freqs['G5'], note4)
leftSing(freqs['F5'], note4)
leftSing(freqs['E5'], note4)
leftSing(freqs['D5'], note4)
leftSing(freqs['C5'], note4)
leftSing(freqs['C5'], note4)
leftSing(freqs['D5'], note4)
leftSing(freqs['E5'], note4)
leftSing(freqs['D5'], note4)
leftSing(freqs['C5'], note4)
leftSing(freqs['C5'], note4)

leftSing(freqs['D5'], note4)
leftSing(freqs['D5'], note4)
leftSing(freqs['E5'], note4)
leftSing(freqs['C5'], note4)
leftSing(freqs['D5'], note4)
leftSing(freqs['E5'], note8)
leftSing(freqs['F5'], note8)
leftSing(freqs['E5'], note4)
leftSing(freqs['C5'], note4)
leftSing(freqs['D5'], note4)
leftSing(freqs['E5'], note8)
leftSing(freqs['F5'], note8)
leftSing(freqs['E5'], note4)
leftSing(freqs['D5'], note4)
leftSing(freqs['C5'], note4)
leftSing(freqs['D5'], note4)
leftSing(freqs['G4'], note4)

leftSing(freqs['E5'], note2)
leftSing(freqs['E5'], note4)
leftSing(freqs['F5'], note4)
leftSing(freqs['G5'], note4)
leftSing(freqs['G5'], note4)
leftSing(freqs['F5'], note4)
leftSing(freqs['E5'], note4)
leftSing(freqs['F5'], note8)
leftSing(freqs['D5'], note8)
leftSing(freqs['C5'], note4)
leftSing(freqs['C5'], note4)
leftSing(freqs['D5'], note4)
leftSing(freqs['E5'], note4)
leftSing(freqs['D5'], note4)
leftSing(freqs['C5'], note4)
leftSing(freqs['C5'], note4)

