import pyaudio
import praw
import pyowm
import time


def audio_int(num_samples=50):
    """ Gets average audio intensity of your mic sound. You can use it to get
            average intensities while you're talking and/or silent. The average
            is the avg of the 20% largest intensities recorded.
        """
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    values = [math.sqrt(abs(audioop.avg(stream.read(CHUNK), 4)))
              for x in range(num_samples)]

    values = sorted(values, reverse=True)
    r = sum(values[:int(num_samples * 0.2)]) / int(num_samples * 0.2)

    print("Average audio intensity is: ", r)
    stream.close()
    p.terminate()

    if r > THRESHOLD:
        listen(0)

    threading.Timer(SILENCE_LIMIT, audio_int).start()


def listen(x):
    r = rs.Recognizer()
    if x == 0:
        system('say Hi. How can I help?')
    with rs.Microphone() as source:
        audio=r.listen(source)
    try:
        text = r.recognize_google(audio)
        y = process(text.lower())
        return y
    except:
        if x == 1:
            system('say Good Bye!')
        else:
            system('say I did not get that. Please say again.')
            listen(1)


def get_joke():
    """
    Gets the top joke of the month on reddit.com/r/jokes.
    :return: returns list of tuples with title being at 0th index and joke being at 1st index.
    """
    reddit = praw.Reddit('Digi', user_agent = 'Digi by Matthew and Geoff')
    # BTW, you need a praw.ini file for this. Otherwise this won't work. I'll send you the praw.ini file some time.
    # put it here:
    #In the directory specified by $HOME/.config if the HOME environment variable is defined (Linux and Mac OS systems).
    # For more information: https://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html#praw-ini


    list_of_jokes = []
    for submission in reddit.subreddit('jokes').top(time_filter='month', limit=100):
        print(f'Here is a joke. It is called "{submission.title}".')
        print(submission.selftext)
        joke_i = (submission.title, submission.selftext)
        list_of_jokes.append(joke_i)
    return list_of_jokes


def get_weather():
    """
    Gets the current weather of ATX.
    :return:
    """
    owm = pyowm.OWM('a07c45f49457239d1504a9fe6fa19b3d')
    observation = owm.weather_at_id(4671654) #THIS IS AUSTIN, TX'S ID
    w = observation.get_weather()
    w.get_humidity()
    w.get_temperature('fahrenheit')
    print(f"wind: {w.get_wind()} humidity: {w.get_humidity}. temp: {w.get_temperature('fahrenheit')}")
    for k, v in w.get_temperature('fahrenheit').items():
        print(k, v)
    return w.get_temperature('fahrenheit')


def get_time():
    """
    Gets the current time using time module.
    :return: String which says the current time.
    """
    local_time = time.ctime(time.time())
    return local_time.split(' ')[3]





def main():
    #get_joke()
    get_weather()
    get_time()
if __name__ == "__main__":
    main()