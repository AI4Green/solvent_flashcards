#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The solvent_guide file of the app
"""
from flask import Flask

def create_app():

    app = Flask(__name__)  # creates the app object

    # Now we need to import the app modules as blueprints
    with app.app_context():
        from .blueprints.solvent_guide import solvent_guide_bp
        app.register_blueprint(solvent_guide_bp)

    return app
