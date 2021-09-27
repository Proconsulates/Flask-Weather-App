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