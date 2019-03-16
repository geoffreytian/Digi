import pyaudio
import praw
import pyowm
import time
import speech_recognition as sr
import os


# def audio_int(num_samples=50):
#     """ Gets average audio intensity of your mic sound. You can use it to get
#             average intensities while you're talking and/or silent. The average
#             is the avg of the 20% largest intensities recorded.
#         """
#     p = pyaudio.PyAudio()
#
#     stream = p.open(format=FORMAT,
#                     channels=CHANNELS,
#                     rate=RATE,
#                     input=True,
#                     frames_per_buffer=CHUNK)
#
#     values = [math.sqrt(abs(audioop.avg(stream.read(CHUNK), 4)))
#               for x in range(num_samples)]
#
#     values = sorted(values, reverse=True)
#     r = sum(values[:int(num_samples * 0.2)]) / int(num_samples * 0.2)
#
#     print("Average audio intensity is: ", r)
#     stream.close()
#     p.terminate()
#
#     if r > THRESHOLD:
#         listen(0)
#
#     threading.Timer(SILENCE_LIMIT, audio_int).start()


# obtain audio from the microphone
def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

        try:
            print("Google thinks you said:\n" + r.recognize_google(audio))
            return r.recognize_google(audio)

        except:
            pass


# def listen(x):
#     r = sr.Recognizer()
#     if x == 0:
#         system('say Hi. How can I help?')
#     with sr.Microphone() as source:
#         audio=r.listen(source)
#     try:
#         text = r.recognize_google(audio)
#         y = process(text.lower())
#         return y
#     except:
#         if x == 1:
#             system('say Good Bye!')
#         else:
#             system('say I did not get that. Please say again.')
#             listen(1)

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
    result = f'Here is a joke. It is called {list_of_jokes[num_jokes][0]}. Here is how it goes. {list_of_jokes[num_jokes][1]}'
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
    result = f'The temperature right now is: {temp} Fahrenheit. It is projected to be between {temp_min} and {temp_max}. '
    return result


def get_time():
    """
    Gets the current time using time module.
    :return: A string, ready to be read out, that gives information about the time.
    """
    local_time = time.ctime(time.time())
    local_time = local_time.split(' ')
    result = f'The time right now is {local_time[3]}.'
    return result

def main():
    num_jokes = 0
    while True:

        command = get_audio()
        if "joke" in command:
            os.system("say " + get_joke(num_jokes))
            print(get_joke(num_jokes))
            num_jokes = num_jokes + 1

        if "weather" in command:
            os.system("say " + get_weather())

        if "time" in command:
            os.system("say " + get_time())

        if command == "goodbye":
            break


if __name__ == "__main__":
    main()
