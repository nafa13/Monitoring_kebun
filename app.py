from flask import Flask, render_template, jsonify, request
import random
import time

app = Flask(__name__)

# Simpan status perangkat (Lampu, Pompa, Kipas) di memori server
device_status = {
    'pump': True,  # Default Nyala
    'light': False, # Default Mati
    'fan': False    # Default Mati
}

# Route Utama: Menampilkan Halaman Web
@app.route('/')
def index():
    return render_template('index.html')

# API: Mengambil Data Sensor (GET)
# Ini nanti dipanggil oleh Javascript setiap beberapa detik
@app.route('/api/sensors')
def get_sensors():
    # Di sini Anda bisa menghubungkan ke database atau membaca Serial Arduino
    # Kita gunakan angka random untuk simulasi
    sensor_data = {
        'soil_moisture': random.randint(50, 85),  # Kelembapan Tanah 50-85%
        'temperature': round(random.uniform(26.0, 32.0), 1), # Suhu 26-32 Celcius
        'humidity': random.randint(60, 90), # Kelembapan Udara 60-90%
        'devices': device_status # Kirim juga status tombol terakhir
    }
    return jsonify(sensor_data)

# API: Mengontrol Perangkat (POST)
# Menerima perintah dari tombol di website
@app.route('/api/control', methods=['POST'])
def control_device():
    data = request.json
    device = data.get('device') # nama alat: pump/light/fan
    state = data.get('state')   # status: true/false
    
    if device in device_status:
        device_status[device] = state
        print(f"Update: {device} sekarang {'ON' if state else 'OFF'}")
        return jsonify({'status': 'success', 'new_state': device_status})
    
    return jsonify({'status': 'error', 'message': 'Device not found'}), 400

if __name__ == '__main__':
    # debug=True agar server auto-reload saat coding
    app.run(debug=True, host='0.0.0.0', port=5000)