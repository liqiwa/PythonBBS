

#完善类别方法。登陆页面、退出页面、注册页面逻辑。
import functools, datetime
from flask import  Blueprint,flash,g,redirect,render_template,request,session,url_for
from werkzeug.security import check_password_hash,generate_password_hash
from pythonnewbbs import db
from pythonnewbbs.db import Users
#声明蓝图
bp = Blueprint("auth",__name__, url_prefix="/auth")

@bp.route('/register',methods =['GET','POST'])
#注册新用户
def register():
    # 插入Mysql数据库中
    print('注册页面识别成功')
    if request.method == 'POST':
        #判断名称是否有重复，并在页面提示错误信息。


        #判断 密码长度，邮箱格式是否正确，并在页面提示错误信息。


        #无上述问题可以插入
        username = request.form['username']
        userpass = request.form['userpass']
        usermail = request.form['usermail']
        userdate = datetime.datetime.now().replace(microsecond=0)
        userlevel = '1'
        new_users = Users(user_name=username,user_pass = generate_password_hash(userpass),user_email = usermail,
                          user_date = userdate,user_level = userlevel)
        dbsession = db.get_db()
        dbsession.add(new_users)
        dbsession.commit()
        dbsession.close
        print('555')
        return redirect(url_for('auth.login'))
        #增加 用户成功、失败、等新消息，
        #页面访问判断跳转，在这里。
    return render_template('auth/register.html')
#用户登陆判断
@bp.route('/login', methods=['POST','GET'])
def login():
    # 查询Mysql数据库中用户名和密码
    print("5555555")
    if request.method == 'POST':
        username = request.form['username']
        print("6666666")


        print("8")

        password = request.form['password']
        print("9")

        dbsession = db.get_db()
        print("777777")

        error = None
        rows = dbsession.query(Users).filter(Users.user_name == username).first()
        #print('',rows.user_name,rows.user_pass)
        if rows is None:
            error = '用户名不存在'
        elif not check_password_hash(rows.user_pass,password):
            error = '密码不正确'
        if error is None:
            session.clear()
            session['user_id'] = rows.user_id
            return redirect(url_for('index'))
        flash(error)
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
         g.user = db.get_db().query(Users).filter(Users.user_id == user_id).first()

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))