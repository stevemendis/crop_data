from datetime import datetime, timedelta
import math,random
from werkzeug.security import generate_password_hash, check_password_hash
from crop_analysis.models.utils import rand_pass
from flask_login import UserMixin
from crop_analysis import db

# Harshita
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone_number = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email_verified = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=False, nullable=False)
    # db.DateTime change dob
    dob = db.Column(db.String(255), nullable=False)
    sex = db.Column(db.String(255), nullable=False)
    sm_code = db.Column(db.String(255), unique= True, nullable=True)
    valid_sm_sec = db.Column(db.Integer, nullable=True)
    valid_sm_code = db.Column(db.Boolean, default=False, nullable=False)
    sm_code_sent_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)
    tokens = db.relationship('UserToken', backref='user', lazy=True)
    user_crop = db.relationship('UserCrop', backref='user', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # -- Backrefrences for other tables
    # property_id = db.relationship('Property',backref='user',lazy=True)
    # tenant_id = db.relationship('Tenant',backref='user',lazy=True)
    # support_id = db.relationship('Supportquery',backref='user',lazy=True)
    
    def __str__(self):
        return 'User: {}'.format(self.username)


    # Create a hash of password
    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)


    # Check if password entered is same as hash of password
    def check_password(self, password):
        return check_password_hash(self.password, password)

    # Generate OTP
    # Need to connect with twilio for sending sms
    #     message = client.messages.create(
    # body='Hi there',
    # from_='+14632637937',
    # to='+18127784955'
    # )

    # print(message.sid)
    @staticmethod
    def generate_smcode(user_id, valid_sm_sec):
        OTP = rand_pass(9)                              # Generate password using rand_pass
        while User.query.filter_by(sm_code=OTP).first():
            OTP = rand_pass(9)                          #Incase OTP been generated before, create new one    
        user_token = User.query.filter_by(id=user_id).first()
        print ('OTP :', OTP)
        user_token.sm_code = OTP
        print (datetime.utcnow)
        user_token.valid_sm_sec = valid_sm_sec
        db.session.commit()
        return OTP

    # Check validity of password
    def is_valid(self):
        valid_till = self.sm_code_sent_at + timedelta(seconds=self.valid_sm_sec)
        return valid_till > datetime.utcnow()
