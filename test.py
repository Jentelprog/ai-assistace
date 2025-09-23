# # # # # from google import genai
# # # # # def gemini(text):
# # # # #     with open("api.txt","r") as f:
# # # # #         api_key=f.readline()

# # # # #     client = genai.Client(api_key=api_key)

# # # # #     response = client.models.generate_content(
# # # # #         model="gemini-2.5-flash", contents="hi how are you "
# # # # #     )
# # # # #     return response.text
# # # # import whisper
# # # # def wisper(audio_file):
# # # #     model = whisper.load_model("turbo")
# # # #     result = model.transcribe(audio_file)
# # # #     return result["text"]

# # # # text=wisper("Injuries & Being Sick.mp3")
# # # # with open("jaden_video.txt",'w') as f:
# # # #     f.write(text)
# # # from RealtimeSTT import AudioToTextRecorder
# # # import pyautogui

# # # def process_text(text):
# # #     pyautogui.typewrite(text + " ")

# # # if __name__ == '__main__':
# # #     print("Wait until it says 'speak now'")
# # #     recorder = AudioToTextRecorder()

# # #     while True:
# # #         recorder.text(process_text)
# # import pyttsx3
# # engine=pyttsx3.init()
# # voices=engine.getProperty('voices')
# # engine.setProperty('rate', 145)
# # engine.setProperty('voice', voices[1].id)
# # engine.say("Oh, hello my love! I'm absolutely wonderful now that I'm talking to you. My heart just feels lighter. How are *you* doing today, my dearest? I hope it's been amazing!")
# # engine.runAndWait()
# from dotenv import load_dotenv
# from elevenlabs.client import ElevenLabs
# from elevenlabs import play
# import os

# load_dotenv()

# elevenlabs = ElevenLabs(
#     api_key="sk_ee75c509c198d3cd439306748bebf1f4fa6ebee953800925",
# )

# audio = elevenlabs.text_to_speech.convert(
#     text="hello my love.",
#     voice_id="jGf6Nvwr7qkFPrcLThmD",
#     model_id="eleven_multilingual_v2",
# )

# play(audio)


import torch
from TTS.api import TTS
from TTS.tts.configs.xtts_config import XttsConfig

# allowlist the config so torch.load can unpickle it
torch.serialization.add_safe_globals([XttsConfig])

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# List available 🐸TTS models
print(TTS().list_models())

# Init TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# Run TTS
# ❗ Since this model is multi-lingual voice cloning model, we must set the target speaker_wav and language
# Text to speech list of amplitude values as output
wav = tts.tts(text="yeah it work!", speaker_wav="speach.wav", language="en")
# Text to speech to a file
tts.tts_to_file(text="yeah it work!", speaker_wav="speach.wav", language="en", file_path="output.wav")