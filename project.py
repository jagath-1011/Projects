import http.server
import socketserver
import urllib.parse
from phonenumbers import geocoder, carrier, parse, phonenumberutil

PORT = 8000


class PhoneHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        phone_number = params.get("number", [None])[0]

        if phone_number:
            try:
                
                parsed_number = parse(phone_number, None)
                location = geocoder.description_for_number(parsed_number, "en")
                service_number = parse(phone_number, None)
                carrier_name = carrier.name_for_number(service_number, "en")

                
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(f"""
                    <html>
                        <head>
                            <style>
                                body {{
                                    font-family: Arial, sans-serif;
                                    background: linear-gradient(to right, #6a11cb, #2575fc);
                                    color: #fff;
                                    margin: 0;
                                    padding: 0;
                                }}
                                h1 {{
                                    text-align: center;
                                    padding: 20px 0;
                                }}
                                .container {{
                                    text-align: center;
                                    margin: 20px auto;
                                    max-width: 600px;
                                    padding: 20px;
                                    border-radius: 10px;
                                    background: rgba(255, 255, 255, 0.9);
                                    color: #333;
                                    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                                }}
                                a {{
                                    text-decoration: none;
                                    color: #ff9800;
                                }}
                            </style>
                        </head>
                        <body>
                            <h1>Phone Number Information</h1>
                            <div class="container">
                                <p><strong>Phone Number:</strong> {phone_number}</p>
                                <p><strong>Location:</strong> {location}</p>
                                <p><strong>Carrier:</strong> {carrier_name}</p>
                                <a href="/">Back</a>
                            </div>
                        </body>
                    </html>
                """.encode("utf-8"))
            except phonenumberutil.NumberParseException:
                
                self.send_response(400)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write("""
                    <html>
                        <head>
                            <style>
                                body {{
                                    font-family: Arial, sans-serif;
                                    background: linear-gradient(to right, #FF5252, #FF1744);
                                    color: #fff;
                                    margin: 0;
                                    padding: 0;
                                }}
                                h1 {{
                                    text-align: center;
                                    padding: 20px 0;
                                }}
                                .container {{
                                    text-align: center;
                                    margin: 20px auto;
                                    max-width: 500px;
                                    padding: 20px;
                                    border-radius: 10px;
                                    background: rgba(255, 255, 255, 0.9);
                                    color: #333;
                                    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                                }}
                                a {{
                                    text-decoration: none;
                                    color: #FFD740;
                                }}
                            </style>
                        </head>
                        <body>
                            <h1>Error</h1>
                            <div class="container">
                                <p>Invalid phone number. Please try again.</p>
                                <a href="/">Back</a>
                            </div>
                        </body>
                    </html>
                """.encode("utf-8"))
        else:
           
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write("""
                <html>
                    <head>
                        <style>
                            /* Body styling with gradient */
                            body {{
                                font-family: 'Arial', sans-serif;
                                background: linear-gradient(to right, #FF6AB2, #FF80B5);
                                margin: 0;
                                padding: 0;
                            }}
                            h1 {{
                                text-align: center;
                                padding: 20px 0;
                                color: white;
                            }}
                            /* Centered login container */
                            .login-container {{
                                max-width: 400px;
                                margin: 50px auto;
                                padding: 30px;
                                border-radius: 15px;
                                background: #fff;
                                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
                                text-align: center;
                            }}
                            /* Input field */
                            input[type="text"] {{
                                padding: 10px;
                                border: 2px solid #FF9800;
                                border-radius: 5px;
                                font-size: 16px;
                                width: 100%;
                                margin: 10px 0;
                            }}
                            /* Submit button */
                            button {{
                                background-color: #FF9800;
                                color: #fff;
                                border: none;
                                padding: 10px 20px;
                                cursor: pointer;
                                border-radius: 5px;
                                transition: background-color 0.3s ease;
                            }}
                            button:hover {{
                                background-color: #FFA733;
                            }}
                        </style>
                    </head>
                    <body>
                        <h1>Login - Search Phone Information</h1>
                        <div class="login-container">
                            <form method="get">
                                <input type="text" name="number" placeholder="+1234567890" required>
                                <br>
                                <button type="submit">Search Phone Info</button>
                            </form>
                        </div>
                    </body>
                </html>
            """.encode("utf-8"))



with socketserver.TCPServer(("", PORT), PhoneHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
# http://localhost:8000