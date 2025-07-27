from google import genai
def gemini(text):
    with open("api.txt","r") as f:
        api_key=f.readline()

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash", contents="hi how are you "
    )
    return response.text
