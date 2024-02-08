# !/usr/bin/env python
# -*- coding: utf-8 -*-

from sources import create_app
from threading import Timer
import webbrowser
import os

app = create_app()

port = os.getenv("FLASK_RUN_PORT")

if not port:
    port = 5000


def open_browser():
    url = "http://127.0.0.1:" + str(port) + '/'

    webbrowser.open_new(url)


def app_run():

    Timer(1, open_browser).start()
    app.run(debug=False, use_reloader=False, host='0.0.0.0', port=port)


if __name__ == '__main__':
    app_run()
