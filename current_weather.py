import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler, HTTPServer

# webserver source: https://pythonbasics.org/webserver/
class WeatherServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>Current Weather</title></head>", "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("<p>A weather file must be specified.</p>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))
        if self.path.endswith('.TXT'):
            split_path = self.path.split('/')
            weather_file = split_path[len(split_path) - 1]
            temp_and_pressure_list = find_temp_and_pressure(weather_file)

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>Current Weather</title></head>", "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            if len(temp_and_pressure_list) == 0:
                self.wfile.write(bytes("<p>No Temperature or Pressure found for %s.</p>" % weather_file, "utf-8"))
            else:
                self.wfile.write(bytes("<p>Current weather for %s.</p>" % weather_file, "utf-8"))
                for temp_or_pressure in temp_and_pressure_list:
                    self.wfile.write(bytes("<p>%s</p>" % temp_or_pressure, "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))


def find_temp_and_pressure(weather_file: str):
    weather_url = 'https://tgftp.nws.noaa.gov/data/observations/metar/decoded/' + weather_file
    try:
        weather_report = urllib.request.urlopen(weather_url).read().decode('utf-8')
        weather_info = weather_report.splitlines()
        return [temp_or_pressure for temp_or_pressure in weather_info
                if temp_or_pressure.startswith("Temperature")
                or temp_or_pressure.startswith("Pressure")]
    except urllib.error.HTTPError as e:
        print("Failed to retrieve weather file %s.\n%s" % (weather_file, str(e)))
        return []


if __name__ == '__main__':
    webServer = HTTPServer(('localhost', 8080), WeatherServer)
    print("Server started http://%s:%s" % ('localhost', 8080))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
