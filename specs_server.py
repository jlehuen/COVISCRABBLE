#!/usr/bin/env python3
#coding:utf-8
"""
specs_server.py - Serveur web local embarqué pour le tableau de bord OpenSpec.
Permet de visualiser les spécifications vivantes et cycles d'évolution en temps réel sur http://localhost:8088/specs
"""

import sys
import os
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, 'openspec'))
from render_html import generate_html

PORT = 8088

class SpecsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ('/', '/specs', '/specs.html'):
            try:
                content = generate_html(BASE_DIR).encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write(f"Error generating specs: {e}".encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def log_message(self, format, *args):
        # Silence normal HTTP access logs for clean console
        pass

def run():
    port = PORT
    for i, arg in enumerate(sys.argv):
        if arg == '-port' and i + 1 < len(sys.argv):
            port = int(sys.argv[i+1])
    
    server_address = ('', port)
    httpd = HTTPServer(server_address, SpecsHandler)
    url = f"http://localhost:{port}/specs"
    print(f"[OpenSpec] Dashboard disponible sur : {url}")
    print("[OpenSpec] Appuyez sur Ctrl+C pour arrêter le serveur.")
    
    if '-open' in sys.argv or '--open' in sys.argv:
        webbrowser.open(url)
        
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[OpenSpec] Arrêt du serveur.")
        httpd.server_close()

if __name__ == '__main__':
    run()
