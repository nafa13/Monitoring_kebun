import requests
import time
import random

# KONFIGURASI SERVER
# Jika Flask ada di Raspberry Pi yang SAMA, gunakan 'http://127.0.0.1:5000'
# Jika Flask ada di Laptop (beda device), gunakan IP Laptop, misal 'http://192.168.1.5:5000'
URL_SERVER = 'http://127.0.0.1:5000/api/update-sensor'

def baca_sensor_dummy():
    """
    Fungsi simulasi sensor. 
    Nanti ganti bagian ini dengan library sensor asli (GPIO/Adafruit).
    """
    data = {
        'soil_moisture': random.randint(40, 90), # Simulasi kelembapan tanah
        'temperature': round(random.uniform(25.0, 33.0), 1), # Simulasi suhu
        'humidity': random.randint(50, 80) # Simulasi kelembapan udara
    }
    return data

def main():
    print(f"Mulai mengirim data ke {URL_SERVER}...")
    
    while True:
        # 1. Baca Data
        sensor_data = baca_sensor_dummy()
        
        # 2. Kirim ke Server Flask
        try:
            response = requests.post(URL_SERVER, json=sensor_data)
            
            if response.status_code == 200:
                print(f"[SUKSES] Data dikirim: {sensor_data}")
            else:
                print(f"[GAGAL] Server merespon: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("[ERROR] Tidak bisa konek ke server. Pastikan Flask sudah jalan.")
            
        # 3. Tunggu 2 detik sebelum kirim lagi
        time.sleep(2)

if __name__ == "__main__":
    main()