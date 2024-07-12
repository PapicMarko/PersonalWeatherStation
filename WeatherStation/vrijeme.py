import serial
import time

# Otvaranje serijske veze (prilagodi 'COM3' tvojoj situaciji)
ser = serial.Serial('COM3', 9600)  # Provjeri koji COM port koristi tvoj Arduino

while True:
    if ser.in_waiting > 0:
        # Čitanje serijskih podataka
        arduino_data = ser.readline().decode('utf-8').rstrip()
        
        # Dohvaćanje trenutnog vremena
        current_time = time.strftime("%H:%M:%S", time.localtime())
        
        # Ispis podataka s vremenom
        print(f"Time: {current_time} - {arduino_data}")
