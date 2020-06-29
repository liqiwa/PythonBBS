# import os,datetime
# from flask import Flask,render_template
# import auth,blog
# from db import get_db
# #数据库内容添加,初始化链接
#
# app = Flask(__name__)
#
#     # a simple page that says hello
#     #@app.route('')
#     # app.register_blueprint(bp)
# print('111')
# print('现在时间是% %',datetime.datetime.now().replace(microsecond=0))
# # 不添加 app.secret_key = 'dev'  竟然报错了。the session is unavailable because no secret key was set.
# # Set the secret_key on the application to something unique and secret.
# app.secret_key = 'dev'
# app.register_blueprint(auth.bp)
# app.register_blueprint(blog.bp)
# app.add_url_rule('/', endpoint='index')
# @app.route('/hello')
# def hello():
#
#     return 'hello,world'
#
# if __name__ == '__main__':
#     app.run()

import os

from flask import Flask


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
       # DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # register the database commands
    # from flaskr import db
    #
    # db.init_app(app)

    # apply the blueprints to the app
    from pythonnewbbs import blog
    from pythonnewbbs import auth

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    return app
