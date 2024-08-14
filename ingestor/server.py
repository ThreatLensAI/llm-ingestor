from http.server import BaseHTTPRequestHandler

class HealthCheckHandler(BaseHTTPRequestHandler):
    """HTTP server that responds to health checks"""
    def do_GET(self):
        """Handle GET requests"""

        if self.path != '/healthz':
            self.send_response(404)
            self.end_headers()
        else:
            self.send_response(200)
            self.end_headers()

    def log_message(self, format, *args):
        pass
