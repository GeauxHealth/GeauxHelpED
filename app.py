from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False)

class PatientProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    medical_info = db.Column(db.Text, nullable=False)
    additional_details = db.Column(db.Text, nullable=True)

class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity_description = db.Column(db.String(200), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient_profile.id'), nullable=False)
    caretaker_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(username=data['username'], email=data['email'], password=hashed_password, role=data['role'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        token = create_access_token(identity={'username': user.username, 'role': user.role})
        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/patient-profiles', methods=['POST'])
@jwt_required()
def create_patient_profile():
    current_user = get_jwt_identity()
    if current_user['role'] != 'caretaker':
        return jsonify({'message': 'Permission denied'}), 403

    data = request.get_json()
    patient_profile = PatientProfile(
        name=data['name'],
        date_of_birth=datetime.strptime(data['dateOfBirth'], '%Y-%m-%d').date(),
        medical_info=data['medicalInfo'],
        additional_details=data.get('additionalDetails')
    )
    db.session.add(patient_profile)
    db.session.commit()
    return jsonify({'message': 'Patient profile created successfully'}), 201

@app.route('/api/activity-logs', methods=['POST'])
@jwt_required()
def log_activity():
    data = request.get_json()
    activity_log = ActivityLog(
        activity_description=data['activityDescription'],
        patient_id=data['patientId'],
        caretaker_id=data['caretakerId']
    )
    db.session.add(activity_log)
    db.session.commit()
    return jsonify({'message': 'Activity log created successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)
