
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
freqs['REST'] = 0.0  

# ================= 2. Pygame 初始化 =================
fs = 44100
pygame.mixer.init(frequency=fs, channels=1) # 单声道

# ================= 3. 音符渲染函数 =================
def generate_tone(freq, duration_sec):
    t = np.arange(int(fs * duration_sec)) / fs
    wave = np.zeros_like(t, dtype=np.float32)
    
    if freq == 0.0: 
        return wave
        
    for i in range(1, 6):
        amplitude = 1.0 / i
        wave += amplitude * np.sin(2 * np.pi * t * (freq * i))
        
    fade_len = int(fs * 0.05)
    if len(wave) > fade_len * 2:
        fade_in = np.linspace(0, 1, fade_len)
        fade_out = np.linspace(1, 0, fade_len)
        wave[:fade_len] *= fade_in
        wave[-fade_len:] *= fade_out
        
    return wave

# ================= 4. 乐谱转波形引擎 =================
def render_song(tracks, bpm=120):
    beat_duration = 60.0 / bpm  
    max_beats = 0
    for track_name, notes in tracks.items():
        for note_name, start_beat, duration_beats in notes:
            end_beat = start_beat + duration_beats
            if end_beat > max_beats:
                max_beats = end_beat
                
    total_samples = int(max_beats * beat_duration * fs)
    mix_buffer = np.zeros(total_samples, dtype=np.float32)
    
    for track_name, notes in tracks.items():
        for note_name, start_beat, duration_beats in notes:
            start_sec = start_beat * beat_duration
            duration_sec = duration_beats * beat_duration
            start_idx = int(start_sec * fs)
            freq = freqs[note_name]
            wave = generate_tone(freq, duration_sec)
            end_idx = start_idx + len(wave)
            mix_buffer[start_idx:end_idx] += wave
            
    max_amp = np.max(np.abs(mix_buffer))
    if max_amp > 0:
        mix_buffer *= (0.8 / max_amp) 
        
    # 【已修复报错】直接将1维数组转为 int16，去掉了 reshape
    final_audio = (mix_buffer * 32767).astype(np.int16)
    return final_audio

# ================= 5. 编写乐谱 (4个乐句) =================
# 格式: (音符名, 起始拍子, 持续拍子)

# 第一乐句：主旋律 A (结尾落在D)
score1 = {
    "Melody": [
        ('E5', 0, 1), ('E5', 1, 1), ('F5', 2, 1), ('G5', 3, 1),
        ('G5', 4, 1), ('F5', 5, 1), ('E5', 6, 1), ('D5', 7, 1),
        ('C5', 8, 1), ('C5', 9, 1), ('D5', 10, 1), ('E5', 11, 1),
        ('E5', 12, 1.5), ('D5', 13.5, 0.5), ('D5', 14, 2)
    ],
    "Chord_Root":  [('C3',0,4), ('G2',4,4), ('C3',8,4), ('C3',12,2), ('G2',14,2)],
    "Chord_Third": [('E3',0,4), ('B2',4,4), ('E3',8,4), ('E3',12,2), ('B2',14,2)],
    "Chord_Fifth": [('G3',0,4), ('D3',4,4), ('G3',8,4), ('G3',12,2), ('D3',14,2)]
}

# 第二乐句：主旋律 A' (变奏，结尾完美解决落在C)
score2 = {
    "Melody": [
        ('E5', 0, 1), ('E5', 1, 1), ('F5', 2, 1), ('G5', 3, 1),
        ('G5', 4, 1), ('F5', 5, 1), ('E5', 6, 1), ('D5', 7, 1),
        ('C5', 8, 1), ('C5', 9, 1), ('D5', 10, 1), ('E5', 11, 1),
        ('D5', 12, 1.5), ('C5', 13.5, 0.5), ('C5', 14, 2)
    ],
    "Chord_Root":  [('C3',0,4), ('G2',4,4), ('C3',8,4), ('G2',12,2), ('C3',14,2)],
    "Chord_Third": [('E3',0,4), ('B2',4,4), ('E3',8,4), ('B2',12,2), ('E3',14,2)],
    "Chord_Fifth": [('G3',0,4), ('D3',4,4), ('G3',8,4), ('D3',12,2), ('G3',14,2)]
}

# 第三乐句：主旋律 B (转折，轻快的跳跃)
# 加入了F大调和A小调和弦增加色彩
score3 = {
    "Melody": [
        ('D5', 0, 1), ('D5', 1, 1), ('E5', 2, 1), ('C5', 3, 1),
        ('D5', 4, 1), ('E5', 5, 0.5), ('F5', 5.5, 0.5), ('E5', 6, 1), ('C5', 7, 1),
        ('D5', 8, 1), ('E5', 9, 0.5), ('F5', 9.5, 0.5), ('E5', 10, 1), ('D5', 11, 1),
        ('C5', 12, 1), ('D5', 13, 1), ('G4', 14, 2)
    ],
    "Chord_Root":  [('G2',0,4), ('G2',4,2), ('C3',6,2), ('G2',8,2), ('A2',10,2), ('F2',12,2), ('G2',14,2)],
    "Chord_Third": [('B2',0,4), ('B2',4,2), ('E3',6,2), ('B2',8,2), ('C3',10,2), ('A2',12,2), ('B2',14,2)],
    "Chord_Fifth": [('D3',0,4), ('D3',4,2), ('G3',6,2), ('D3',8,2), ('E3',10,2), ('C3',12,2), ('D3',14,2)]
}

# 第四乐句：主旋律 A' (回归，与第二乐句相同，全曲结束)
score4 = {
    "Melody": [
        ('E5', 0, 1), ('E5', 1, 1), ('F5', 2, 1), ('G5', 3, 1),
        ('G5', 4, 1), ('F5', 5, 1), ('E5', 6, 1), ('D5', 7, 1),
        ('C5', 8, 1), ('C5', 9, 1), ('D5', 10, 1), ('E5', 11, 1),
        ('D5', 12, 1.5), ('C5', 13.5, 0.5), ('C5', 14, 2)
    ],
    "Chord_Root":  [('C3',0,4), ('G2',4,4), ('C3',8,4), ('G2',12,2), ('C3',14,2)],
    "Chord_Third": [('E3',0,4), ('B2',4,4), ('E3',8,4), ('B2',12,2), ('E3',14,2)],
    "Chord_Fifth": [('G3',0,4), ('D3',4,4), ('G3',8,4), ('D3',12,2), ('G3',14,2)]
}

# ================= 6. 依次渲染并播放 =================
# 将四个乐句放进列表循环播放
scores_list = [score1, score2, score3, score4]

print("🎼 音乐合成与播放开始...\n")

for idx, current_score in enumerate(scores_list):
    print(f"[{idx+1}/4] 正在合成第 {idx+1} 乐句...")
    
    # 渲染当前乐句的波形
    final_wave = render_song(current_score, bpm=120) 
    sound = pygame.sndarray.make_sound(final_wave)
    
    print(f"▶ 正在播放第 {idx+1} 乐句...\n")
    sound.play()
    
    # 计算当前乐句播放时长，并让程序等待，直到播放完毕
    total_play_time = len(final_wave) / fs
    time.sleep(total_play_time) 

print("🎉 欢乐颂全曲播放完毕！")

