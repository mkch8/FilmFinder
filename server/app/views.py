from flask import Blueprint, jsonify, request, current_app as app
from .models import Film, User
from . import db

main = Blueprint('main', __name__)

@main.route('/api/users', methods=['GET'])
def users():
    return jsonify(
        {
            "users": [
                'arpan',
                'zach',
                'michael'
            ]
        }
    )

# @main.route('/api/data', methods=['GET'])
# def get_data():
#     data = YourModel.query.all()
#     result = [item.to_dict() for item in data]
#     return jsonify(result)
#
# @main.route('/api/data', methods=['POST'])
# def add_data():
#     data = request.json
#     new_item = YourModel(
#         name=data['name'],
#         value=data['value']
#     )
#     db.session.add(new_item)
#     db.session.commit()
#     return jsonify(new_item.to_dict()), 201
