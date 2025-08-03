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
