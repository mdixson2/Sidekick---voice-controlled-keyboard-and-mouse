import deepspeech
import numpy as np
import os
import pyaudio
import time
from deepparser import *
import enchant
import math
import struct
import audioop

d = enchant.Dict("en_US")
# DeepSpeech parameters
DEEPSPEECH_MODEL_DIR = './'
MODEL_FILE_PATH = os.path.join(DEEPSPEECH_MODEL_DIR, 'graph.pbmm')
BEAM_WIDTH = 500
#LM_FILE_PATH = os.path.join(DEEPSPEECH_MODEL_DIR, 'lm.binary')
#TRIE_FILE_PATH = os.path.join(DEEPSPEECH_MODEL_DIR, 'trie')
LM_ALPHA = 0.75
LM_BETA = 1.85

# Make DeepSpeech Model
model = deepspeech.Model(MODEL_FILE_PATH)#, BEAM_WIDTH)
model.setBeamWidth(BEAM_WIDTH)
#model.enableDecoderWithLM(LM_FILE_PATH, TRIE_FILE_PATH, LM_ALPHA, LM_BETA)

# Create a Streaming session
context = model.createStream()
parser = CheetahParser()

# Make sure to set threshold correctly (test dB level for silence and adjust)
threshold = 40 # decibels above which we record
SHORT_NORMALIZE = (1.0/32768.0)
swidth = 2
# Encapsulate DeepSpeech audio feeding into a callback for PyAudio
text_so_far = ''
lastlength = 0
silentcount = 0 # Counts number of reads lower than X decibels (=silence)
countingsilence = False # True if silent periods after threshold crossed not reached
flush = False # Enough silence has occurred after threshold breached to flush (intermediateDecode) and safely use the last word in the stiring
def process_audio(in_data, frame_count, time_info, status):
    global text_so_far
    global lastlength
    global silentcount 
    global countingsilence
    global flush
    dB = 20 * math.log10(audioop.rms(in_data,2))
    data16 = np.frombuffer(in_data, dtype=np.int16)
    if dB > threshold or countingsilence == True:
        silentcount += 1
        if dB > threshold:
            silentcount = 0
            countingsilence = True
        if silentcount >= 20:
            countingsilence = False
            flush = True
        #print(dB)
        data16 = np.frombuffer(in_data, dtype=np.int16)
        context.feedAudioContent(data16)
        text = context.intermediateDecode()

        if flush:
            #print(text)
            flush = False
        #print(text)
        #if text != text_so_far:
            #print('Interim text = {}'.format(text))
            vals = text.split(' ')
            if len(vals) > 1:
                diff = len(vals) - lastlength
                if diff > 0:
                    for word in vals[-diff:]:
                        if word != "" and word != None:
                            if word != "go" and word != "co" and d.check(word):
                                parser.ingest(word)
                        lastlength += 1
                text_so_far = text
          
    return (in_data, pyaudio.paContinue)

# PyAudio parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK_SIZE = 1024

# Feed audio to deepspeech in a callback to PyAudio
audio = pyaudio.PyAudio()
stream = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK_SIZE,
    stream_callback=process_audio
)

print('Please start speaking, when done press Ctrl-C ...')
stream.start_stream()

try: 
    while stream.is_active():
        time.sleep(0.1)
except KeyboardInterrupt:
    # PyAudio
    stream.stop_stream()
    stream.close()
    audio.terminate()
    print('\nThank you for using the speech driven keyboard. Have a nice day.')
    # DeepSpeech
    context.finishStream()