import requests
import pandas as pd
import datetime
import smtplib
from email.mime.text import MIMEText

# Replace 'your_api_key_here' with your WeatherAPI key
api_key = 'ed296bbe7b374b40908121219230610'

def get_weather_data(locations):
    weather_data = {}
    for location in locations:
        url = f'https://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days=7&aqi=no&alerts=no'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            daily_data = data['forecast']['forecastday']
            weather_data[location] = daily_data
        else:
            print(f'Failed to retrieve data for {location}')
    return weather_data

def tabulate_weather_data(weather_data):
    all_tables_str = ""
    for location, data in weather_data.items():
        table_data = []  # Reset table_data for each location
        for day_data in data:
            date = day_data['date']
            day_name = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%A')
            formatted_date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%Y')
            hour_temps = [hour_data['temp_c'] for hour_data in day_data['hour']]
            
            min_temp_index = hour_temps.index(min(hour_temps))
            max_temp_index = hour_temps.index(max(hour_temps))
            
            min_temp_time = day_data['hour'][min_temp_index]['time'][11:16]
            min_temp = day_data['hour'][min_temp_index]['temp_c']
            
            max_temp_time = day_data['hour'][max_temp_index]['time'][11:16]
            max_temp = day_data['hour'][max_temp_index]['temp_c']
            
            avg_temp = int(sum(hour_temps) / len(hour_temps))
            
            table_data.append([formatted_date, day_name, f'{min_temp_time} ({min_temp}°C)', f'{max_temp_time} ({max_temp}°C)', avg_temp])
        
        df = pd.DataFrame(table_data, columns=['Date', 'Day of the Week', 'Time of Min Temp (°C)', 'Time of Max Temp (°C)', 'Average Temp (°C)'])
        table_str = df.to_html(classes='table table-bordered', index=False, escape=False)  # Using pandas to_html method
        table_with_title = f"<h3>Weather Report for {location}</h3>{table_str}"
        all_tables_str += table_with_title  # Concatenate the table strings
    return all_tables_str

def send_email(table_str):
    recipients = ['liran.iphone@icloud.com', 'blm017@gmail.com', 'nickol2007@gmail.com']
    sender = 'blm017@gmail.com'
    subject = 'תחזית מזג האוויר ע״י לירן מיכאלי'
    body = f'Daily Weather Report:<br>{table_str}'

    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('blm017@gmail.com', 'bqbtgzpkorvwupxy')
        server.sendmail(sender, recipients, msg.as_string())

def main():
    locations = ['Jerusalem,Israel', 'Bat Yam,Israel']
    weather_data = get_weather_data(locations)
    weather_table = tabulate_weather_data(weather_data)
    send_email(weather_table)

if __name__ == '__main__':
    main()
