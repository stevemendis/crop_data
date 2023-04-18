from datetime import datetime, timedelta
import math,random
from werkzeug.security import generate_password_hash, check_password_hash
from crop_analysis.models.utils import rand_pass
from flask_login import UserMixin
from crop_analysis import db

# Harshita
class CropData(db.Model):
    crop_data_id = db.Column(db.Integer, primary_key=True)
    crop_id = db.Column(db.Integer, db.ForeignKey('crop.crop_id'), nullable=False)
    season_id = db.Column(db.Integer, db.ForeignKey('season.season_id'), nullable=False)
    district_id = db.Column(db.Integer, db.ForeignKey('district.district_id'), nullable=False)
    area = db.Column(db.Float, nullable=False)
    production = db.Column(db.Float, nullable=False)
    yield_data = db.Column(db.Float, nullable=False)
    profit = db.Column(db.Float, nullable=False)
    rainfall = db.Column(db.Float, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable = True)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    user_crop = db.relationship('UserCrop', backref='cropdata', lazy=True)

    def __str__(self):
        return 'CropData :{}'.format(self.crop_data_id)