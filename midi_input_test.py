# -*- coding: utf-8 -*-
import pygame.midi

pygame.init()
pygame.midi.init()

#入力ポートを出力
input_id = pygame.midi.get_default_input_id()
print("input MIDI:%d" % input_id)

#input開始
i = pygame.midi.Input(input_id)

#MIDIイベントを14回読み込んで出力する（note-onで1回、note-offで1回の7音）
#status:144=note-on, 128=note-off　data1:音高 data2:volume data3:channel
print ("starting")
print ("full midi_events:[[[status,data1,data2,data3],timestamp],...]")

going = True
count = 0
while going:
    #データが入力されたらprint
    if i.poll():
        midi_events = i.read(10)
        print ("full midi_events:" + str(midi_events))
        count += 1
    if count >= 14:
        going = False

i.close()
pygame.midi.quit()
pygame.quit()
exit()