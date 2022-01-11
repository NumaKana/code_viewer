# -*- coding: utf-8 -*-
from types import DynamicClassAttribute
import pygame
import pygame.midi
from pygame.locals import *
import copy

width = 1200
height = 700
notes_y = 400
chord_y = 200
bg_color = 20, 20, 20
#note_name = (["C","C"], ["C#","Db"], ["D","D"], ["D#","Eb"], ["E","E"], ["F","F"], ["F#","Gb"], ["G","G"], ["G#","Ab"], ["A","A"], ["Bb","Bb"], ["B","B"])
note_name = ("C", "Db", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B")
fifth_circle = ("C", "F", "Bb", "Eb", "Ab", "Db", "F#", "B", "E", "A", "D", "G")
tensions = {0:"", 1:"b2", 2:"2", 3:"#2", 4:"", 5:"4", 6:"b5", 7:"", 8:"b6", 9:"6", 10:"7", 11:"M7",
                12:"", 13:"b9", 14:"9", 15:"#9", 16:"", 17:"11", 18:"#11", 19:"", 20:"b13", 21:"13"}


#ダイアトニックコードを作成
diatonics = {}
for n in range(0, len(note_name)):
    two = n+2
    if two > 11: two -= 12
    three = n+4
    if three > 11: three -= 12
    four = n+5
    if four > 11: four -= 12
    five = n+7
    if five > 11: five -= 12
    six = n+9
    if six > 11: six -= 12
    seven = n+11
    if seven > 11: seven -= 12
    diatonics[note_name[n]] = (note_name[n] + "maj7", note_name[two] + "m7", note_name[three] + "m7",
                                note_name[four] + "maj7", note_name[five] + "7", note_name[six] + "m7", note_name[seven] + "m7")

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
    
    #四和音
    chords[note_name[n]+"7"] = [note_name[n], note_name[third], note_name[fifth], note_name[seventh]]
    chords[note_name[n]+"maj7"] = [note_name[n], note_name[third], note_name[fifth], note_name[maj_seventh]]
    chords[note_name[n]+"m7"] = [note_name[n], note_name[minor_third], note_name[fifth], note_name[seventh]]
    chords[note_name[n]+"dim7"] = [note_name[n], note_name[minor_third], note_name[minor_fifth], note_name[sixth]]
    chords[note_name[n]+"aug7"] = [note_name[n], note_name[third], note_name[aug_fifth], note_name[seventh]]
    chords[note_name[n]+"sus7"] = [note_name[n], note_name[fourth], note_name[fifth], note_name[seventh]]


event_note = []
midi_note = []
text = []
chord_show = ""
tension_show = ""

#22音(root~13th)を入れるための配列を作成
note_show = []
for n in range(0,22):
    note_show.append("") 

#初期化
pygame.init()
pygame.midi.init()

#スクリーンの初期設定
screen = pygame.display.set_mode((width, height))

font_note = pygame.font.Font("C:/Users/kr814/AppData/Local/Microsoft/Windows/Fonts/SourceHanSans-Light.otf", 20)
font_chord = pygame.font.Font("C:/Users/kr814/AppData/Local/Microsoft/Windows/Fonts/SourceHanSans-Light.otf", 90)
font_tension = pygame.font.Font("C:/Users/kr814/AppData/Local/Microsoft/Windows/Fonts/SourceHanSans-Light.otf", 40)

screen.fill((50,50,50))

chord_text = font_chord.render(chord_show, True, (255,255,255))
tension_text = font_tension.render(tension_show, True, (255,255,255))

tension_x = (width + int(chord_text.get_width())) // 2

chord_rect = chord_text.get_rect(center=(width//2, chord_y))
tension_rect = tension_text.get_rect(left = tension_x + 10, bottom = chord_y - 20)

screen.blit(chord_text, chord_rect)
screen.blit(tension_text, tension_rect)

for n in range(0,22):
    pygame.draw.rect(screen,  (255,255,255), (12+53*n, notes_y+5, 1, 25))
    text = font_note.render(str(note_show[n]), True, (255,255,255))
    screen.blit(text, (34+53*n, notes_y))
pygame.draw.rect(screen,  (255,255,255), (1178, notes_y+5, 1, 25))

pygame.display.update()


#入力ポートを表示
input_id = pygame.midi.get_default_input_id()
print("input MIDI:%d" % input_id)

#input開始
i = pygame.midi.Input(input_id)
while True:

    #データが入力されたら処理
    if i.poll():
        note_show = []
        for n in range(0,22):
            note_show.append("") 
        tmp = []
        n = 0
        chord_show = ""
        tension_show = ""
        before_chord = ""

        midi_events = i.read(20)
        # print ("full midi_events:" + str(midi_events))

        #note-onで配列に追加、note-offで削除
        if midi_events[0][0][0] == 144:
            if midi_events[0][0][1] not in event_note: event_note.append(midi_events[0][0][1])
        if midi_events[0][0][0] == 128:
            if midi_events[0][0][1] in event_note: event_note.remove(midi_events[0][0][1])

        midi_note = copy.copy(event_note)

        if len(midi_note) > 0:
            #音高順にソート
            midi_note.sort()

            #rootを取り出す
            root_note = midi_note[0]       

            for note in midi_note:
                #rootからの距離へと変更（13thより上はオクターブ下げる）
                note -= root_note
                while note > 21: note -= 12
                
                tmp.append(note)
            
            #13thより上の重複を削除
            tmp = list(set(tmp))

            #表示する場所に挿入
            for num in tmp:
                note_num = num + root_note
                while note_num > 11: note_num -= 12
                note_show[num] = (str(note_name[note_num]))

            #コード群からマッチしている音の数が多いものを判定
            while root_note > 11: root_note -= 12
            tmp_matchnum = 0
            chord_tmp = ""
            chord_note = [a for a in note_show if a != ""]
            chord_note = list(dict.fromkeys(chord_note))
            for chord, chord_notes in chords.items():
                matchnum = len(list(set(chord_notes) & set(chord_note)))
                if matchnum > 1:
                    #コードの種類ごとに重みづけ
                    #rootは入っている前提
                    if chord_notes[0] not in chord_note:
                        matchnum *= 0
                    #最低音がrootと一致していたら可能性高
                    if chord_notes[0] == note_name[root_note]:
                        matchnum *= 5
                    #完全一致は可能性高
                    if set(chord_note) == set(chord_notes):
                        matchnum *= 100
                    #dim, augは完全一致のみ
                    if "dim" in chord or "dim7" in chord or "aug" in chord or "aug7" in chord:
                        if set(chord_note) == set(chord_notes): matchnum *= 100
                        else: matchnum = 0
                    #susは4度の音が入っていることが前提
                    if "sus4" in chord or "sus7" in chord:
                        if chord_notes[1] not in chord_note:
                            matchnum *= 0
                                            
                    #音楽理論的にありそうなパターンは高く
                    #コードは同じでテンションだけ変わっている場合
                    if chord == before_chord:
                        matchnum *= 1.1
                    #同じダイアトニック上のコードは続きやすい
                    for key, diatonic_chord in diatonics.items():
                        if chord in diatonic_chord and before_chord in diatonic_chord:
                            matchnum *= 5
                    #半音、全音で移動するやつ
                    if before_chord != "":
                        chord_distance = int(note_name.index(chord_notes[0])) - int(note_name.index(chords[before_chord][0]))
                        if abs(chord_distance) == 1 or 2:
                            matchnum *= 2
                    #5度圏で隣には行きやすい
                    if before_chord != "":
                        fifth_circle_distance = int(fifth_circle.index(chord_notes[0])) - int(note_name.index(chords[before_chord][0]))
                        if fifth_circle_distance == 1 or 11:
                            matchnum *= 3

                    if matchnum > tmp_matchnum:
                        chord_tmp = chord
                        tmp_matchnum = matchnum
                        print(chord_tmp+":"+str(tmp_matchnum))
            
            chord_show = chord_tmp

            if chord_show != "":        
                #テンションを追加
                tension_note = []
                for n in tmp:
                    n += root_note
                    n_tmp = n
                    while n_tmp > 11: n_tmp -= 12
                    if note_name[n_tmp] not in chords[chord_show]:
                        distance = n - note_name.index(chords[chord_show][0])
                        while distance < 0: distance += 12
                        while distance > 21: distance -= 12
                        if distance == 18 and "m7" in chord_show:
                            distance = 6
                        tension_note.append(distance)
                
                tension_note = list(set(tension_note))
                tension_note.sort()

                for n in tension_note:
                    tension_show += tensions[n] + " "
    
            before_chord = chord_show

            #オンコードの処理
            if chord_show != "":
                if chords[chord_show][0] != chord_note[0]:
                    chord_show += "/" + chord_note[0]

        #描画処理
        screen.fill((50,50,50))
        chord_text = font_chord.render(chord_show, True, (255,255,255))
        tension_text = font_tension.render(tension_show, True, (255,255,255))

        tension_x = (width + int(chord_text.get_width())) // 2

        chord_rect = chord_text.get_rect(center=(width//2, chord_y))
        tension_rect = tension_text.get_rect(left = tension_x + 10, bottom = chord_y - 20)

        screen.blit(chord_text, chord_rect)
        screen.blit(tension_text, tension_rect)

        for n in range(0,22):
            pygame.draw.rect(screen,  (255,255,255), (12+53*n, notes_y+5, 1, 25))
            text = (font_note.render(str(note_show[n]), True, (255,255,255)))
            screen.blit(text, (34+53*n, notes_y))
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

i.close()
pygame.midi.quit()
pygame.quit()

