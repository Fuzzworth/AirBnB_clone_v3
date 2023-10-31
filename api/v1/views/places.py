#!/usr/bin/python3
"""
Module Docs
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def all_places(city_id):
    """
    Function Docs
    """
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    place_list = []
    for place in city.places:
        place_list.append(place.to_dict())
    return jsonify(place_list)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """
    Function Docs
    """
    try:
        place = storage.get('Place', place_id)
        return jsonify(place.to_dict())
    except Exception:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Function Docs
    """
    try:
        place = storage.get('Place', place_id)
        storage.delete(place)
        return jsonify({}), 200
    except Exception:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """
    Function Docs
    """
    city = storage.get('City', city_id)
    if not city:
        abort(404)

    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in request.json:
        return jsonify({"error": "Missing user_id"}), 400

    user = storage.get('User', request.json()['user_id'])
    if not user:
        abort(404)
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400

    new_place = Place(**request.json())
    new_place.city_id = city_id
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """
    Function Docs
    """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200