

#完善类别方法。登陆页面、退出页面、注册页面逻辑。
import functools,time,datetime
from flask import  Blueprint,flash,g,redirect,render_template,request,session,url_for
from werkzeug.security import check_password_hash,generate_password_hash
import db
#声明蓝图
bp = Blueprint("auth",__name__, url_prefix="/auth")

@bp.route('/register',methods =['GET','POST'])
#注册新用户
def register():
    # 插入Mysql数据库中
    print('222')
    if request.method == 'POST':
        #判断名称是否有重复


        #判断 密码长度，邮箱格式是否正确。


        #无上述问题可以插入
        print('333')
        username = request.form["username"]
        print('444 + %',username)
        userpass = request.form['userpass']
        usermail = request.form['usermail']
        userdate = datetime.datetime.now().replace(microsecond=0)
        userlevel = '1'
        new_users = db.Users(user_name=username,user_pass = userpass,user_email = usermail,
                          user_date = userdate,user_level = userlevel)
        session = db.get_db()
        session.add(new_users)
        session.commit()
        session.close
        print('555')
    return render_template('auth/register.html')
#用户登陆判断
@bp.route('/login', methods=['POST','GET'])
def login():
    # 查询Mysql数据库中用户名和密码
        return render_template('auth/login.html')

