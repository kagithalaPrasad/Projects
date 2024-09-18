from django.shortcuts import render
import requests

api_key = '77dd13084d55a01e6099e3c24d606d45'

def index(request):
    current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    forecast_url = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}'

    if request.method == 'POST':
        city1 = request.POST['city1']
        city2 = request.POST.get('city2', None)

        weather_data1 = fetch_weather_and_forecast(city1, api_key, current_weather_url, forecast_url)

        if city2:
            weather_data2 = fetch_weather_and_forecast(city2, api_key, current_weather_url, forecast_url)
        else:
            weather_data2 = None

        context = {
            'weather_data1': weather_data1,
            'weather_data2': weather_data2,
        }

        return render(request, 'weather_app/index.html', context)
    else:
        return render(request, 'weather_app/index.html')


def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    # Get current weather
    response = requests.get(current_weather_url.format(city, api_key)).json()
    lat, lon = response['coord']['lat'], response['coord']['lon']
    
    # Get 5-day forecast
    forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()
    
    # Parse current weather data
    weather_data = {
        'city': city,
        'temperature': round(response['main']['temp'] - 273.15, 2),
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon'],
    }
    
    # Parse forecast data
    forecast_data = []
    for item in forecast_response['list']:
        forecast_data.append({
            'datetime': item['dt_txt'],
            'temperature': round(item['main']['temp'] - 273.15, 2),
            'description': item['weather'][0]['description'],
            'icon': item['weather'][0]['icon'],
        })
    
    return {
        'current_weather': weather_data,
        'forecast': forecast_data
    }
