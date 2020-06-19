

#完善类别方法。登陆页面、退出页面、注册页面逻辑。
import functools,time
from flask import (
    Blueprint,flash,g,redirect,render_template,request,session,url_for
)
from werkzeug.security import check_password_hash,generate_password_hash
from db import get_db
from db import  Users

bp = Blueprint("auth", __name__, url_prefix="/auth")

def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
@bp.route('/register',method =("GET","POST"))
def register():
    # 插入Mysql数据库中
    if request.method =="POST":
        username = request.form['username']
        userpass = request.form['userpass']
        usermail =request.form['usermail']
        userdate = time.time()
        userlevel = '1'
        new_users = Users(user_name=username,user_pass = userpass,user_mail = usermail,
                          user_date = userdate,user_level = userlevel)
        db = get_db()
        db.add(new_users)
        db.commit()
        db.close
        return render_template('register.html')

@bp.route('/login', methods=['POST'])
def singin():
    # 查询Mysql数据库中用户名和密码
        request.form['username']
        return render_template('')

