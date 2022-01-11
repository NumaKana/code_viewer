### インポート
import pygame
from pygame.locals import KEYDOWN,K_ESCAPE
 
### モジュール初期化
pygame.init()
 
### 画面設定
pygame.display.set_mode((640,400))
 
### 無限ループ
while True:

 
    ### イベント処理
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            break
    else:
        continue
 
    ### whileループ終了
    break
 
### 終了処理
pygame.quit()