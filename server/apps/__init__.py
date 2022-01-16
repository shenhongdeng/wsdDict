from flask import Flask, render_template
from flask_bootstrap import Bootstap
from flask_momnet import Mail
from flask_sqlalchemy import SQLAlchemy
from config import config

bootrstap = Bootstap()
main = Main()
moment = Momnet()
db = SQLAlchemy()

'''
初始化各种文件，返回创建APP的工厂函数，工厂函数的好处是可以创建过个不同配置的应用实例。
而且配置是可以动态进行修改的。而以往的写法中，由于app一开始就创建好了，那就算后期修改
配置也不起作用了。所以我们可以用工厂函数来穿件不同的app
'''

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    return app




