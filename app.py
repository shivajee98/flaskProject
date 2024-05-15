from flask import Flask, render_template
import serial
import time

app = Flask(__name__)

# Configure the serial port
serial_port = '/dev/ttyACM1'  # Update with the correct serial port of your Arduino
baud_rate = 115200


# Function to establish serial connection with Arduino
def establish_serial_connection():
    while True:
        try:
            ser = serial.Serial(serial_port, baud_rate, timeout=1)
            if ser.is_open:
                print("Serial connection established with Arduino")
                return ser
        except serial.SerialException:
            print(f"Failed to connect to {serial_port}. Retrying in 5 seconds...")
            time.sleep(5)


# Establish serial connection
ser = establish_serial_connection()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send_command/<direction>')
def send_command(direction):
    if direction in ['F', 'B', 'L', 'R', 'A', '1', '2', '3', '4', 'S']:
        ser.write(direction.encode())
        return f'Sent command: {direction}'
    else:
        return 'Invalid action'


@app.route('/start_radar')
def start_radar():
    # Add code here to run the radar functionality
    return 'Radar started successfully'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)


