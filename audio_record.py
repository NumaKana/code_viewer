import pyaudio  #pyaudioをインポート
import wave     #データ保存用にwaveを使う

device = 3 #マイクの選択
chunk = 1024 
format = pyaudio.paInt16 #フォーマットは16bit
channel = 2 #モノラルで録音
rate = 44100 #サンプリングレート
time = 5 #5秒間録音する
output_path = './fiveseconds.wav' #保存先の名前

p = pyaudio.PyAudio() #録音するんやで

stream = p.open(format = format, 
                channels = channel,
                rate = rate,
                input = True,
                input_device_index = device,
                frames_per_buffer = chunk) #ストリームを開いて録音開始!

print("now recoding...")

frames = [] #録音したデータをしまうList
for i in range(0, int(rate / chunk * time)): 
  data = stream.read(chunk)
  frames.append(data)

print('done.') #録音終わったよ！

stream.stop_stream() #用済みどもの始末
stream.close()
p.terminate()

wf = wave.open(output_path, 'wb') # ファイルに保存するよ
wf.setnchannels(channel)
wf.setsampwidth(p.get_sample_size(format))
wf.setframerate(rate)
wf.writeframes(b''.join(frames))
wf.close() #ファイルを保存したよ