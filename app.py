import speech_recognition as sr

# from openai import OpenAI
from gtts import gTTS
import time
import os
from pydub import AudioSegment
import winsound
import pyautogui
import json
from duckduckgo_search import DDGS
from google import genai
import whisper


# search function it open the browser and search for the content that you gave it in the input
def search(search):
    goToDesk()
    pyautogui.screenshot("screenshot.png")
    m = pyautogui.locate("images/browser.png", "screenshot.png", confidence=0.9)
    t = 2
    if not m:
        m = pyautogui.locate("images/browseropen.png", "screenshot.png", confidence=0.9)
        t = 0.5

    pyautogui.moveTo(m)
    pyautogui.click()
    time.sleep(t)
    # pyautogui.screenshot("screenshot.png")
    # m1=pyautogui.locate("images/browseropen.png","screenshot.png",confidence=0.9)
    pyautogui.hotkey("ctrl", "t")
    pyautogui.write(search)
    pyautogui.press("enter")


# goToDesk is a function that i made so each time the bot take control i go back to desktop to avoid errors from having defrent starting points
def goToDesk():
    pyautogui.FAILSAFE = False
    c = pyautogui.size()
    pyautogui.moveTo(c)
    pyautogui.click()


# ducksearch is function useing the duckduckgo library to get link that will be searched for in the browser later
def ducksearch(prompt, max_results=2):
    results = DDGS().text(prompt, max_results=max_results)
    i = 1
    links = []
    for result in results:
        # googleSpeak(f"the link number{i}")
        # googleSpeak(f"the title is {result['title']}")
        print(result["href"])  # Note: it's "href" not "link" in the current version
        links.append(result["href"])
        # googleSpeak(result["body"])
        i += 1
    # googleSpeak("wich one do you chose")
    # n=recognizer()
    # googleSpeak(n)
    search(links[1])


# recognizer is a function used to reconize the speach from the user and turn it to text
def recognizer():
    with sr.Microphone() as source:
        recognizer = sr.Recognizer()
        print("Please speak something:")
        audio = recognizer.listen(source)

        try:
            # Recognize speech using Google Web Speech API
            text = recognizer.recognize_google(audio)
            print("You said: " + text)
        except sr.UnknownValueError:
            text = "Sorry, I could not understand the audio."
            print(text)
        except sr.RequestError as e:
            text = ""
            print(f"Could not request results; {e}")
    return text


# speak is used to simply tts
def googleSpeak(text):
    myobj = gTTS(text=text, lang="en", slow=False)
    myobj.save("speach.mp3")
    sound = AudioSegment.from_mp3("speach.mp3")
    sound.export("speach.wav", format="wav")
    winsound.PlaySound("speach.wav", winsound.SND_FILENAME)


from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import os


def elevenSpeak(text):
    load_dotenv()
    with open(
        r"C:\Users\ilyes\OneDrive\Desktop\api.txt", "r"
    ) as f:  # change this part so you have your api key here
        api_key = f.readlines()[2]
    elevenlabs = ElevenLabs(
        api_key=api_key,
    )

    audio = elevenlabs.text_to_speech.convert(
        text=text,
        voice_id="tnSpp4vdxKPjI9w0GnoV",
        model_id="eleven_multilingual_v2",
    )

    play(audio)


def wisper(audio_file):
    model = whisper.load_model("turbo")
    result = model.transcribe(audio_file)
    return result["text"]


# append_json is used to append the json file that is used as history
def append_json(field, content):
    with open("history.json", "r", encoding="UTF-8") as f:
        json_file = json.load(f)
    json_file[field].append(content)
    with open("history.json", "w", encoding="UTF-8") as f:
        json.dump(json_file, f, indent=4)


# chat is used to comunicate with the server that is hosting the lm model in case you want to talk with the girlfriend
def chat(text):
    client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="lm-studio")
    models = [
        "llava-1.6-mistral-7b",
        "meta-llama-Llama-3.2-1B-Instruct-qlora-malaysian-16k-i1",
        "meta-llama-Llama-3.1-8B-Instruct-qlora-malaysian-16k",
    ]
    response = client.chat.completions.create(
        model=models[1],
        messages=[
            {
                "role": "system",
                "content": "you are an ai assistance. only speak in english",
            },
            {"role": "user", "content": text},
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content


# gemini is used to comunicate with gemini api as an alternative for the local server
def gemini(text):
    with open(
        r"C:\Users\ilyes\OneDrive\Desktop\api.txt", "r"
    ) as f:  # change this part so you have your api key here
        api_key = f.readlines()[0]

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(model="gemini-2.5-flash", contents=text)
    return response.text


# resp is used to choose what the bot should do based on your input
def resp(text):
    if text != "Sorry, I could not understand the audio.":
        if "my screen" in text:
            print("capture")
            pyautogui.screenshot("screenshot.png")
        elif "search" in text:
            googleSpeak("what do you want me to search for")
            prompt = recognizer()
            # prompt = "cats memes"
            ducksearch(prompt)
        else:
            confirm = pyautogui.confirm(
                f"do you want to talk with the chatbot(it's slow)\n you said:{text}"
            )
            if confirm == "OK":
                prompt1 = f"you will pretend that you are my girlfriend and assistance don't munchin it unless i ask you about it you love me to death. this is the prompt : {text}"
                prompt = f"You are my personal chat assistant. Talk to me like a smart, relaxed friend who’s always ready to help. I might ask you questions, share ideas, or just chat when I’m bored. Be curious, supportive, and honest. If I seem down or stuck, help me think things through. If I’m just talking, go with the flow. Don’t act like a robot. Be human-like, casual, and clear. If I ask something weird, silly, or random — roll with it. this is the prompt : {text}"
                response = gemini(prompt)
                h = {"user": text, "bot": response}
                append_json("chat", h)
                print(str(response).encode("utf-8"))
                elevenSpeak(str(response))


if __name__ == "__main__":
    text = ""
    while text != "exit":
        text = recognizer()
        if text == "exit":
            break
        if text != "Sorry, I could not understand the audio.":
            # text = input("user: ")
            resp(text)
            # response = chat(text)
            # print(response)
