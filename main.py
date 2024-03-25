from serpwow.google_search_results import GoogleSearchResults
import speech_recognition as sr
import openai

openai_api_key =  
serpwow_api_key = 

openai.api_key = openai_api_key
serpwow = GoogleSearchResults(serpwow_api_key)

def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for a command. Please speak...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError:
            print("Could not request results; check your network connection.")
            return None

def handle_command(command):
    # Try to get a response from OpenAI
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{command}\nHow can I help you?",
        max_tokens=50
    )
    answer = response.choices[0].text.strip()

    # If the response is uncertain or vague, search on Google
    if "I'm not sure" in answer or "I don't understand" in answer:
        print("I didn't understand your query, so I'm searching Google for the answer...")
        search_results = serpwow.get_json({"q": command})
        google_answer = search_results['organic_results'][0]['snippet'] if search_results['organic_results'] else "No results found."
        print(f"Google says: {google_answer}")
    else:
        print(answer)

while True:
    command = listen_for_command()
    if command:
        handle_command(command)
