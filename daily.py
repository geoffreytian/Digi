import praw
import pyowm
import datetime
import speech_recognition as sr
from gtts import gTTS
import os
import random


# obtain audio from the microphone
def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        play_audio("How can I help you?", "en")
        audio = r.listen(source)

        try:
            return r.recognize_google(audio)

        except:
            pass


def get_joke(num_jokes):
    """
    Gets jokes from reddit.
    :param num_jokes: This is how many times the user has asked for a joke.
    :return: A string, ready to be read out, that tells a joke.
    """
    reddit = praw.Reddit(client_id = 'QL3zf4QfPOaOQw', client_secret = 'aZJEE0uGrzzssCE_2Q5DS3MXy5w', user_agent = 'Digi by Matthew and Geoff')
    # BTW, you need a praw.ini file for this. Otherwise this won't work. I'll send you the praw.ini file some time.
    # put it here:
    #In the directory specified by $HOME/.config if the HOME environment variable is defined (Linux and Mac OS systems).
    # For more information: https://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html#praw-ini
    list_of_jokes = []
    for submission in reddit.subreddit('jokes').top(time_filter='month', limit=(num_jokes+1)):
        joke_i = (submission.title, submission.selftext)
        list_of_jokes.append(joke_i)

    list_of_jokes[num_jokes][1].replace('\n', '')
    result = f'Here is a joke. Here is how it goes. {list_of_jokes[num_jokes][0]} {list_of_jokes[num_jokes][1]}'
    return result


def get_weather():
    """
    Gets the current weather of ATX.
    :return: A string, ready to be read out, that gives information about the weather.
    """
    owm = pyowm.OWM('a07c45f49457239d1504a9fe6fa19b3d')
    observation = owm.weather_at_id(4671654) #THIS IS AUSTIN, TX'S ID
    w = observation.get_weather()
    w.get_humidity()
    w.get_temperature('fahrenheit')
    temp = ''
    temp_max = ''
    temp_min = ''
    for k, v in w.get_temperature('fahrenheit').items():
        if k == 'temp':
            temp = v
        elif k == 'temp_max':
            temp_max = v
        elif k == 'temp_min':
            temp_min = v
    result = f'The temperature right now is: {int(temp)} degrees Fahrenheit. It is projected to be between {int(temp_min)} degrees and {int(temp_max)} degrees. '
    return result


def get_time():
    """
    Gets the current time using time module.
    :return: A string, ready to be read out, that gives information about the time.
    """
    currentDT = datetime.datetime.now()
    date = currentDT.strftime("%a, %b %d, %Y")
    time = currentDT.strftime("%I %M %p")
    result = f'It is {time} on {date}.'
    return result


def play_audio(string, language):
    """
    saves the string as an mp3 audio file using google text to speech and then uses command line to play the file.
    :param string: string to be read
    :param language: language to be output
    :return: speech
    """
    str = string
    myobj = gTTS(text=str, lang=language, slow=False)
    myobj.save("welcome.mp3")
    try:
        os.system("mpg321 welcome.mp3")
    except:
        os.system("welcome.mp3")


def main():
    language = 'en'
    num_jokes = random.randint(0,100)
    while True:
        command = get_audio()
        if "joke" in command:
            str =  get_joke(num_jokes)
            play_audio(str, language)
            if num_jokes < 100:
                num_jokes = num_jokes + 1
            else:
                num_jokes = 0

        if "weather" in command:
            play_audio(get_weather(), language)

        if "time" in command:
            play_audio(get_time(), language)

        if command == "goodbye":
            play_audio('goodbye', language)
            break


if __name__ == "__main__":
    main()
