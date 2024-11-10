import pandas as pd

def time_to_milliseconds(time_str):
    if pd.isna(time_str):
        return None
    try:
        minutes, seconds = time_str.split(':')
        seconds, milliseconds = seconds.split('.')
        total_milliseconds = (int(minutes) * 60 * 1000) + (int(seconds) * 1000) + int(milliseconds)
        return total_milliseconds
    except ValueError:
        return None