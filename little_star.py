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

# 定义分解和弦（琶音）模式
arpeggio_patterns = {
    'C': [freqs['C3'], freqs['G3'], freqs['E3'], freqs['G3']],
    'F': [freqs['F2'], freqs['C3'], freqs['A2'], freqs['C3']],
    'G': [freqs['G2'], freqs['D3'], freqs['B2'], freqs['D3']],
    'G7': [freqs['G2'], freqs['D3'], freqs['F3'], freqs['B2']],
}

def make_melody_sound(freq, duration):
    """生成主旋律音符"""
    buf = np.sin(2 * np.pi * np.arange(int(fs * duration)) * freq / fs).astype(np.float32)
    envelope = np.ones_like(buf)
    fade_len = int(fs * 0.01)
    envelope[:fade_len] = np.linspace(0, 1, fade_len)
    envelope[-fade_len:] = np.linspace(1, 0, fade_len)
    buf *= envelope
    buf = np.reshape(buf, (-1, 1))
    buf *= 0.3 / (np.max(np.abs(buf)) + 0.001)
    buf = (buf * 32767).astype(np.int16)
    return buf

def make_arpeggio_sound(arpeggio_freqs, total_duration):
    """生成分解和弦（琶音）"""
    note_duration = total_duration / len(arpeggio_freqs)
    buf = np.array([], dtype=np.float32)
    
    for freq in arpeggio_freqs:
        note_buf = np.sin(2 * np.pi * np.arange(int(fs * note_duration)) * freq / fs)
        # 为每个音符添加包络
        envelope = np.ones_like(note_buf)
        fade_len = int(fs * 0.005)
        envelope[:fade_len] = np.linspace(0, 1, fade_len)
        envelope[-fade_len:] = np.linspace(1, 0, fade_len)
        note_buf *= envelope
        buf = np.concatenate([buf, note_buf])
    
    buf = np.reshape(buf, (-1, 1))
    buf *= 0.2 / (np.max(np.abs(buf)) + 0.001)
    buf = (buf * 32767).astype(np.int16)
    return buf

def play_with_arpeggio(melody_freq, arpeggio_name, duration):
    """同时播放主旋律和分解和弦"""
    melody_buf = make_melody_sound(melody_freq, duration)
    arpeggio_buf = make_arpeggio_sound(arpeggio_patterns[arpeggio_name], duration)
    
    # 确保两个缓冲区长度相同
    min_len = min(len(melody_buf), len(arpeggio_buf))
    melody_buf = melody_buf[:min_len]
    arpeggio_buf = arpeggio_buf[:min_len]
    
    # 混合主旋律和琶音
    combined = melody_buf + arpeggio_buf
    stereo_buf = np.concatenate((combined, combined), axis=1)
    
    sound = pygame.sndarray.make_sound(stereo_buf)
    sound.play()
    time.sleep(duration)
    sound.stop()

print("播放《小星星》- 分解和弦伴奏版本")
print("-" * 40)

# 第一段：Twinkle twinkle little star
play_with_arpeggio(freqs['C5'], 'C', note4)  # Twink-
play_with_arpeggio(freqs['C5'], 'C', note4)  # le
play_with_arpeggio(freqs['G5'], 'C', note4)  # twink-
play_with_arpeggio(freqs['G5'], 'C', note4)  # le

play_with_arpeggio(freqs['A5'], 'F', note4)  # lit-
play_with_arpeggio(freqs['A5'], 'F', note4)  # tle
play_with_arpeggio(freqs['G5'], 'C', note2)  # star

# 第二段：How I wonder what you are
play_with_arpeggio(freqs['F5'], 'F', note4)
play_with_arpeggio(freqs['F5'], 'F', note4)
play_with_arpeggio(freqs['E5'], 'C', note4)
play_with_arpeggio(freqs['E5'], 'C', note4)

play_with_arpeggio(freqs['D5'], 'G', note4)
play_with_arpeggio(freqs['D5'], 'G', note4)
play_with_arpeggio(freqs['C5'], 'C', note2)

# 第三段：Up above the world so high
play_with_arpeggio(freqs['G5'], 'C', note4)
play_with_arpeggio(freqs['G5'], 'C', note4)
play_with_arpeggio(freqs['F5'], 'F', note4)
play_with_arpeggio(freqs['F5'], 'F', note4)

play_with_arpeggio(freqs['E5'], 'C', note4)
play_with_arpeggio(freqs['E5'], 'C', note4)
play_with_arpeggio(freqs['D5'], 'G', note2)

# 第四段：Like a diamond in the sky
play_with_arpeggio(freqs['G5'], 'C', note4)
play_with_arpeggio(freqs['G5'], 'C', note4)
play_with_arpeggio(freqs['F5'], 'F', note4)
play_with_arpeggio(freqs['F5'], 'F', note4)

play_with_arpeggio(freqs['E5'], 'C', note4)
play_with_arpeggio(freqs['E5'], 'C', note4)
play_with_arpeggio(freqs['D5'], 'G', note2)

# 第五段：Twinkle twinkle little star（重复第一段）
play_with_arpeggio(freqs['C5'], 'C', note4)
play_with_arpeggio(freqs['C5'], 'C', note4)
play_with_arpeggio(freqs['G5'], 'C', note4)
play_with_arpeggio(freqs['G5'], 'C', note4)

play_with_arpeggio(freqs['A5'], 'F', note4)
play_with_arpeggio(freqs['A5'], 'F', note4)
play_with_arpeggio(freqs['G5'], 'C', note2)

# 第六段：How I wonder what you are（重复第二段）
play_with_arpeggio(freqs['F5'], 'F', note4)
play_with_arpeggio(freqs['F5'], 'F', note4)
play_with_arpeggio(freqs['E5'], 'C', note4)
play_with_arpeggio(freqs['E5'], 'C', note4)

play_with_arpeggio(freqs['D5'], 'G7', note4)
play_with_arpeggio(freqs['D5'], 'G7', note4)
play_with_arpeggio(freqs['C5'], 'C', note2)

print("播放完毕！")
pygame.quit()
