

from __future__ import division

import re
import sys
import os
from google.cloud import speech_v1p1beta1 as speech
import pyaudio
from six.moves import queue

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 5)  # 100ms

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'your/json/path'

class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            input_device_index=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b"".join(data)

def listen_print_loop(responses):
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue
        
        transcript = result.alternatives[0].transcript
        confidence = result.alternatives[0].confidence
        overwrite_chars = " " * (num_chars_printed - len(transcript))
        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + "\r")
            sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:
            speaker_tag = result.alternatives[0].words[-1].speaker_tag if result.alternatives[0].words else None
            channel_tag = result.channel_tag if result.channel_tag else None
            result_words = transcript + overwrite_chars
            print(f"Speaker: {speaker_tag}, Channel: {channel_tag}, Confidence: {confidence}, Words: '{result_words}'")

            # print(response)
            # for alternative in result.alternatives:
                # print(f"Speaker: {alternative.words[-1].speaker_tag}, 信頼度: {confidence}, Words: '{result_words}'")

            # for result in response.results:
            #     for alternative in result.alternatives:
            #         print(f"Speaker Tag: {alternative.words[-1].speaker_tag}, Transcript: '{alternative.transcript}' ")

            if re.search(r"\b(exit|quit)\b", transcript, re.I):
                print("Exiting..")
                break

            num_chars_printed = 0

def main():
    language_code = "ja-JP"

    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
        audio_channel_count=1,
        enable_separate_recognition_per_channel=True,
        enable_automatic_punctuation=True,
        enable_word_confidence=True,
        diarization_config=speech.SpeakerDiarizationConfig(
            enable_speaker_diarization=True,
            min_speaker_count=1,
            max_speaker_count=2,
        ),
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )

        responses = client.streaming_recognize(streaming_config, requests)

        listen_print_loop(responses)

if __name__ == "__main__":
    main()
