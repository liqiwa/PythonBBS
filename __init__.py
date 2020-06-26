import os
from flask import Flask,render_template
import auth,blog
from db import get_db
#数据库内容添加,初始化链接

app = Flask(__name__)

    # a simple page that says hello
    #@app.route('')
    # app.register_blueprint(bp)
print('111')
app.register_blueprint(auth.bp)
app.register_blueprint(blog.bg)
@app.route('/')
def home():
     return render_template('/blog/index.html')

if __name__ == '__main__':
    app.run()