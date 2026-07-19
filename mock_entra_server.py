from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, urlencode, parse_qsl
import json


AUTH_CODE = "mock-auth-code-123"


class MockEntraHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        
        if parsed_url.path == "/":

            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Mock Customer Portal</title>
                <style>
                    body{
                        font-family:Arial;
                        background:#f5f5f5;
                        display:flex;
                        justify-content:center;
                        align-items:center;
                        height:100vh;
                    }

                    .card{
                        background:white;
                        padding:40px;
                        border-radius:10px;
                        box-shadow:0 2px 10px rgba(0,0,0,.15);
                        text-align:center;
                        width:420px;
                    }

                    button{
                        background:#0078D4;
                        color:white;
                        border:none;
                        padding:12px 24px;
                        border-radius:5px;
                        cursor:pointer;
                        font-size:16px;
                    }

                    button:hover{
                        background:#106ebe;
                    }
                </style>
            </head>

            <body>

                <div class="card">

                    <h2>Contoso Bank</h2>

                    <p>
                        Welcome to the Mock Customer Portal.
                    </p>

                    <p>
                        Click below to access CapeArk.
                    </p>

                    <button
                        onclick="window.location='http://localhost:8000/api/auth/entra/start/'">

                        Login to CapeArk

                    </button>

                </div>

            </body>

            </html>
            """

            self.send_html(html)
            return

        if parsed_url.path == "/authorize":
            query = parse_qs(parsed_url.query)
            redirect_uri = query.get("redirect_uri", [""])[0]
            state = query.get("state", [""])[0]

            params = {
                "code": AUTH_CODE,
                "state": state,
            }

            callback_url = redirect_uri + "?" + urlencode(params)

            self.send_response(302)
            self.send_header("Location", callback_url)
            self.end_headers()
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        parsed_url = urlparse(self.path)

        if parsed_url.path == "/auth/token":
            response = {
                "id_token": {
                    "email": "azureuser@example.com",
                    "name": "Azure Test User",
                    "oid": "mock-entra-object-id-001",
                    "tid": "mock-tenant-id-001",
                },
                "access_token": "mock-access-token",
                "token_type": "Bearer",
                "expires_in": 3600,
            }

            body = json.dumps(response).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        self.send_response(404)
        self.end_headers()

    def send_html(self, html):
        body = html.encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()

        self.wfile.write(body)

if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 9000), MockEntraHandler)
    print("Mock Entra server running on http://localhost:9000")
    server.serve_forever()