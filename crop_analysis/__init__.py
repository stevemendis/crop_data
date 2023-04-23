from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from crop_analysis.config import DevelopmentConfig
from flask_jwt_extended import JWTManager
from twilio.rest import Client
import csv
import os
from flask_cors import CORS


print(os.getcwd())
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
jwt = JWTManager()
cors = CORS()
login_manager = LoginManager()
login_manager.login_message = 'Please login to continue'
login_manager.login_view = 'user.login'
login_manager.login_message_category = 'info'
# limiter = Limiter(key_func=get_remote_address)

def create_app(config=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config)
    jwt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.session_protection = "strong"
    mail.init_app(app)
    cors.init_app(app, resources={r"/*": {"origins": "*"}})
    from crop_analysis.models.Crop import Crop
    from crop_analysis.models.CropData import CropData
    from crop_analysis.models.District import District
    from crop_analysis.models.Season import Season
    from crop_analysis.models.State import State
    from crop_analysis.models.User import User
    from crop_analysis.models.UserToken import UserToken
    from crop_analysis.models.UserCrop import UserCrop
    from crop_analysis.auth import utils
    from crop_analysis.auth.blocklist import BLOCKLIST
    from crop_analysis.main.routes import main
    # from iot_security.api.routes import api
    from crop_analysis.user.routes import user
    app.register_blueprint(user,url_prefix='/api/user')
    # app.register_error_handler(404, handle_error_404)
    # app.register_error_handler(500, handle_error_500)
    # app.register_error_handler(429, handle_error_429)
    # app.register_blueprint(user)
    # login_manager.blueprint_login_views = {
    #     'admin' : '/admin/login',
    #     'user' : '/user/login'
    # }
    app.register_blueprint(main)
    # app.register_blueprint(admin,url_prefix='/admin')
    # app.register_blueprint(user,url_prefix='/user')
    
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST


    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )


    # Meghana - Create Table and Insert
    with app.app_context():
        db.create_all()
        db.session.commit()
        
    # Steve & Meghana
    
        
        # with open('finaldata.csv') as csv_file:
        #     csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        #     next(csv_reader) # Skip first row
        #     for row in csv_reader:
        #         try:
        #             state = State.query.filter_by(state_name=row[0]).first()
        #             if not state:
        #                 state = State(state_name=row[0])
        #                 db.session.add(state)
        #                 db.session.commit()
        #             crop = Crop.query.filter_by(crop_name=row[1]).first()
        #             if not crop:
        #                 crop = Crop(crop_name=row[1])
        #                 db.session.add(crop)
        #                 db.session.commit()
        #             season = Season.query.filter_by(season_name=row[2]).first()
        #             if not season:
        #                 season = Season(season_name=row[2])
        #                 db.session.add(season)
        #                 db.session.commit()
        #             district = District.query.filter_by(district_name=row[3]).first()
        #             if not district:
        #                 district = District(district_name=row[3], state_id=state.state_id)
        #                 db.session.add(district)
        #                 db.session.commit()
        #             crop_data = CropData(crop_id=crop.crop_id, season_id=season.season_id, district_id=district.district_id, area=row[4], production=row[5], yield_data=row[6], profit=row[7], rainfall=row[8], year=row[9])
        #             db.session.add(crop_data)
        #             db.session.commit()
        #         except Exception as e:
        #             print(f"Failed to insert row {row}: {str(e)}")
        #             db.session.rollback()
        #return True
        # with open('finaldata.csv') as file:
            
        #     for line in file:
        #         print(line)
        #         state_name, crop_name, season_name, district_name, area, production, yield_, profit, rainfall, year = line.strip().split(',')
        #         if state_name == "State":
        #             print("HEY ADS D")
        #             continue
        #         if state_name is None and crop_name is None and season_name is None and district_name is None and area is None and production is None and yield_ is None:
        #             continue
        #         # print("State : ",state_name,"Crop : " ,crop_name,"Season Name : " ,season_name,"District Name : " ,district_name,"Area : " ,area, "Production : " ,production,"Yeild : " ,yield_,"Profit : " ,profit, "Rainfall : " ,rainfall, "Year : " ,year)
        #         state = State.query.filter_by(state_name=state_name).first()
        #         if not state:
        #             state = State(state_name=state_name)
        #             db.session.add(state)
        #             db.session.commit()
        #         crop = Crop.query.filter_by(crop_name=crop_name).first()
        #         if not crop:
        #             crop = Crop(crop_name=crop_name)
        #             db.session.add(crop)
        #             db.session.commit()
        #         season = Season.query.filter_by(season_name=season_name).first()
        #         if not season:
        #             season = Season(season_name=season_name)
        #             db.session.add(season)
        #             db.session.commit()
        #         district = District.query.filter_by(district_name=district_name).first()
        #         if not district:
        #             district = District(district_name=district_name, state_id=state.state_id)
        #             db.session.add(district)
        #             db.session.commit()
        #         crop_data = CropData(crop_id=crop.crop_id, season_id=season.season_id, district_id=district.district_id, area=float(area), production=float(production), yield_data=float(yield_), profit=float(profit), rainfall=float(rainfall), year=int(year))
        #         db.session.add(crop_data)
        #         db.session.commit()

    return app
