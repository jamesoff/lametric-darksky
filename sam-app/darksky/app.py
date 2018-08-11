import os
import darksky


def lambda_handler(event, context):
    """Sample pure Lambda function

    Arguments:
        event LambdaEvent -- Lambda Event received from Invoke API
        context LambdaContext -- Lambda Context runtime methods and attributes

    Returns:
        dict -- {'statusCode': int, 'body': dict}
    """

    forecast = darksky.getDarkSkyWeather(
        os.environ['darksky_apikey'],
        os.environ['latitude'],
        os.environ['longitude'])
    output = darksky.convertOutput(forecast)
    darksky.pushForecast(
        output,
        os.environ['lametric_key'],
        os.environ['lametric_token'])

if __name__ == '__main__':
    lambda_handler(None, None)
