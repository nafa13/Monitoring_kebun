from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import random
import time

app = Flask(__name__)

# --- KONFIGURASI LOGIN ---
app.secret_key = 'rahasia_kebun_saya'  # Kunci acak untuk mengamankan session
USERNAME_VALID = 'admin'               # Ganti username sesuai keinginan
PASSWORD_VALID = '12345'               # Ganti password sesuai keinginan

# Simpan status perangkat (Lampu, Pompa, Kipas) di memori server
#
device_status = {
    'pump': True,
    'light': False,
    'fan': False
}

# --- ROUTE LOGIN & LOGOUT ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Cek apakah username dan password cocok
        if username == USERNAME_VALID and password == PASSWORD_VALID:
            session['logged_in'] = True  # Tandai user sudah login
            return redirect(url_for('index')) # Arahkan ke dashboard
        else:
            error = 'Username atau Password salah!'
            
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None) # Hapus sesi login
    return redirect(url_for('login'))

# --- ROUTE UTAMA ---

@app.route('/')
def index():
    # Cek Keamanan: Jika belum login, tendang ke halaman login
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    return render_template('index.html')

# --- API SENSORS (Tetap sama) ---
@app.route('/api/sensors')
def get_sensors():
    # Proteksi tambahan (opsional): Hanya kirim data jika login
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401

    sensor_data = {
        'soil_moisture': random.randint(50, 85),
        'temperature': round(random.uniform(26.0, 32.0), 1),
        'humidity': random.randint(60, 90),
        'devices': device_status
    }
    return jsonify(sensor_data)

# --- API CONTROL (Tetap sama) ---
@app.route('/api/control', methods=['POST'])
def control_device():
    # Proteksi tambahan: Jangan izinkan kontrol jika belum login
    if not session.get('logged_in'):
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401

    data = request.json
    device = data.get('device')
    state = data.get('state')
    
    if device in device_status:
        device_status[device] = state
        print(f"Update: {device} sekarang {'ON' if state else 'OFF'}")
        return jsonify({'status': 'success', 'new_state': device_status})
    
    return jsonify({'status': 'error', 'message': 'Device not found'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)