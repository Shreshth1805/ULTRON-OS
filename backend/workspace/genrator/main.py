
# main.py

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///secure_student_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __init__(self, name, email):
        self.name = name
        self.email = email

class StudentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email')

student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

@app.route('/student', methods=['POST'])
def create_student():
    new_student = Student(name=request.json['name'], email=request.json['email'])
    db.session.add(new_student)
    db.session.commit()
    return student_schema.jsonify(new_student)

@app.route('/student', methods=['GET'])
@jwt_required
def get_students():
    all_students = Student.query.all()
    result = students_schema.dump(all_students)
    return jsonify(result)

@app.route('/student/<id>', methods=['GET'])
@jwt_required
def get_student(id):
    student = Student.query.get(id)
    if student is None:
        return jsonify({"msg": "Student not found"}), 404
    return student_schema.jsonify(student)

@app.route('/student/<id>', methods=['PUT'])
@jwt_required
def update_student(id):
    student = Student.query.get(id)
    if student is None:
        return jsonify({"msg": "Student not found"}), 404
    student.name = request.json['name']
    student.email = request.json['email']
    db.session.commit()
    return student_schema.jsonify(student)

@app.route('/student/<id>', methods=['DELETE'])
@jwt_required
def delete_student(id):
    student = Student.query.get(id)
    if student is None:
        return jsonify({"msg": "Student not found"}), 404
    db.session.delete(student)
    db.session.commit()
    return jsonify({"msg": "Student deleted"})

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not email or not password:
        return jsonify({"msg": "Bad email or password"}), 401

    student = Student.query.filter_by(email=email).first()
    if not student:
        return jsonify({"msg": "Bad email or password"}), 401

    access_token = create_access_token(identity=student.id)
    return jsonify(access_token=access_token)

if __name__ == '__main__':
    app.run(debug=True)
