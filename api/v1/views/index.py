#!/usr/bin/python3
"""
Module docs
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def stat_return():
    """
    Function Docs
    """
    return jsonify({"status": "OK"})

if __name__ == "__main__":
    pass