# !/usr/bin/env python
# -*- coding: utf-8 -*-

from sources import create_app
from threading import Timer
import webbrowser

app = create_app()


def open_browser():
    webbrowser.open_new("http://127.0.0.1/")


def app_run():
    if __name__ == '__main__':
        Timer(1, open_browser).start()
        app.run(debug=False, use_reloader=False, host='0.0.0.0', port='80')


app_run()
