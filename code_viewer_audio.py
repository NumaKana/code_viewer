from types import DynamicClassAttribute
import pyaudio
import pygame
from pygame.locals import *
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
import collections

FORMAT = pyaudio.paInt16
CHANNELS = 2
CHUNK = 1024
RATE = 42000  # サンプリングレート
FRAME_NUM = 218
TIME = 0.2
threshold = 100000000

width = 1200
height = 700
notes_y = 400
chord_y = 200
bg_color = 20, 20, 20
note_name = ("C", "Db", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B")
notes = np.array(["C", "Db", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"])
fifth_circle = ("C", "F", "Bb", "Eb", "Ab", "Db", "F#", "B", "E", "A", "D", "G")
tensions = {0:"", 1:"b2", 2:"2", 3:"#2", 4:"", 5:"4", 6:"b5", 7:"", 8:"b6", 9:"6", 10:"7", 11:"M7",
                12:"", 13:"b9", 14:"9", 15:"#9", 16:"", 17:"11", 18:"#11", 19:"", 20:"b13", 21:"13"}
event_note = []
midi_note = []
text = []
chord_show = ""

#コードをセット
chords = {}
for n in range(0,len(note_name)):
    third = n + 4
    if third > 11: third -= 12
    minor_third = n + 3
    if minor_third > 11: minor_third -= 12
    fifth = n + 7
    if fifth > 11: fifth -= 12
    minor_fifth = n + 6
    if minor_fifth > 11: minor_fifth -= 12
    seventh = n + 10
    aug_fifth = n + 8
    if aug_fifth > 11: aug_fifth -= 12
    if seventh > 11: seventh -= 12
    maj_seventh = n + 11
    if maj_seventh > 11: maj_seventh -= 12
    fourth = n + 5
    if fourth > 11: fourth -= 12
    sixth = n + 9
    if sixth > 11: sixth -= 12
    
    #トライアド
    chords[note_name[n]] = [note_name[n], note_name[third], note_name[fifth]]
    chords[note_name[n]+"m"] = [note_name[n], note_name[minor_third], note_name[fifth]]
    chords[note_name[n]+"sus4"] = [note_name[n], note_name[fourth], note_name[fifth]]
    chords[note_name[n]+"dim"] = [note_name[n], note_name[minor_third], note_name[minor_fifth]]
    chords[note_name[n]+"aug"] = [note_name[n], note_name[third], note_name[aug_fifth]]


#初期化
pygame.init()

#スクリーンの初期設定
screen = pygame.display.set_mode((width, height))
font_chord = pygame.font.Font("C:/Users/kr814/AppData/Local/Microsoft/Windows/Fonts/SourceHanSans-Light.otf", 90)
screen.fill((50,50,50))
chord_text = font_chord.render(chord_show, True, (255,255,255))
chord_rect = chord_text.get_rect(center=(width//2, chord_y))
screen.blit(chord_text, chord_rect)

#グラフの描画準備
plt.ion()
fig = plt.figure(figsize=(6.4, 4.8))
ax = fig.add_subplot()

#オーディオ準備
audio = pyaudio.PyAudio()
#print(audio.get_device_count())
stream = audio.open(
    format = FORMAT, 
    channels = CHANNELS,
    rate = RATE, 
    input = True,
    input_device_index = 3,  # デバイスのインデックス番号
    frames_per_buffer = CHUNK
)

# ここでループを回してマイクから取得される値を処理していく
while True:
    numpydata = np.empty(1)

    for i in range(0, int(RATE / CHUNK * TIME)): 
        data = stream.read(CHUNK)
        tmp = np.frombuffer(data, dtype=np.int)
        numpydata = np.append(numpydata, tmp, axis=0)
    
    #print(numpydata.max())
    if numpydata.max() > threshold:
        numpydata = np.nan_to_num(numpydata)
        hop_length = 512
        n_chroma = 12
        n_octaves = 7
        chroma_cq = librosa.feature.chroma_cqt(y=numpydata, sr=RATE, hop_length=hop_length, fmin=librosa.note_to_hz('C1'), n_chroma=n_chroma, n_octaves=n_octaves)
        time = librosa.core.frames_to_time(np.arange(chroma_cq.shape[1]), sr=RATE, hop_length=hop_length)

        now_chord = []
        chroma_cq_t = chroma_cq.transpose()
        for t, chroma in zip(time, chroma_cq_t):
            current_notes = []
            chord_indices = np.argsort(chroma)[-1:-4:-1]
            current_notes = notes[chord_indices]
            print(f't: {t:.2f}[s], notes: {current_notes}', end='')
            print()

            #コード判定
            for chord, chord_notes in chords.items():

                if set(current_notes) == set(chord_notes):
                    now_chord.append(chord)
                    print(f', chord: {chord}', end='')
                    print()
            if len(now_chord) > 0:
                chord_show = collections.Counter(now_chord).most_common()[0][0]
            else: chord_show = ""

        
        #グラフ再描画処理
        plt.cla()
        plt.clf()
        
        librosa.display.specshow(chroma_cq, x_axis='time', y_axis='chroma')
        plt.colorbar()
        ax.set_title('chromagram (cqt)')
        plt.tight_layout()
        plt.pause(0.1)
    
    else:
        #グラフ再描画処理
        plt.cla()
        plt.clf()
        
        plt.pause(0.1)
        chord_show = ""


    #コード描画処理
    screen.fill((50,50,50))
    chord_text = font_chord.render(chord_show, True, (255,255,255))
    chord_rect = chord_text.get_rect(center=(width//2, chord_y))

    screen.blit(chord_text, chord_rect)

    pygame.draw.rect(screen,  (255,255,255), (1178, notes_y+5, 1, 25))
    pygame.display.update()

    ### イベント処理
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            break
    else:
        continue

    ### whileループ終了
    break