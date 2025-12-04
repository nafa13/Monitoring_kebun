from flask import Flask, render_template, jsonify, request, session, redirect, url_for
# random tidak lagi dibutuhkan untuk sensor, tapi boleh dibiarkan jika ingin test tanpa alat
import time

app = Flask(__name__)

# --- KONFIGURASI LOGIN ---
app.secret_key = 'rahasia_kebun_saya'
USERNAME_VALID = 'admin'
PASSWORD_VALID = '12345'

# --- VARIABEL GLOBAL ---

# 1. Simpan status perangkat (Kontrol dari Web)
device_status = {
    'pump': True,
    'light': False,
    'fan': False
}

# 2. Simpan data sensor TERAKHIR (Dikirim dari Raspberry Pi)
# Default 0 agar tidak error saat pertama kali jalan
current_sensor_values = {
    'soil_moisture': 0,
    'temperature': 0.0,
    'humidity': 0
}

# --- ROUTE LOGIN & LOGOUT ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == USERNAME_VALID and password == PASSWORD_VALID:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            error = 'Username atau Password salah!'
            
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

# --- ROUTE UTAMA ---

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html')

# --- API UPDATE SENSOR (BARU: Menerima data dari Raspberry Pi) ---
@app.route('/api/update-sensor', methods=['POST'])
def update_sensor():
    global current_sensor_values
    data = request.json
    
    if not data:
        return jsonify({'status': 'error', 'message': 'No data received'}), 400

    # Update variabel global dengan data baru
    if 'soil_moisture' in data:
        current_sensor_values['soil_moisture'] = data['soil_moisture']
    if 'temperature' in data:
        current_sensor_values['temperature'] = data['temperature']
    if 'humidity' in data:
        current_sensor_values['humidity'] = data['humidity']
        
    print(f"Data Masuk: {current_sensor_values}")
    return jsonify({'status': 'success'})

# --- API SENSORS (GET: Kirim data ke Web Dashboard) ---
@app.route('/api/sensors')
def get_sensors():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401

    # Gabungkan data sensor asli dengan status perangkat
    response_data = current_sensor_values.copy()
    response_data['devices'] = device_status
    
    return jsonify(response_data)

# --- API CONTROL (POST: Terima perintah dari Web) ---
@app.route('/api/control', methods=['POST'])
def control_device():
    if not session.get('logged_in'):
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401

    data = request.json
    device = data.get('device')
    state = data.get('state')
    
    if device in device_status:
        device_status[device] = state
        print(f"Update Switch: {device} -> {'ON' if state else 'OFF'}")
        return jsonify({'status': 'success', 'new_state': device_status})
    
    return jsonify({'status': 'error', 'message': 'Device not found'}), 400

if __name__ == '__main__':
    # Host 0.0.0.0 agar bisa diakses dari perangkat lain (Raspberry Pi/HP)
    app.run(debug=True, host='0.0.0.0', port=5000)