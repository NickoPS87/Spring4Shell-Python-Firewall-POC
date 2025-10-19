# www.theforage.com - Telstra Cyber Task 3
# Firewall Server Handler

from http.server import BaseHTTPRequestHandler, HTTPServer

host = "localhost"
port = 8000

#########
# Handle the response here 
def block_request(self ):
    # Send a 403 Forbidden response to block the malicious request
    self.send_response(403)
    self.send_header("content-type", "application/json")
    self.end_headers()
    # Log the block action to the console for monitoring
    print("[-] Request blocked: Malicious pattern detected.")

def handle_request(self):
    # Send a 200 OK response for legitimate requests
    self.send_response(200)
    self.send_header("content-type", "application/json")
    self.end_headers()
    print("[+] Request handled successfully.")

#########

class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # For this exercise, we assume GET requests are safe and handle them.
        handle_request(self)

    def do_POST(self):
        # 1. Get the size of the request body from the headers
        content_length = int(self.headers['Content-Length'])
        
        # 2. Read the raw request body
        post_data = self.rfile.read(content_length)
        
        # 3. Decode the body into a string for inspection
        post_data_str = post_data.decode('utf-8')
        
        # 4. FIREWALL RULE:
        # If the malicious signature is found in the request body,
        # block the request. Otherwise, handle it normally.
        if "class.module.classLoader" in post_data_str:
            block_request(self)
        else:
            handle_request(self)

if __name__ == "__main__":        
    server = HTTPServer((host, port), ServerHandler)
    print("[+] Firewall Server")
    print("[+] HTTP Web Server running on: %s:%s" % (host, port))

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()
    print("[-] Server terminated. Exiting...")
    exit(0)
