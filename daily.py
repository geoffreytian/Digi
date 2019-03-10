import pyaudio
import praw
import pyowm

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
    reddit = praw.Reddit('Digi', user_agent = 'Digi by Matthew and Geoff')
    # BTW, you need a praw.ini file for this. Otherwise this won't work. I'll send you the praw.ini file some time.
    # put it here:
    #In the directory specified by $HOME/.config if the HOME environment variable is defined (Linux and Mac OS systems).
    # For more information: https://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html#praw-ini

    for submission in reddit.subreddit('jokes').top(time_filter='month', limit=1):
        print(f'Here is a joke. It is called "{submission.title}".')
        print(submission.selftext)


def get_weather():
    owm = pyowm.OWM('a07c45f49457239d1504a9fe6fa19b3d')
    reg = owm.city_id_registry()
    reg.ids_for('Austin')


    observation = owm.weather_at_place('')
    w = observation.get_weather()
    print(w)
    w.get_wind()
    w.get_humidity()
    w.get_temperature('fahrenheit')


def main():
    #get_joke()
    get_weather()

if __name__ == "__main__":
    main()