import pygame
import numpy as np
import time

# ================= 1. 频率表生成 =================
A4 = 440
C0 = A4 * pow(2, -4.75)
note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
freqs = {}
for i in range(9):
    for j, name in enumerate(note_names):
        freqs[name + str(i)] = C0 * pow(2, i + (j / 12))

# 增加一个休止符（静音）
freqs['REST'] = 0.0  

# ================= 2. Pygame 初始化 =================
fs = 44100
pygame.mixer.init(frequency=fs, channels=1) # 明确使用单声道

# ================= 3. 音符渲染函数 =================
def generate_tone(freq, duration_sec):
    """生成单个音符的波形（包含高次谐波和淡入淡出）"""
    t = np.arange(int(fs * duration_sec)) / fs
    wave = np.zeros_like(t, dtype=np.float32)
    
    if freq == 0.0: # 休止符
        return wave
        
    # 叠加谐波 (基频 + 2、3、4、5倍频)
    for i in range(1, 6):
        amplitude = 1.0 / i
        wave += amplitude * np.sin(2 * np.pi * t * (freq * i))
        
    # --- 包络线 (Envelope) 消除爆音 ---
    # 在音符开头和结尾加入 0.05 秒的淡入淡出
    fade_len = int(fs * 0.05)
    if len(wave) > fade_len * 2:
        fade_in = np.linspace(0, 1, fade_len)
        fade_out = np.linspace(1, 0, fade_len)
        wave[:fade_len] *= fade_in
        wave[-fade_len:] *= fade_out
        
    return wave

# ================= 4. 乐谱转波形引擎 =================
def render_song(tracks, bpm=120):
    """
    将多条音轨合成到一个音频数组中
    tracks: 字典，包含多个音轨的列表
    bpm: 音乐速度 (Beats Per Minute)
    """
    beat_duration = 60.0 / bpm  # 一拍的绝对时间（秒）
    
    # 1. 找出整首歌的总长度（找到所有音轨中最后结束的音符）
    max_beats = 0
    for track_name, notes in tracks.items():
        for note_name, start_beat, duration_beats in notes:
            end_beat = start_beat + duration_beats
            if end_beat > max_beats:
                max_beats = end_beat
                
    total_samples = int(max_beats * beat_duration * fs)
    
    # 2. 创建"空白画布"（总混音缓冲区）
    mix_buffer = np.zeros(total_samples, dtype=np.float32)
    
    # 3. 把所有音符"画"（相加）到画布上
    for track_name, notes in tracks.items():
        for note_name, start_beat, duration_beats in notes:
            # 计算时间和采样点位置
            start_sec = start_beat * beat_duration
            duration_sec = duration_beats * beat_duration
            
            start_idx = int(start_sec * fs)
            
            # 生成这个音符的波形
            freq = freqs[note_name]
            wave = generate_tone(freq, duration_sec)
            
            end_idx = start_idx + len(wave)
            
            # 核心原理：波形叠加（加法）
            mix_buffer[start_idx:end_idx] += wave
            
    # 4. 防止爆音，进行总体归一化并转为 16-bit
    max_amp = np.max(np.abs(mix_buffer))
    if max_amp > 0:
        mix_buffer *= (0.8 / max_amp) # 预留一点余量，最大音量 80%
        
    # Pygame 单声道格式要求 shape 为 (N, 1)
    #mix_buffer = np.reshape(mix_buffer, (-1, 1))
    final_audio = (mix_buffer * 32767).astype(np.int16)
    
    return final_audio

# ================= 5. 编写乐谱 (多音轨) =================
# 格式: (音符名, 起始拍子, 持续拍子)
# 注意：我们假设一拍就是四分音符 (note4)

score = {
    # 右手主旋律
    "Melody": [
        ('E5', 0, 1), ('E5', 1, 1), ('F5', 2, 1), ('G5', 3, 1),
        ('G5', 4, 1), ('F5', 5, 1), ('E5', 6, 1), ('D5', 7, 1),
        ('C5', 8, 1), ('C5', 9, 1), ('D5', 10, 1), ('E5', 11, 1),
        ('E5', 12, 1.5), ('D5', 13.5, 0.5), ('D5', 14, 2)
    ],
    
    # 左手伴奏 (和弦分解或长和弦，这里用柱式长和弦示范)
    "Chords_Note1": [
        ('C3', 0, 4),  # 第 0 拍开始，弹 C大调根音，持续 4 拍
        ('G2', 4, 4),  # 第 4 拍开始，弹 G大调根音，持续 4 拍
        ('C3', 8, 4),  # 第 8 拍开始，弹 C大调根音，持续 4 拍
        ('G2', 12, 2), # 第 12 拍开始，弹 G大调根音，持续 2 拍
        ('G2', 14, 2)
    ],
    "Chords_Note2": [
        ('E3', 0, 4),  # C大调三音
        ('B2', 4, 4),  # G大调三音
        ('E3', 8, 4),  
        ('B2', 12, 2),
        ('B2', 14, 2)
    ],
    "Chords_Note3": [
        ('G3', 0, 4),  # C大调五音
        ('D3', 4, 4),  # G大调五音
        ('G3', 8, 4),  
        ('D3', 12, 2),
        ('D3', 14, 2)
    ]
}

# ================= 6. 渲染并播放 =================
print("正在合成音乐...")
# BPM=120 表示一分钟 120 拍，即一拍 0.5 秒（也就是你原来的 note4 速度）
final_wave = render_song(score, bpm=120) 

print("开始播放...")
print(final_wave)
sound = pygame.sndarray.make_sound(final_wave)

sound.play()

# 计算播放总时长并等待
total_play_time = len(final_wave) / fs
time.sleep(total_play_time + 1) # 等待音乐播放完毕
print("播放完毕。")
