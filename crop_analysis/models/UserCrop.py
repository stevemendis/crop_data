from datetime import datetime, timedelta
import math,random
from werkzeug.security import generate_password_hash, check_password_hash
from crop_analysis.models.utils import rand_pass
from flask_login import UserMixin
from crop_analysis import db



class UserCrop(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cropdata_id = db.Column(db.Integer, db.ForeignKey('crop_data.crop_data_id'))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __str__(self):
        return 'UserCrop :{}'.format(self.user_id)