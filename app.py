from flask import Flask, render_template, request, jsonify
import math
import time
import csv
import io

app = Flask(__name__)
START_TIME = time.time()

G = 6.67430e-11
g = 9.80665

def numbers(data, *keys):
    vals = [float(data[k]) for k in keys]
    if not all(math.isfinite(x) for x in vals):
        raise ValueError("Invalid number")
    return vals

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/status")
def status():
    return jsonify({
        "name": "PHYSICS LAB ULTIMATE",
        "status": "ONLINE",
        "version": "FINAL EDITION",
        "uptime": int(time.time() - START_TIME)
    })

@app.route("/api/projectile", methods=["POST"])
def projectile():
    try:
        d = request.get_json()
        v, angle, gravity = numbers(d, "velocity", "angle", "gravity")
        if v < 0 or not 0 <= angle <= 90 or gravity <= 0:
            raise ValueError()
        rad = math.radians(angle)
        vx, vy = v*math.cos(rad), v*math.sin(rad)
        t = 2*vy/gravity
        return jsonify({
            "time": round(t, 4),
            "height": round(vy**2/(2*gravity), 4),
            "range": round(vx*t, 4)
        })
    except (ValueError, TypeError, KeyError):
        return jsonify({"error": "Check your inputs"}), 400

@app.route("/api/mechanics", methods=["POST"])
def mechanics():
    try:
        d = request.get_json()
        u, a, t, mass = numbers(d, "u", "a", "t", "mass")
        if t < 0 or mass <= 0:
            raise ValueError()
        v = u+a*t
        s = u*t+0.5*a*t*t
        return jsonify({
            "final_velocity": round(v, 4),
            "displacement": round(s, 4),
            "momentum": round(mass*v, 4),
            "kinetic_energy": round(0.5*mass*v*v, 4)
        })
    except (ValueError, TypeError, KeyError):
        return jsonify({"error": "Check your inputs"}), 400

@app.route("/api/ohm", methods=["POST"])
def ohm():
    try:
        d = request.get_json()
        v, r = numbers(d, "voltage", "resistance")
        if r <= 0:
            raise ValueError()
        i = v/r
        return jsonify({
            "current": round(i, 4),
            "power": round(v*i, 4),
            "resistance": r
        })
    except (ValueError, TypeError, KeyError):
        return jsonify({"error": "Resistance must be positive"}), 400

@app.route("/api/optics", methods=["POST"])
def optics():
    try:
        d = request.get_json()
        u, f = numbers(d, "u", "f")
        if u == 0 or f == 0 or f == u:
            raise ValueError()
        v = 1/(1/f+1/u)
        return jsonify({
            "image_distance": round(v, 4),
            "magnification": round(v/u, 4)
        })
    except (ValueError, TypeError, KeyError, ZeroDivisionError):
        return jsonify({"error": "Invalid distances"}), 400

@app.route("/api/waves", methods=["POST"])
def waves():
    try:
        d = request.get_json()
        f, wavelength = numbers(d, "frequency", "wavelength")
        if f < 0 or wavelength < 0:
            raise ValueError()
        return jsonify({
            "speed": round(f*wavelength, 4),
            "period": round(1/f, 4) if f else None
        })
    except (ValueError, TypeError, KeyError):
        return jsonify({"error": "Invalid wave values"}), 400

@app.route("/api/astronomy", methods=["POST"])
def astronomy():
    try:
        d = request.get_json()
        mass, radius = numbers(d, "mass", "radius")
        if mass <= 0 or radius <= 0:
            raise ValueError()
        escape = math.sqrt(2*G*mass/radius)
        orbital = math.sqrt(G*mass/radius)
        return jsonify({
            "escape_velocity": round(escape, 3),
            "orbital_velocity": round(orbital, 3),
            "surface_gravity": round(G*mass/radius**2, 4)
        })
    except (ValueError, TypeError, KeyError):
        return jsonify({"error": "Mass and radius must be positive"}), 400

@app.route("/api/thermo", methods=["POST"])
def thermo():
    try:
        d = request.get_json()
        m, c, change = numbers(d, "mass", "specific_heat", "temperature_change")
        if m < 0 or c < 0:
            raise ValueError()
        return jsonify({"heat": round(m*c*change, 4)})
    except (ValueError, TypeError, KeyError):
        return jsonify({"error": "Invalid values"}), 400

@app.route("/api/constants")
def constants():
    return jsonify({
        "Speed of light": "299792458 m/s",
        "Gravitational constant": "6.67430 × 10⁻¹¹ N m²/kg²",
        "Planck constant": "6.62607015 × 10⁻³⁴ J s",
        "Electron charge": "1.602176634 × 10⁻¹⁹ C",
        "Avogadro constant": "6.02214076 × 10²³ mol⁻¹",
        "Standard gravity": "9.80665 m/s²",
        "Boltzmann constant": "1.380649 × 10⁻²³ J/K"
    })

@app.route("/api/csv", methods=["POST"])
def csv_export():
    try:
        d = request.get_json()
        rows = d.get("rows", [])
        if not isinstance(rows, list) or len(rows) > 500:
            raise ValueError()
        output = io.StringIO()
        writer = csv.writer(output)
        for row in rows:
            if not isinstance(row, list) or len(row) > 20:
                raise ValueError()
            writer.writerow([str(x)[:200] for x in row])
        return jsonify({"csv": output.getvalue()})
    except (ValueError, TypeError, AttributeError):
        return jsonify({"error": "Invalid table"}), 400

@app.route("/api/health")
def health():
    return jsonify({"status": "OK"})

if __name__ == "__main__":
    print("PHYSICS LAB ULTIMATE FINAL EDITION")
    app.run(host="127.0.0.1", port=8767, debug=False)
