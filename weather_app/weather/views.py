from django.shortcuts import render

# api_request = requests.get('http://api.weatherapi.com/v1/forecast.json?key=4f506553666f42c0b5f190311211706&q=04090&days=3&aqi=no&alerts=yes')


def weather(request):
    import json, requests, datetime
    from .api_key import key

    if request.method == 'POST':
        if len(request.POST['location']) > 0:
            location = request.POST['location']

            api_request = requests.get('http://api.weatherapi.com/v1/forecast.json?key=' + key + '&q=' + location + '&days=3&aqi=no&alerts=yes')
        
            try:
                api_response = json.loads(api_request.content)
            except:
                api_response = 'Error'

            if api_response == 'Error':
                pass
            else:
                if 'error' in api_response:
                    if api_response['error']['code'] == 1006:
                        alert = f"You searched: {location}. {api_response['error']['message']}"
                    else:
                        alert = "Something went wrong. Please try again later."
                    return render(request, 'weather.html', {'alert':alert})
                else:
                    days_str = [day['date']+' ' for day in api_response['forecast']['forecastday']]
                    sunrises_str = [day['astro']['sunrise'] for day in api_response['forecast']['forecastday']]
                    sunsets_str = [day['astro']['sunset'] for day in api_response['forecast']['forecastday']]

                    sunrises_day_time = list(map(str.__add__, days_str, sunrises_str))
                    sunsets_day_time = list(map(str.__add__, days_str, sunsets_str))

                    sunrises = [datetime.datetime.strptime(date, '%Y-%m-%d %I:%M %p') for date in sunrises_day_time]
                    sunsets = [datetime.datetime.strptime(date, '%Y-%m-%d %I:%M %p') for date in sunsets_day_time]

                    day_segments = [datetime.datetime.strptime(day['date'], '%Y-%m-%d').ctime().split(' ') for day in api_response['forecast']['forecastday']]

                    day1 = 'Today'
                    day2 = day_segments[1][0] + ' ' + day_segments[1][2]
                    day3 = day_segments[2][0] + ' ' + day_segments[2][2]
                    
                    current_time = datetime.datetime.strptime(api_response['location']['localtime'], '%Y-%m-%d %H:%M')

                    context = {
                        'api_response':api_response,
                        'current_time':current_time,
                        'day1':day1,
                        'day2':day2,
                        'day3':day3,
                        'sunrises':sunrises,
                        'sunsets':sunsets,
                    }

                    return render(request, 'weather.html', context)
        else:
            alert = "Please enter a location."
            return render(request, 'weather.html', {'alert':alert})
    else:
        return render(request, 'weather.html')