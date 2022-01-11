import pyaudio

p = pyaudio.PyAudio()

apiCnt = p.get_host_api_count()
print("Host API Count: %d" % apiCnt)

default = p.get_default_host_api_info()
print("Host API:%s" % default)

DeviceCnt = p.get_device_count()
for cnt in range(DeviceCnt):
    if(p.get_device_info_by_index(cnt)["hostApi"] == 0):
        print(p.get_device_info_by_index(cnt))  