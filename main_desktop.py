#!/usr/bin/env python
"""
ISBMS - Business Management System Desktop Software Wrapper
Launches embedded Django server and native Desktop App window.
"""
import os
import sys
import time
import socket
import threading
import webbrowser
from wsgiref.simple_server import make_server

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'isbms.settings')

def get_free_port():
    """Find a free port on localhost."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 0))
    port = s.getsockname()[1]
    s.close()
    return port

def run_django_server(host, port):
    """Run Django WSGI server in local background thread."""
    try:
        import django
        django.setup()

        from django.core.management import call_command
        print("[ISBMS Engine] Running database migrations...")
        call_command('migrate', interactive=False)

        from django.core.wsgi import get_wsgi_application
        application = get_wsgi_application()

        httpd = make_server(host, port, application)
        print(f"[ISBMS Engine] Desktop server running on http://{host}:{port}")
        httpd.serve_forever()
    except Exception as e:
        print(f"[ISBMS Engine Error] Server failure: {e}")

def wait_for_server(url, max_retries=40):
    """Poll local HTTP endpoint until Django WSGI server responds cleanly."""
    import urllib.request
    print(f"[ISBMS Desktop] Waiting for local server at {url}...")
    for _ in range(max_retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'ISBMS-Desktop'})
            with urllib.request.urlopen(req, timeout=1.5) as resp:
                if resp.status in (200, 302):
                    print("[ISBMS Desktop] Server ready & accepting connections!")
                    return True
        except Exception:
            time.sleep(0.25)
    return False

def main():
    host = '0.0.0.0'
    port = 8000
    
    # Try port 8000 first, fallback to free port if busy
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.close()
    except OSError:
        port = get_free_port()

    local_url = f"http://127.0.0.1:{port}"
    url = local_url
    print(f"==================================================")
    print(f"  ISBMS - Business Management System Software")
    print(f"  Local PC URL:       http://127.0.0.1:{port}")
    print(f"  Mobile / Wi-Fi URL: http://192.168.0.137:{port}")
    print(f"==================================================")

    # Start Django server in background daemon thread
    server_thread = threading.Thread(target=run_django_server, args=(host, port), daemon=True)
    server_thread.start()

    # Wait until Django server is fully booted up and serving HTTP requests
    server_ready = wait_for_server(url)
    if not server_ready:
        print("[ISBMS Desktop Warning] Server startup timed out. Retrying connection...")

    # Launch Browser Access Automatically to Guarantee Working UI
    def open_browser():
        time.sleep(0.8)
        webbrowser.open(url)

    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()

    # Launch PyWebView Native Desktop GUI
    use_pywebview = False
    try:
        import webview
        print("[ISBMS Desktop] Launching native window via PyWebView...")
        
        window = webview.create_window(
            title='ISBMS - Business Management System',
            url=url,
            width=1340,
            height=860,
            min_size=(900, 600),
            resizable=True
        )
        use_pywebview = True
        # Try MS Edge WebView2 first, fallback gracefully if locked (0x800700AA)
        webview.start(private_mode=False)
    except Exception as err:
        print(f"[ISBMS Desktop Warning] PyWebView window engine note ({err}). Active in system browser.")
        use_pywebview = False

    print("\n==================================================")
    print("  ISBMS Software is Active at: " + url)
    print("==================================================\n")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[ISBMS Desktop] Shutting down application...")

if __name__ == '__main__':
    main()
