"""Send DarkSky info to LaMetric."""

import requests


def getDarkSkyWeather(apikey, latitude, longitude):
    result = requests.get(
        "https://api.forecast.io/forecast/{api_key}/{latitude},{longitude}?units=uk2&exclude=flags,hourly,alerts".
        format(
            api_key=apikey,
            latitude=latitude,
            longitude=longitude),
        headers={'Accept-Encoding': 'gzip'})
    return result.json()


def pickIcon(icon):
    icon_map = {
        "clear-day": "a2282",
        "cloudy": "a2283",
        "rain": "a2284",
        "sleet": "a160",
        "partly-cloudy-day": "a2286",
        "snow": "a2289",
        "clear-night": "i2314",
        "wind": "a2440",
        "fog": "i2158",
        "partly-cloudy-night": "i2152"
    }
    return icon_map.get(icon, "i73")


def convertOutput(forecast):
    temperature = round(float(forecast['currently']['temperature']))
    icon = pickIcon(forecast['currently']['icon'])
    minutely_summary = forecast['minutely']['summary']

    dailys = forecast['daily']['data']
    min_time = None
    min_temp = None
    max_temp = None
    summary = None
    for day in dailys:
        if not min_time or day['time'] < min_time:
            min_time = day['time']
            min_temp = round(float(day['temperatureMin']))
            max_temp = round(float(day['temperatureMax']))
            summary = day['summary']
            summary_icon = pickIcon(day['icon'])

    ret_val = {
        'frames': [{
            'index': 0,
            'text': u"{}° {}".format(temperature, minutely_summary),
            'icon': icon
        }]
    }

    if min_time:
        ret_val['frames'].append({
            'index': len(ret_val),
            'text': summary,
            'icon': summary_icon
        })
        ret_val['frames'].append({
            'index': len(ret_val),
            'text': u"{}°".format(max_temp),
            'icon': 'i120'
        })
        ret_val['frames'].append({
            'index': len(ret_val),
            'text': u"{}°".format(min_temp),
            'icon': 'i124'
        })

    return ret_val


def pushForecast(output, key, token):
    # local_url = 'https://192.168.3.31:4343/api/v1/dev/widget/update/com.lametric.{}/1'
    remote_url = 'https://developer.lametric.com/api/v1/dev/widget/update/com.lametric.{}/1'.format(key)
    requests.post(
        remote_url,
        json=output,
        headers={
            'X-Access-Token': token
        },
        verify=False)


if __name__ == '__main__':
    forecast = getDarkSkyWeather()
    output = convertOutput(forecast)
    pushForecast(output)
