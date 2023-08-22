import pyttsx3
import re
import openai
import webbrowser





OPENAI_KEY = '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'
openai.api_key = OPENAI_KEY

# Daftar situs web
websites = {
    'youtube': 'https://www.youtube.com/',
    'exzwebs': 'https://exz.free.nf/',
    'google': 'https://www.google.com/',
    'github': 'https://github.com/',
    'twitter': 'https://www.twitter.com/',
    'instagram': 'https://www.instagram.com/',
    'facebook': 'https://www.facebook.com/',
    'chatgpt': 'https://chat.openai.com/',
    'wikipedia': 'https://en.wikipedia.org/'
    # Tambahkan situs web lain sesuai keinginan Anda
}



# Inisialisasi Text-to-Speech Engine
tts_engine = pyttsx3.init()
voices = tts_engine.getProperty('voices')
tts_engine.setProperty('volume', 1)   # Mengatur volume
tts_engine.setProperty('rate', 180)   # Mengatur kecepatan
tts_engine.setProperty('pitch', 1.2)
tts_engine.setProperty('voice', voices[1].id)

promt = "Jawab pake bahasa english untuk menjawab pertanyaan tersebut. kamu adalah Bot yang diberi nama Vyrine. Tugas kamu membantu Master mencari informasi!"

def get_bot_response(inputuser):
    response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=inputuser + promt,
            max_tokens=2025,
            temperature=1,
            frequency_penalty=0.45,
            presence_penalty=0.54,
            top_p=0.43
        )
    print(f"Viryne:", response.choices[0].text.strip())
    tts_engine.say(response.choices[0].text.strip())
    tts_engine.runAndWait()
    chatbot()
    
    
        

# Fungsi untuk membuka situs web
def open_website(website):
    if website in websites:
        print(f"Viryne: Wait! I will open the website page {website}.")
        tts_engine.say(f"Wait! I will open the website page {website}.")
        tts_engine.runAndWait()
        webbrowser.open(websites[website])
    else:
        print(f"Viryne: Sorry, I don't understand the command.")
        tts_engine.say("Sorry, I don't understand the command.")
        tts_engine.runAndWait()

# Fungsi utama chatbot
def chatbot():
   
    while True:
        input_text = input("Master: ")
        input_text = input_text.lower()
        if re.search(r'\b(open)\b', input_text):
            for website in websites:
                if re.search(r'\b' + website + r'\b', input_text):
                    open_website(website)
                    break
            else:
                print("Viryne: Sorry, I don't know the name of the website.")
                tts_engine.say("Sorry, I don't know the name of the website.")
                tts_engine.runAndWait()
        if re.search(r'\b', input_text):
            get_bot_response(inputuser=input_text)
            break
        else:
            print("Viryne: Sorry, I don't understand what you mean")
            tts_engine.say("Sorry, I don't understand what you mean")
            tts_engine.runAndWait()

            


# Jalankan chatbot
if __name__ == "__main__":
    get_bot_response(inputuser="Beri Sambutan kepada master!")
