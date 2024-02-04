from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
    
        query_components = parse_qs(urlparse(self.path).query)

        if self.path.startswith("/lsb/code/text"):
             
            extrat = query_components.get("info", [])[0]
            # Faire quelque chose avec image_input_value, par exemple, l'imprimer côté serveur
            print("Image Input Value:", extrat)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes('{"message": "Success"}', "utf-8"))
        else:
            self.handle_not_found()

    def handle_home(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Home</title></head>", "utf-8"))
        self.wfile.write(bytes("<body><h1>Welcome to the Home Page</h1></body></html>", "utf-8"))

    def handle_about(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>About</title></head>", "utf-8"))
        self.wfile.write(bytes("<body><h1>About Us</h1></body></html>", "utf-8"))

    def handle_contact(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Contact</title></head>", "utf-8"))
        self.wfile.write(bytes("<body><h1>Contact Us</h1></body></html>", "utf-8"))

    def handle_not_found(self):
        self.send_response(404)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Not Found</title></head>", "utf-8"))
        self.wfile.write(bytes("<body><h1>404 - Not Found</h1></body></html>", "utf-8"))

if __name__ == "__main__":
    hostName = "localhost"
    serverPort = 8080
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
