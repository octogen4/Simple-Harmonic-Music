import pygame
import numpy as np
import time
import sys

note = 2
note2 = note/2
note4 = note/4
note8 = note/8

# 计算音符频率
A4 = 440
C0 = A4 * pow(2, -4.75)
note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
freqs = {}

for i in range(9):
    for j, name in enumerate(note_names):
        freq = C0 * pow(2, i + (j / 12))
        freqs[name + str(i)] = freq

pygame.display.set_mode((200, 200))
fs = 44100
pygame.mixer.init(frequency=fs)
pygame.mixer.set_num_channels(2)

# 定义和弦
chords = {
    'C': [freqs['C3'], freqs['E3'], freqs['G3']],      # C大三和弦
    'G': [freqs['G2'], freqs['B2'], freqs['D3']],      # G大三和弦
    'G7': [freqs['G2'], freqs['B2'], freqs['D3'], freqs['F3']],  # G7和弦
    'Am': [freqs['A2'], freqs['C3'], freqs['E3']],     # A小三和弦
    'F': [freqs['F2'], freqs['A2'], freqs['C3']],      # F大三和弦
    'Dm': [freqs['D3'], freqs['F3'], freqs['A3']],     # D小三和弦
}

def make_melody_sound(freq, duration):
    """生成主旋律音符"""
    buf = np.sin(2 * np.pi * np.arange(int(fs * duration)) * freq / fs).astype(np.float32)
    # 添加包络，使声音更自然
    envelope = np.ones_like(buf)
    fade_len = int(fs * 0.01)  # 10ms淡入淡出
    envelope[:fade_len] = np.linspace(0, 1, fade_len)
    envelope[-fade_len:] = np.linspace(1, 0, fade_len)
    buf *= envelope
    buf = np.reshape(buf, (-1, 1))
    buf *= 0.3 / (np.max(np.abs(buf)) + 0.001)
    buf = (buf * 32767).astype(np.int16)
    return buf

def make_chord_sound(chord_freqs, duration):
    """生成和弦伴奏"""
    buf = np.zeros(int(fs * duration), dtype=np.float32)
    for freq in chord_freqs:
        buf += np.sin(2 * np.pi * np.arange(int(fs * duration)) * freq / fs)
    # 添加包络
    envelope = np.ones_like(buf)
    fade_len = int(fs * 0.01)
    envelope[:fade_len] = np.linspace(0, 1, fade_len)
    envelope[-fade_len:] = np.linspace(1, 0, fade_len)
    buf *= envelope
    buf = np.reshape(buf, (-1, 1))
    buf *= 0.35 / (np.max(np.abs(buf)) + 0.001)  # 伴奏音量更小
    buf = (buf * 32767).astype(np.int16)
    return buf

def play_with_chord(melody_freq, chord_name, duration):
    """同时播放主旋律和和弦"""
    melody_buf = make_melody_sound(melody_freq, duration)
    chord_buf = make_chord_sound(chords[chord_name], duration)
    
    # 确保两个缓冲区长度相同
    min_len = min(len(melody_buf), len(chord_buf))
    melody_buf = melody_buf[:min_len]
    chord_buf = chord_buf[:min_len]
    
    # 合并左右声道：左声道是主旋律+和弦，右声道也是主旋律+和弦
    combined = melody_buf + chord_buf
    stereo_buf = np.concatenate((combined, combined), axis=1)
    
    sound = pygame.sndarray.make_sound(stereo_buf)
    sound.play()
    time.sleep(duration)
    sound.stop()

print("播放《欢乐颂》- 带和弦伴奏版本")
print("-" * 40)

# 第一段
play_with_chord(freqs['E5'], 'C', note4)
play_with_chord(freqs['E5'], 'C', note4)
play_with_chord(freqs['F5'], 'C', note4)
play_with_chord(freqs['G5'], 'C', note4)

play_with_chord(freqs['G5'], 'G', note4)
play_with_chord(freqs['F5'], 'G', note4)
play_with_chord(freqs['E5'], 'G', note4)
play_with_chord(freqs['D5'], 'G7', note4)

play_with_chord(freqs['C5'], 'C', note4)
play_with_chord(freqs['C5'], 'C', note4)
play_with_chord(freqs['D5'], 'C', note4)
play_with_chord(freqs['E5'], 'C', note4)

play_with_chord(freqs['E5'], 'G7', note4)
play_with_chord(freqs['D5'], 'G7', note4)
play_with_chord(freqs['D5'], 'C', note4)
time.sleep(note4)

# 第二段（重复，结尾不同）
play_with_chord(freqs['E5'], 'C', note4)
play_with_chord(freqs['E5'], 'C', note4)
play_with_chord(freqs['F5'], 'C', note4)
play_with_chord(freqs['G5'], 'C', note4)

play_with_chord(freqs['G5'], 'G', note4)
play_with_chord(freqs['F5'], 'G', note4)
play_with_chord(freqs['E5'], 'G', note4)
play_with_chord(freqs['D5'], 'G7', note4)

play_with_chord(freqs['C5'], 'C', note4)
play_with_chord(freqs['C5'], 'C', note4)
play_with_chord(freqs['D5'], 'C', note4)
play_with_chord(freqs['E5'], 'C', note4)

play_with_chord(freqs['D5'], 'G', note4)
play_with_chord(freqs['C5'], 'C', note4)
play_with_chord(freqs['C5'], 'C', note4)
time.sleep(note4)

# 中间段
play_with_chord(freqs['D5'], 'G', note4)
play_with_chord(freqs['D5'], 'G', note4)
play_with_chord(freqs['E5'], 'G', note4)
play_with_chord(freqs['C5'], 'C', note4)

play_with_chord(freqs['D5'], 'G', note4)
play_with_chord(freqs['E5'], 'C', note8)
play_with_chord(freqs['F5'], 'C', note8)
play_with_chord(freqs['E5'], 'C', note4)
play_with_chord(freqs['C5'], 'C', note4)

play_with_chord(freqs['D5'], 'G', note4)
play_with_chord(freqs['E5'], 'G', note8)
play_with_chord(freqs['F5'], 'G', note8)
play_with_chord(freqs['E5'], 'C', note4)
play_with_chord(freqs['D5'], 'G', note4)

play_with_chord(freqs['C5'], 'C', note4)
play_with_chord(freqs['D5'], 'G', note4)
play_with_chord(freqs['G4'], 'G7', note4)
time.sleep(note4)

# 最后一段
play_with_chord(freqs['E5'], 'C', note2)
play_with_chord(freqs['E5'], 'C', note4)
play_with_chord(freqs['F5'], 'C', note4)

play_with_chord(freqs['G5'], 'G', note4)
play_with_chord(freqs['G5'], 'G', note4)
play_with_chord(freqs['F5'], 'G', note4)
play_with_chord(freqs['E5'], 'G7', note4)

play_with_chord(freqs['F5'], 'C', note8)
play_with_chord(freqs['D5'], 'C', note8)
play_with_chord(freqs['C5'], 'C', note4)
play_with_chord(freqs['C5'], 'C', note4)
play_with_chord(freqs['D5'], 'C', note4)
play_with_chord(freqs['E5'], 'C', note4)

play_with_chord(freqs['D5'], 'G', note4)
play_with_chord(freqs['C5'], 'C', note4)
play_with_chord(freqs['C5'], 'C', note4)
time.sleep(note4)

print("播放完毕！")
pygame.quit()
