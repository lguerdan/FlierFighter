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
    print lat
    print lon
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

def getLyftData(destination, origin):
    return 0