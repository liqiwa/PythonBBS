#完成主题数据的维护和更新
import functools,datetime,time
from flask import Blueprint,flash,g,render_template,redirect,session,url_for
from werkzeug.security import check_password_hash,generate_password_hash
import db
#声明蓝图
bg  =Blueprint("blog",__name__,url_prefix="/blog")

@bg.route('/index',methods = ['GET'])
def index():
    return render_template('blog/index.html')

@bg.route('/topic',methods = ['GET'])
def topic():
    return render_template('blog/topic.html')

@bg.route('/category',methods = ['GET'])
def category():
    return render_template('blog/category.html')

