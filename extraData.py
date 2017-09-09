from geopy.geocoders import Nominatim
import requests
import httplib, urllib, base64
import json


def getWeatherData(location, date):
    '''
    https://earthnetworks.azure-api.net/
    getStationList/data/locations/v3/
    stationlist?latitude=39.1833&longitude=-77.2667
    &verbose=true&&subscription-key=?????
    '''
    geolocator = Nominatim()
    location = geolocator.geocode(location)
    lat = str(location.latitude)
    lon = str(location.longitude)
    # print lat
    # print lon
    # https://earthnetworks.azure-api.net/data/forecasts/v1/daily?locationtype=
    # latitudelongitude&location=34.1144504,-118.7778678

    params = urllib.urlencode({
        # Request parameters
        'verbose': 'true',
        'cultureInfo': 'en-en',
    })
    headers = {
        'Ocp-Apim-Subscription-Key': '391c2d3855f34ce5b1f82af1340e56a1',
    }
    try:
        conn = httplib.HTTPSConnection('earthnetworks.azure-api.net')
        conn.request("GET",
            "/data/forecasts/v1/daily?locationtype=latitudelongitude&location=0,0&%s" % params,
            "{body}",
            headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        # print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
        data = []
    
    for day in data['dailyForecastPeriods']:
        if date[5:9] == day['forecastDateLocalStr'][5:9]: # look at just the month/day
            # get weather data
            return day['detailedDescription']
    # we assume data is in a format 2017-09-09...
    return None 


'''
Gets the estimated fare and offers to order a lyft ride
'''
def getLyftData(destination, origin):
    authToken = \
        ("N+3uBHIGeHDpISQtE++3eS0O/" +
        "3HdeK4bGLXm2DEsOm312fJD93VnnNIV/" +
        "EyTg5HlrQk8R/330TrDN8fV3uk2oT7LDxpqmPMDccmk6B9zQHws" +
        "/txDw9npKjg=")
    geolocator = Nominatim()
    destinationL = geolocator.geocode(destination)
    latD = destinationL.latitude
    lonD = destinationL.longitude
    originL = geolocator.geocode(origin)
    latO = originL.latitude
    lonO = originL.longitude
    headers = {
        'Authorization': 'bearer '+authToken
    }

    params = (
        ('start_lat', latO),
        ('start_lng', lonO),
        ('end_lat', latD),
        ('end_lng', lonD),
        ('ride_type', 'lyft'),
    )

    rideData = [] # A list of dictionaries about ride data
    overallDuration = 0
    r = requests.get('https://api.lyft.com/v1/cost', headers=headers, params=params)
    if r.status_code == 200:
        data = json.loads(r.text)
        for costJson in data['cost_estimates']:
            rideEntry = {}
            rideEntry['display_name'] = costJson['display_name']
            rideEntry['estimated_cost_cents_max'] = costJson['estimated_cost_cents_max']
            rideEntry['estimated_cost_cents_min'] = costJson['estimated_cost_cents_min']
            rideEntry['primetime_percentage'] = costJson['primetime_percentage']
            rideData.append(rideEntry)
            overallDuration = costJson['estimated_duration_seconds']
        return (rideData, overallDuration)
    return None