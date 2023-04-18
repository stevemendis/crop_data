from crop_analysis import login_manager
from crop_analysis.models import User
# from tour_management.models import Admin
from base64 import b64encode
from base64 import b64decode
from flask import redirect, url_for, render_template, current_app
import json
import os
import re
import requests



@login_manager.user_loader
def load_user(user_id):
    x = User.query.get(user_id)
    return x