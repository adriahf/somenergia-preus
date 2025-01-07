"""
Script to fetch indexed electricity prices from Som Energia's API, combine them
with previously saved data, and save results to a CSV file named with the
current date.
"""

import requests
import pytz
import pandas as pd

from datetime import datetime, timedelta


def get_current_time_in_barcelona():
    """
    Return the current datetime in the Barcelona (Europe/Madrid) timezone.
    """
    barcelona_tz = pytz.timezone('Europe/Madrid')
    return datetime.now(barcelona_tz)


def get_indexed_prices(tariff, geo_zone):
    """
    Fetch indexed prices from Som Energia's API for the given tariff and
    geographical zone.

    :param tariff: Tariff code (e.g., "2.0TD").
    :param geo_zone: Geographical zone (e.g., "PENINSULA").
    :return: Parsed JSON response as a dictionary.
    :raises Exception: If the request fails (non-200 status code).
    """
    url = "https://api.somenergia.coop/data/indexed_prices"
    params = {
        "tariff": tariff,
        "geo_zone": geo_zone
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    msg = f"Failed to fetch data: {response.status_code}"
    raise Exception(msg)


def filter_day_data(prices):
    """
    Filter and format day data from the API's prices response. Adjusts for the
    one-hour shift in the provided data.

    :param prices: Dictionary from the API containing 'data', 'curves', and
                   'price_euros_kwh'.
    :return: A tuple of (list of prices, list of corresponding datetimes).
    """
    price_data = prices['data']['curves']['price_euros_kwh']
    first_date = datetime.fromisoformat(prices['data']['first_date'])

    # The first hour is shifted by 1 hour, so we need to adjust it
    first_date -= timedelta(hours=1)

    filtered_prices = []
    time_labels = []

    for i, price in enumerate(price_data):
        current_time = first_date + timedelta(hours=i)
        filtered_prices.append(price)
        time_labels.append(current_time)

    return filtered_prices, time_labels


def main():
    """
    Main execution flow: 
    1. Load yesterday's CSV data (if exists).
    2. Fetch today's indexed prices from Som Energia.
    3. Filter day data and combine with yesterday's data.
    4. Save combined data to a new CSV (named with today's date).
    """
    # Build filename for yesterday's CSV
    yesterday_date_str = (get_current_time_in_barcelona() - timedelta(days=1)).strftime('%Y-%m-%d')
    filename_read = f"prices_somenergia_{yesterday_date_str}.csv"

    try:
        df_read = pd.read_csv(filename_read)
    except FileNotFoundError:
        df_read = pd.DataFrame(columns=["time", "price"])

    # Fetch and process data
    tariff = "2.0TD"
    geo_zone = "PENINSULA"
    indexed_prices = get_indexed_prices(tariff, geo_zone)

    prices, time_labels = filter_day_data(indexed_prices)

    # Create new DataFrame from the fetched data
    df_new = pd.DataFrame({"time": time_labels, "price": prices})

    # Replace null values with None
    df_new = df_new.where(pd.notnull(df_new), None)

    # Convert 'time' column to datetime for both new and existing dataframes
    df_new['time'] = pd.to_datetime(df_new['time'])
    df_read['time'] = pd.to_datetime(df_read['time'])

    # Concatenate the dataframes
    df_combined = pd.concat([df_read, df_new], ignore_index=True)

    # Drop duplicates, keeping the latest entry for each 'time'
    df_combined.drop_duplicates(subset='time', keep='last', inplace=True)

    # Sort the dataframe by 'time' in ascending order
    df_combined.sort_values(by='time', inplace=True)
    df_combined.reset_index(drop=True, inplace=True)

    # Build filename for today's CSV
    today_date_str = get_current_time_in_barcelona().strftime('%Y-%m-%d')
    filename_write = f"prices_somenergia_{today_date_str}.csv"

    # Save combined DataFrame to CSV
    df_combined.to_csv(filename_write, index=False)
    print(f"File saved: {filename_write}")


if __name__ == "__main__":
    main()
