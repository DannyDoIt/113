from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    is_online = db.Column(db.Boolean, default=False)
    hobbies = db.Column(db.String(100))

with app.app_context():
    db.create_all()

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(first_name=data['first_name'], last_name=data['last_name'], hobbies=data.get('hobbies', ''))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User added!"}), 201

@app.route('/update_user/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User not found!"}), 404
    user.last_name = data['last_name']
    user.is_online = data['is_online']
    db.session.commit()
    return jsonify({"message": "User updated!"})

@app.route('/delete_user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User not found!"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted!"})

@app.route('/online_users', methods=['GET'])
def online_users():
    users = User.query.filter_by(is_online=True).all()
    return jsonify([{"id": user.id, "first_name": user.first_name, "last_name": user.last_name, "hobbies": user.hobbies} for user in users])

if __name__ == '__main__':
    app.run(debug=True)
