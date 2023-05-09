from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config['JSON_AS_ASCII'] = False
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    #app.config["APPLICATION_ROOT"] = "/api"
    config[config_name].init_app(app)

    db.init_app(app)

    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.utils import utils
    app.register_blueprint(utils)

    from app.userApi import userPage
    app.register_blueprint(userPage)
    from app.managerApi import managerPage
    app.register_blueprint(managerPage)

    from app.superApi import superApi
    app.register_blueprint(superApi)



    from app.coursePage import coursePage
    app.register_blueprint(coursePage)

    from app.teacherApi import teacherPage
    app.register_blueprint(teacherPage)


    from app.labPage import labPage
    app.register_blueprint(labPage)

    from app.studentApi import studentPage
    app.register_blueprint(studentPage)

    from app.lessonApi import lessonPage
    app.register_blueprint(lessonPage)





    return app

