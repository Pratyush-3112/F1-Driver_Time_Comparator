from flask import Flask, jsonify, send_from_directory
import fastf1
import numpy as np
import os

fastf1.Cache.enable_cache('cache')

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/lap')
def lap_data():
    session = fastf1.get_session(2026, 'Japan', 'R')
    session.load(telemetry=True, weather=False, messages=False)

    laps = session.laps
    lap_NOR = laps.pick_drivers('NOR').pick_fastest()
    lap_PIA = laps.pick_drivers('PIA').pick_fastest()

    def extract(lap, name):
        tel = lap.get_telemetry()
        x = tel['X'].values.tolist()
        y = tel['Y'].values.tolist()
        speed = tel['Speed'].values.tolist()
        throttle = tel['Throttle'].values.tolist()
        brake = tel['Brake'].values.tolist()
        return {
            'name': name,
            'x': x,
            'y': y,
            'speed': speed,
            'throttle': throttle,
            'brake': brake,
            'laptime': str(lap['LapTime']),
        }

    data = {
        'drivers': [
            extract(lap_NOR, 'NOR'),
            extract(lap_PIA, 'PIA'),
        ]
    }
    return jsonify(data)

if __name__ == '__main__':
    os.makedirs('static', exist_ok=True)
    app.run(debug=True, port=5065)
