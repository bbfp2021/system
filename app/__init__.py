from flask import Flask, render_template
from config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pandas as pd

app = Flask(__name__)

app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import models

storage_items = models.StorageList.query.all()
box_nums = [ele.box_num for ele in storage_items]
contents = [ele.content for ele in storage_items]
storage_df = pd.DataFrame({
    'box_num': box_nums,
    'content': contents
})

jobs = [None]

robots_list = [type('Robot', (object,), {"id":1, "pos_x": 3, "pos_y": 0, "pos_z": 1})]

lift_list = [type('Lift', (object,), {"pos_x": 0, "pos_y": 0, "current_floor": 1})]

from app import routes

