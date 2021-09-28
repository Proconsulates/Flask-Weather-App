from flask import Flask, render_template, request, redirect
  
import json
import math
import urllib.request
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
  
@app.route('/', methods=['GET'])
def index():
    ip = urllib.request.urlopen('https://ipv4.icanhazip.com/')
    print(request.remote_addr)
    req = urllib.request.urlopen('https://ip-geolocation.whoisxmlapi.com/api/v1?apiKey=' + os.getenv("GEOLOCATION_API_KEY") + '&ipAddress=' + ip.read().decode('utf8'))

    return redirect(location="/weather?location=" + json.loads(str(str(req.read())).replace('b', '').replace("'", ''))['location']['city'])

@app.route('/weather', methods=['GET'])
def weather_route():
    location = request.args.get('location')
    if location == None: 
        return '<h1>Please specify a location!</h1><br/><a href="/">Home Page</a>'
  
    try:
        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + location + '&appid=' + os.getenv("WEATHER_API_KEY")).read()
    
        list_of_data = json.loads(source)

        fahrenheit = math.floor(list_of_data['main']['temp'] - 273.15) * 9/5 + 32
    
        data = {
            "country_code": str(list_of_data['sys']['country']),
            "coordinate": str(list_of_data['coord']['lon']) + ' ' 
                        + str(list_of_data['coord']['lat']),
            "temp": str(fahrenheit),
            "pressure": str(list_of_data['main']['pressure']),
            "humidity": str(list_of_data['main']['humidity']),
        }
        
        return render_template('index.html', data=data, location=location)
    except: 
        return '<script>alert("Invalid Location");document.location.href=`${new URL(document.location.href).origin}/`;</script>'
  
  
if __name__ == '__main__':
    app.run(debug = True)





"""
so it's kind of embarassing that there is .9 percent more html than there is python in this repo,
so this comment will make it so that this repo looks cooler and has a lot more python code with this passage:



We’re no strangers to love,
You know the rules and so do I.
A full commitment’s what I’m thinking of,
You wouldnt get this from any other guy.

I just wanna tell you how I’m feeling,
Gotta make you understand…

Never gonna give you up,
Never gonna let you down,
Never gonna run around and desert you.
Never gonna make you cry,
Never gonna say goodbye,
Never gonna tell a lie and hurt you.

We’ve known each other for so long
Your heart’s been aching
But you’re too shy to say it.
Inside we both know what’s been going on,
We know the game and we’re gonna play it.

Annnnnd if you ask me how I’m feeling,
Don’t tell me you’re too blind to see…

Never gonna give you up,
Never gonna let you down,
Never gonna run around and desert you.
Never gonna make you cry,
Never gonna say goodbye,
Never gonna tell a lie and hurt you.

Never gonna give you up,
Never gonna let you down,
Never gonna run around and desert you.
Never gonna make you cry,
Never gonna say goodbye,
Never gonna tell a lie and hurt you.

Give you up. give you up.
Give you up, give you up.
Never gonna give
Never gonna give, give you up.
Never gonna give
Never gonna give, give you up.

We’ve known each other for so long
Your heart’s been aching
But you’re too shy to say it.
Inside we both know what’s been going on,
We know the game and we’re gonna play it.

I just wanna tell you how I’m feeling,
Gotta make you understand…

Never gonna give you up,
Never gonna let you down,
Never gonna run around and desert you.
Never gonna make you cry,
Never gonna say goodbye,
Never gonna tell a lie and hurt you.

Never gonna give you up,
Never gonna let you down,
Never gonna run around and desert you.
Never gonna make you cry,
Never gonna say goodbye,
Never gonna tell a lie and hurt you.

Never gonna give you up,
Never gonna let you down,
Never gonna run around and desert you.
Never gonna make you cry,
Never gonna say goodbye,
Never gonna tell a lie and hurt you.
"""