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


pygame.display.set_mode((200, 200))
fs = 44100
pygame.mixer.init(frequency=fs)
pygame.mixer.set_num_channels(1)


def make_sound(freq1, freq2, mute1, mute2):
    global note
    duration1 = note
    duration2 = note
    
    # 生成时间轴数组
    t1 = np.arange(fs * duration1) / fs
    t2 = np.arange(fs * duration2) / fs
    
    # 初始化空的波形数组
    buf1 = np.zeros_like(t1, dtype=np.float32)
    buf2 = np.zeros_like(t2, dtype=np.float32)
    
    # === 修改部分：叠加高次谐波 ===
    # i=1 是基频，i=2,3,4,5 是泛音/高次谐频
    # (1.0 / i) 让高次谐波的音量逐渐减弱，产生类似管风琴/簧片乐器的丰富音色
    for i in range(1, 6):
        amplitude = 1.0 / i  
        buf1 += amplitude * np.sin(2 * np.pi * t1 * (freq1 * i))
        buf2 += amplitude * np.sin(2 * np.pi * t2 * (freq2 * i))
    # ==============================

    # reshape the waveform to have a second dimension of 1 for mono sound
    buf1 = np.reshape(buf1, (-1, 1))
    buf2 = np.reshape(buf2, (-1, 1))

    # normalize the waveform and convert to 16-bit integer
    # 使用 np.max(np.abs()) 进行归一化更安全，防止波形偏移导致破音
    buf1 *= 0.5 / np.max(np.abs(buf1))
    buf1 = (buf1 * 32767).astype(np.int16)
    
    buf2 *= 0.5 / np.max(np.abs(buf2))
    buf2 = (buf2 * 32767).astype(np.int16)
    
    if mute1:
        buf1 = 0 * buf1
    if mute2:
        buf2 = 0 * buf2

    buf = np.concatenate((buf1, buf2), axis=1)  # concatenate buf with a 2D array of zeros
    return buf

# create a Sound object from the waveform and play it indefinitely

def leftSing(freq,dura):
    buf = make_sound(freq,freq,False, False)
    sound = pygame.sndarray.make_sound(buf)
    sound.play(-1)
    time.sleep(dura)
    sound.stop()

# 打印频率表（可选）
# for i, name in enumerate(freqs):
#     print(name, freqs[name],'Hz')

# 播放《欢乐颂》
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
