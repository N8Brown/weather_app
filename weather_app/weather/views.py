from django.shortcuts import render

# https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode=04090&distance=5&API_KEY=366D1BA7-2827-4B6B-B434-4C432C57F9B8

# Create your views here.
def home(request):
    import json
    import requests

    api_request = requests.get("https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode=04090&distance=5&API_KEY=366D1BA7-2827-4B6B-B434-4C432C57F9B8")

    try:
        api_response = json.loads(api_request.content)
    except Exception as e:
        api_response = "Error fetching data."

    return render(request, 'home.html', {
        'api_response': api_response
    })
