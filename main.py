import serial
import time
import pandas as pd
import os

# Funkcija za izračunavanje pomičnog prosjeka
def moving_average(data, window_size):
    return round(sum(data[-window_size:]) / window_size, 2)

# Funkcija za generiranje imena datoteke
def generate_filename(base_name):
    suffix = 'a'
    while os.path.exists(f"{base_name}_{suffix}.csv"):
        suffix = chr(ord(suffix) + 1)
    return f"{base_name}_{suffix}.csv"

# Serijski port i baud rate - provjerite koji je vaš port i prilagodite
ser = serial.Serial('COM3', 9600)  # Zamijenite 'COM3' s vašim portom

# Funkcija za generiranje novog imena datoteke na temelju trenutnog datuma
def get_new_filename():
    date_str = time.strftime("%d.%m")
    filename_base = f"sensor_data_{date_str}"
    return generate_filename(filename_base)

filename = get_new_filename()
data = []
reading_counter = 0

while True:
    if ser.in_waiting > 0:
        # Čitanje serijskih podataka
        arduino_data = ser.readline().decode('utf-8').rstrip()

        # Dohvaćanje trenutnog vremena i datuma
        current_time = time.strftime("%H:%M:%S", time.localtime())
        current_date = time.strftime("%d.%m", time.localtime())
        
        # Provjera promjene datuma i generiranje novog imena datoteke
        if f"sensor_data_{current_date}" not in filename:
            filename = get_new_filename()

        # Ispis podataka s vremenom
        print(f"Time: {current_time} - {arduino_data}")
        
        # Razdvajanje podataka
        if "Vlažnost" in arduino_data:
            # Razdvoji string u dijelove
            parts = arduino_data.split(" ")
            humidity = round(float(parts[1][:-1]), 2)  # Ukloni znak '%' i konvertiraj u float
            temperature = round(float(parts[4][:-2]), 2)  # Ukloni znak '°C' i konvertiraj u float
            
            # Dodavanje podataka u listu s inicijalnim vrijednostima
            data.append([current_time, humidity, temperature, None, None, None, None, None, None])  # Dodavanje dodatnih polja za prosjeke i anemometar
        
        if "Tlak" in arduino_data:
            # Razdvoji string u dijelove
            parts = arduino_data.split(" ")
            pressure = round(float(parts[1]), 2)
            
            # Ažuriranje zadnjeg retka s podacima za tlak
            if data and data[-1][3] is None:
                data[-1][3] = pressure

        if "Napon" in arduino_data:
            # Razdvoji string u dijelove
            parts = arduino_data.split(" ")
            
            # Provjera duljine niza dijelova kako bi se izbjegla greška
            if len(parts) >= 5:
                try:
                    voltage = round(float(parts[1]), 2)  # Ukloni 'V' i konvertiraj u float
                    wind_speed = round(float(parts[4]), 2)  # Ukloni 'm/s' i konvertiraj u float
                    
                    # Dodajte vrijednosti u zadnji redak podataka (ako je dostupan)
                    if data:
                        data[-1][7] = voltage
                        data[-1][8] = wind_speed
                except ValueError as e:
                    print(f"Error converting to float: {e}, parts: {parts}")

        # Povećavanje brojača očitanja
        reading_counter += 1
        
        # Izračunavanje srednjih vrijednosti nakon svakih 10 očitanja
        if reading_counter % 10 == 0 and len(data) >= 10:
            avg_humidity = moving_average([row[1] for row in data if row[1] is not None], 10)
            avg_temperature = moving_average([row[2] for row in data if row[2] is not None], 10)
            avg_pressure = moving_average([row[3] for row in data if row[3] is not None], 10)
            avg_voltage = moving_average([row[7] for row in data if row[7] is not None], 10)
            avg_wind_speed = moving_average([row[8] for row in data if row[8] is not None], 10)
            
            print(f"Moving Averages - Vlažnost: {avg_humidity}%, Temperatura: {avg_temperature}°C, Tlak: {avg_pressure} hPa, Prosječni napon: {avg_voltage} V, Prosječna brzina vjetra: {avg_wind_speed} m/s")
            
            # Dodavanje prosječnih vrijednosti u zadnji redak
            data[-1][4] = avg_humidity
            data[-1][5] = avg_temperature
            data[-1][6] = avg_pressure

        # Spremanje podataka u CSV datoteku
        df = pd.DataFrame(data, columns=['Vrijeme', 'Vlažnost (%)', 'Temperatura (°C)', 'Tlak (hPa)', 'Prosječna Vlažnost (%)', 'Prosječna Temperatura (°C)', 'Prosječni Tlak (hPa)', 'Napon (V)', 'Brzina vjetra (m/s)'])
        df.to_csv(filename, index=False)
