from datetime import datetime, timedelta
import math,random
from werkzeug.security import generate_password_hash, check_password_hash
from crop_analysis.models.utils import rand_pass
from flask_login import UserMixin
from crop_analysis import db

# Harshita
class Crop(db.Model):
    crop_id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable = True)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)


    def __str__(self):
        return 'Crop :{}'.format(self.id)