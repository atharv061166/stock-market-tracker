import requests
import logging

API_KEY = '1G75BDBQFENFALZD'
BASE_URL = 'https://www.alphavantage.co/query'

logger = logging.getLogger(__name__)

def get_stock_data(symbol):
    try:
        response = requests.get(BASE_URL, params={
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol,
            'apikey': API_KEY
        })
        response.raise_for_status()
        data = response.json()
        logger.info(f"API response for {symbol}: {data}")
        if "Time Series (Daily)" not in data:
            error_message = data.get("Error Message", "Invalid response from API")
            raise ValueError(error_message)
        time_series = data.get('Time Series (Daily)', {})
        sorted_dates = sorted(time_series.keys(), reverse=True)
        latest_date = sorted_dates[0]
        latest_data = time_series[latest_date]
        historical_data = [
            {
                'date': date,
                'open': time_series[date]['1. open'],
                'high': time_series[date]['2. high'],
                'low': time_series[date]['3. low'],
                'close': time_series[date]['4. close'],
                'volume': time_series[date]['5. volume']
            }
            for date in sorted_dates
        ]
        return {
            'symbol': symbol,
            'date': latest_date,
            'open': latest_data['1. open'],
            'high': latest_data['2. high'],
            'low': latest_data['3. low'],
            'close': latest_data['4. close'],
            'volume': latest_data['5. volume'],
            'historical_data': historical_data
        }
    except requests.RequestException as e:
        raise Exception('Error fetching stock data') from e
    except ValueError as e:
        raise Exception(str(e)) from e