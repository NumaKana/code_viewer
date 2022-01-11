import pygame
import pygame.midi

#初期化
pygame.init()
pygame.midi.init()

count = pygame.midi.get_count()

#MIDI入力・出力ポートのデフォルト値を出力
print("get_default_input_id:%d" % pygame.midi.get_default_input_id())
print("get_default_output_id:%d" % pygame.midi.get_default_output_id())

#各ポートに割り当てられているデバイス、input,outputを表示
print("No:(interf, name, input, output, opened)")
for i in range(count):
    print("%d:%s" % (i, pygame.midi.get_device_info(i)))
