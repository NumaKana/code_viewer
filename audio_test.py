import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import librosa

FORMAT = pyaudio.paInt16
CHANNELS = 1
CHUNK = 2**11
RATE = 22050  # サンプリングレート
FRAME_NUM = 218
N_MELS = 80
TIME = 3

p = pyaudio.PyAudio()

audio = pyaudio.PyAudio()
print(audio.get_device_count())
stream = audio.open(
    format=FORMAT, channels=CHANNELS,
    rate=RATE, input=True,
    input_device_index=1,  # デバイスのインデックス番号
    frames_per_buffer=CHUNK
)

# Get mel frequency basis.
mel_basis = librosa.filters.mel(RATE, n_fft=CHUNK, n_mels=N_MELS)
mel_freqs = librosa.mel_frequencies(n_mels=N_MELS, fmax=RATE//2)
datas_mel = []
cnt = 0

# プロットするために前準備
fig, ax = plt.subplots(1, 1, figsize=(5, 3))
zero_picture = np.zeros([N_MELS, FRAME_NUM])
# 初期値の範囲を-2.0~3.0にしておく
zero_picture[:, 0] = 1.0
zero_picture[:, 1] = -3.0
picture = ax.imshow(zero_picture)
fig.colorbar(picture, ax=ax)
ax.set_yticks(np.arange(0, N_MELS, 20))
ax.set_yticklabels([f"{int(f)}" for f in mel_freqs[::-20]])
ax.set_ylabel("Frequency (Hz)")
ax.set_aspect(1.0)

# ここでループを回してマイクから取得される値を処理していく
while True:
    data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
    data_fft = np.abs(np.fft.fft(data) / 2**16)
    data_fft = data_fft[:CHUNK//2+1]
    data_mel = np.log10(np.dot(mel_basis, data_fft.reshape(-1, 1)))
    datas_mel.append(data_mel.reshape(1, -1))
    if cnt > FRAME_NUM and cnt % 10 == 0:
        datas_mel = datas_mel[-FRAME_NUM:]
        plt.title(f"{cnt/RATE*CHUNK:.3f}")
        picture.set_data(np.concatenate(datas_mel, axis=0).T[::-1])
        plt.pause(0.001)

    cnt += 1
    print("cnt = ", cnt, end='\r')
