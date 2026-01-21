import threading
import webview
from app import app, socketio

def run_flask():
    socketio.run(app, port=5000, debug=False, use_reloader=False)

if __name__=='__main__':
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()
    webview.create_window()