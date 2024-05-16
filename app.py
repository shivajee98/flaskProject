from flask import Flask, render_template
import serial
import time

app = Flask(__name__)

# Configure the possible serial ports
serial_ports = ['/dev/ttyACM0', '/dev/ttyACM1']  # Add more if needed
baud_rate = 115200

# Function to establish serial connection with Arduino
def establish_serial_connection():
    for port in serial_ports:
        try:
            ser = serial.Serial(port, baud_rate, timeout=1)
            if ser.is_open:
                print(f"Serial connection established with Arduino on {port}")
                return ser
        except serial.SerialException:
            print(f"Failed to connect to {port}. Trying next port...")

    # If no port is successfully connected
    print("Failed to connect to any serial port.")
    return None

# Establish serial connection
ser = establish_serial_connection()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_command/<direction>')
def send_command(direction):
    if direction in ['F', 'B', 'L', 'R', 'A', '1', '2', '3', '4', 'S']:
        if ser:
            ser.write(direction.encode())
            return f'Sent command: {direction}'
        else:
            return 'Failed to send command. Arduino not connected.'
    else:
        return 'Invalid action'

@app.route('/start_radar')
def start_radar():
    # Add code here to run the radar functionality
    return 'Radar started successfully'

if __name__ == '__main__':
    if ser:
        app.run(host='0.0.0.0', port=80)
    else:
        print("Exiting Flask application. Arduino not connected.")
