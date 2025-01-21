#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    pass
def get(self):
        """GET /plants - Fetch all plants."""
        plants = Plant.query.all()
        return jsonify([plant.to_dict() for plant in plants])
def post(self):
        """POST /plants - Create a new plant."""
        data = request.get_json()
        if not data or not data.get('name') or not data.get('image') or not data.get('price'):
            return make_response(jsonify({"error": "Missing required fields"}), 400)
        if data['image'] is None or data['price'] is None:
            return make_response(jsonify({"error": "Image and price cannot be None"}), 400)
        
        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price']
        )
        db.session.add(new_plant)
        db.session.commit()
        return jsonify(new_plant.to_dict()), 201


class PlantByID(Resource):
    pass
def get(self, id):
        """GET /plants/<id> - Fetch a plant by ID."""
        plant = Plant.query.get_or_404(id)
        return jsonify(plant.to_dict())
def put(self, id):
        """PUT /plants/<id> - Update an existing plant."""
        data = request.get_json()
        if not data or not data.get('name') or not data.get('image') or not data.get('price'):
            return make_response(jsonify({"error": "Missing required fields"}), 400)
        plant = Plant.query.get(id)
        if not plant:
            return make_response(jsonify({"error": "Plant not found"}), 404)
        
        plant.name = data['name']
        plant.image = data['image']
        plant.price = data['price']
        
        db.session.commit()
    
        return jsonify(plant.to_dict())
def delete(self, id):
        """DELETE /plants/<id> - Delete a plant."""
        plant = Plant.query.get(id)
        if not plant:
            return make_response(jsonify({"error": "Plant not found"}), 404)
        
        db.session.delete(plant)
        db.session.commit()
        return jsonify({"message": "Plant deleted successfully"}), 200

api.add_resource(Plants, '/plants')  
api.add_resource(PlantByID, '/plants/<int:id>')  
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
