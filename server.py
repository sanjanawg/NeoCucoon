import serial
from http.server import BaseHTTPRequestHandler, HTTPServer

# Initialize the serial port (adjust '/dev/ttyACM0' if needed)
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Serve the HTML when the root URL is accessed
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(index_html(), 'utf-8'))

        # Serve sensor data to /data endpoint
        elif self.path == '/data':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            data = read_from_uart()
            self.wfile.write(bytes(data, 'utf-8'))

# Function to read data from UART
def read_from_uart():
    try:
        data = ser.readline().decode('utf-8').rstrip()  # Read and decode UART data
        if data:
            return f"{data}\n"  # Return sensor data
        else:
            return "No data available\n"
    except serial.SerialException as e:
        return f"Error reading from UART: {e}\n"

# HTML with CSS for the grid layout
def index_html():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sensor Data Display</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #000;  /* Black background */
                color: #00FF00;  /* Green font for vital readings */
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                width: 90%;
                max-width: 1200px;
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 20px;
                padding: 20px;
            }
            .sensor-block {
                background-color: #333;  /* Dark gray card background */
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.7);
            }
            .sensor-block div {
                margin-bottom: 10px;
                font-size: 1.5em;
            }
            .value {
                font-size: 4em;  /* Large font for vitals */
                font-weight: bold;
            }
            .error {
                color: red;
                font-size: 2em;
                margin-bottom: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="sensor-block">
                <div>Temperature</div>
                <div class="value" id="temperature">Loading...</div>
            </div>
            <div class="sensor-block">
                <div>Heart Rate</div>
                <div class="value" id="heartrate">Loading...</div>
            </div>
            <div class="sensor-block">
                <div>Light Intensity</div>
                <div class="value" id="light">Loading...</div>
            </div>
        </div>
        
        <script>
            async function fetchData() {
                const response = await fetch('/data');
                const data = await response.text();
                
                // Assuming data is in format: temperature,heartrate,light
                const sensorData = data.split(",");
                if (sensorData.length >= 3) {
                    document.getElementById('temperature').textContent = sensorData[0] + ' °C';
                    document.getElementById('heartrate').textContent = sensorData[1] + ' bpm';
                    document.getElementById('light').textContent = sensorData[2] + ' lux';
                } else {
                    document.getElementById('temperature').textContent = "Error";
                    document.getElementById('heartrate').textContent = "Error";
                    document.getElementById('light').textContent = "Error";
                }
            }

            // Fetch data every second
            setInterval(fetchData, 1000);
        </script>
    </body>
    </html>
    """

# Run the HTTP server
def run(server_class=HTTPServer, handler_class=MyHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Serving on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()

# Close the serial port when the program exits
import atexit
atexit.register(ser.close)
