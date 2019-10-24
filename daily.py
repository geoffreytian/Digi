import praw
import pyowm
import datetime
import speech_recognition as sr
from gtts import gTTS
import os
import random
import sys
import config
from geolocation.main import GoogleMaps
from geolocation.distance_matrix.client import DistanceMatrixApiClient
import geocoder

n = 49

# obtain audio from the microphone
def get_audio():
    """
    Listens for audio commands and uses Google Speech API to produce a transcript of audio
    :precondition: Must be connected to Internet.
    :return: A string that gives information about the user input.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        play_audio("How can I help you?", "en")
        audio = r.listen(source)
        try:
            return r.recognize_google(audio)
        except:
            return ""


def get_joke(num_jokes):
    """
    Gets joke from top n jokes from reddit.
    :precondition: Need a praw.ini file in the directory specified by $HOME/.config 
                   If the HOME environment is defined (Linux and Mac OS systems).
                   For more information: https://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html#praw-ini
    :param num_jokes: This is how many times the user has asked for a joke.
    :return: A string, ready to be read out, that tells a joke.
    """
    reddit = praw.Reddit(client_id = config.reddit_client_id, client_secret = config.reddit_secret, user_agent = config.reddit_agent)
    list_of_jokes = []

    # get the top num_jokes jokes and return the last one, sort of randomization of the top n jokes 
    for submission in reddit.subreddit('jokes').top(time_filter='month'):
        joke_i = (submission.title, submission.selftext)
        if len(joke_i[1]) < 100:
            list_of_jokes.append(joke_i)
        if len(list_of_jokes) > num_jokes:
            break
    
    # replace any new lines with a period in the punchline for dramatic effect
    list_of_jokes[num_jokes][1].replace('\n', '. ')
    result = f'Here is a joke. Here is how it goes. {list_of_jokes[num_jokes][0]}. {list_of_jokes[num_jokes][1]}'
    return result


def get_location():
    """
    Gets current location based on IP address using geocoder API
    :precondition: must be in US city.
    :return: A string that returns US city.
    """
    # get location by IP address
    myloc = geocoder.ip('me')
    return myloc.city


def get_weather():
    """
    Gets the current weather of current US city.
    :return: A string, ready to be read out, that gives information about the weather.
    """
    owm = pyowm.OWM(config.omw_secret)
    my_location = get_location()
    # observation = owm.weather_at_place('Austin, US')
    observation = owm.weather_at_place(my_location)
    w = observation.get_weather()
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
    Gets the current time using datetime package.
    :return: A string, ready to be read out, that gives information about the time.
    """
    currentDT = datetime.datetime.now()
    date = currentDT.strftime("%a, %b %d, %Y")
    time = currentDT.strftime("%I %M %p")
    result = f'It is {time} on {date}.'
    return result


def play_audio(string, language):
    """
    saves the string as an mp3 audio file using google text to speech and then uses os shell commands to playback the file.
    :param string: string to be read
    :param language: language to be output
    :return: audio playback
    """
    str = string
    myobj = gTTS(text=str, lang=language, slow=False)
    myobj.save("welcome.mp3")

    if sys.platform.startswith('darwin') or sys.platform.startswith('linux'):
        os.system("mpg321 welcome.mp3")

    elif sys.platform.startswith('win32'):
        os.system("welcome.mp3")

def main():
    language = 'en'
    num_jokes = random.randint(0, n)
    while True:
        command = get_audio()

        # if more than one key-word is said to Digi, the first key word that is said will be used
        if "joke" in command:
            str =  get_joke(num_jokes)
            play_audio(str, language)
            if num_jokes < 100:
                num_jokes = num_jokes + 1
            else:
                num_jokes = 0

        elif "weather" in command:
            play_audio(get_weather(), language)

        elif "time" in command:
            play_audio(get_time(), language)

        elif command == "goodbye":
            play_audio('goodbye', language)
            break

        elif command == "":
            play_audio('goodbye', language)
            break


if __name__ == "__main__":
    main()
