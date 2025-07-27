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


def search(search):
    goToDesk()
    pyautogui.screenshot("screenshot.png")
    m = pyautogui.locate("images/browser.png", "screenshot.png", confidence=0.9)
    t = 3
    if not m:
        m = pyautogui.locate("images/browseropen.png", "screenshot.png", confidence=0.9)
        t = 0.5

    pyautogui.moveTo(m, duration=1)
    pyautogui.click()
    time.sleep(t)
    # pyautogui.screenshot("screenshot.png")
    # m1=pyautogui.locate("images/browseropen.png","screenshot.png",confidence=0.9)
    pyautogui.hotkey("ctrl", "t")
    pyautogui.write(search, 0.2)
    pyautogui.press("enter")


def goToDesk():
    pyautogui.FAILSAFE = False
    c = pyautogui.size()
    pyautogui.moveTo(c)
    pyautogui.click()


def ducksearch(prompt, max_results=2):
    results = DDGS().text(prompt, max_results=max_results)
    i = 1
    links = []
    for result in results:
        # speak(f"the link number{i}")
        # speak(f"the title is {result['title']}")
        print(result["href"])  # Note: it's "href" not "link" in the current version
        links.append(result["href"])
        # speak(result["body"])
        i += 1
    # speak("wich one do you chose")
    # n=recognizer()
    # speak(n)
    search(links[1])


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


def speak(text):
    myobj = gTTS(text=text, lang="en", slow=False)
    myobj.save("speach.mp3")
    sound = AudioSegment.from_mp3("speach.mp3")
    sound.export("speach.wav", format="wav")
    winsound.PlaySound("speach.wav", winsound.SND_FILENAME)


def append_json(field, content):
    with open("history.json", "r") as f:
        json_file = json.load(f)
    json_file[field].append(content)
    with open("history.json", "w") as f:
        json.dump(json_file, f)


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


def gemini(text):
    with open("api.txt", "r") as f:
        api_key = f.readline()

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(model="gemini-2.5-flash", contents=text)
    return response.text


def resp(text):
    if text != "Sorry, I could not understand the audio.":
        if "my screen" in text:
            print("capture")
            pyautogui.screenshot("screenshot.png")
        elif "search" in text:
            speak("what do you want me to search for")
            prompt = recognizer()
            # prompt = "cats memes"
            ducksearch(prompt)
        else:
            confirm = pyautogui.confirm(
                f"do you want to talk with the chatbot(it's slow)\n you said:{text}"
            )
            if confirm == "OK":
                response = gemini(text)
                h = {"user": text, "bot": response}
                # append_json("chat", h)
                print(str(response))
                speak(str(response))


if __name__ == "__main__":
    text = ""
    while text != "close":
        text = recognizer()
        if text != "Sorry, I could not understand the audio.":
            # text = input("user: ")
            resp(text)
            # response = chat(text)
            # print(response)
