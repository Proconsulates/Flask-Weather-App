from flask import Flask, render_template, request, redirect
  
import json
import math
import urllib.request
import socket

app = Flask(__name__)
  
@app.route('/', methods=['GET'])
def index():
    ip = urllib.request.urlopen('https://ipv4.icanhazip.com/')
    req = urllib.request.urlopen('https://ip-geolocation.whoisxmlapi.com/api/v1?apiKey=at_FTf7sfz2mDkrTJtupEBqh4VaY0MQB&ipAddress=' + ip.read().decode('utf8'))

    return redirect(location="/weather?location=" + json.loads(str(str(req.read())).replace('b', '').replace("'", ''))['location']['city'])

@app.route('/weather', methods=['GET'])
def weather_route():
    location = request.args.get('location')
    if location == None: 
        return '<h1>Please specify a location!</h1><br/><a href="/">Home Page</a>'
    
    api = '2f758f104006786fe5a7505e33bc8f6e'
  
    try:
        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + location + '&appid=' + api).read()
    
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
    except: return '<h1>Invalid Location</h1><br/><a href="/">Home Page</a>'
  
  
if __name__ == '__main__':
    app.run(debug = True)