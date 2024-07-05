import requests

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_temperature(lat, long):
    weather_api_key = 'bf12a4c39ad553044b01fa3896b83239'
    weather_api_url = f'https:/api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&units=metric&appid={weather_api_key}'
    response = requests.get(weather_api_url)
    return response.json()

def get_location_temperature(ip):
    geo_api_url = f'https://ipinfo.io/{ip}?770a41bca6538d'
    response = requests.get(geo_api_url).json()
    if 'bogon' in response:
        return response
    
    else:
        location = response.get('loc', '').split(',')
        lat = location[0] if len(location) > 1 else None
        long = location[1] if len(location) > 1 else None
        
        return response.get('city'), get_temperature(lat, long)