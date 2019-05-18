backup设计：
flask 和 flask-restplus 

db:
sqlite3

db库名称
media.db

db表名称
table user_info 
id, user_name, password, sex（0:male，1:female）, salt

table poll_info
id, poll_name, options, status

table poll_log
id, poll_info_id, user_id, sex, select_id


REST API:

/logout      get 退出，清除session
                 请求参数：无
                 返回参数：{"code": 0}
/login       post 登陆 
                  请求参数：user_name（用户名称）
                          password (密码)
                          其中 admin/admin 为管理员
                  返回参数：
                         code:0 登陆成功
                         code:1 失败
                         msg: 失败的具体原因
                         eg:
                         {"msg": "password is wrong", "code": 1}
/register    post 注册
                  请求参数：user_name(用户名称)
                           password（密码）
                           checkout_password(确认密码)
                           sex(性别 0 男 1 女)
                           全部必填，用户名全局唯一不允许重复的
                  返回参数：
                         code:0 登陆成功
                         code:1 失败
                         msg: 失败的具体原因
                         eg:
                        {"msg": "user already exist", "code": 1} 
/session     get  获取用户名信息
                  请求参数：
                          无
                  返回参数：
                         data:用户名称，没有为空
                         eg：
                         {data:''} or {'data':'admin'}                 
/poll        get  展示投票选项  
                   请求参数：
                           无
                   返回参数：
                         code:0 成功
                         code:1 失败
                         data:为投票选项
                         {"data": poll_datas, "code": 0}
                         poll_data:投票详情列表
                         其中具体信息如下
                         {'id': 投票列表id, 
                         'name': 投票名称, 
                         'options': 选项列表 
                         'view': true/false 用户是否可查看投票结果
                         }
                         view:true 展示查看投票结果按钮
                         view:false 展示投票按钮
                         用户为admin管理员名，那么view全部为true
                         其他登陆用户，根据是否已投过票展示true/false
                         未登陆用户，view全部为false，投票前需要先登陆
             post 投票
                   请求参数：
                       poll_id：投票列表id
                       select_id: 选择id,对应上面（options）顺序，从0开始，后端没有越界校验
                       user_name: 用户名名称
                       要求用户必须登陆才能投票，即session存在
                   返回参数：
                        code:0 登陆成功
                         code:1 失败
                        eg:
                            {"msg": "user is not login", "code": 1}
/view/<poll_id> get 展示投票结果
                     请求参数：
                           url中的poll_id：投票列表id
                     返回参数：
                           {"result": result, "result_sex": result_sex, "code": 0}
                           result:投票结果
                           eg:{a:10,b:20:c:10}
                           result_sex:根据男女区分的投票结果
                           eg:{0:{a:5,b:15,c:2},1:{a:5,b:5,c:8}}
                                 
/user        get show 展示用户信息
                    请求参数：
                        无
                    返回参数：
                        code:0 成功
                        code:1 失败
                        data:成功时，返回用户信息
                        {"msg": "user is not login", "code": 1}
                        {"data":{"id": user.id, "name": user.name, "sex": user.sex}, "code":0}
/admin/user  get show 管理查看所有的用户信息
                    必须为管理员
                    请求参数：
                        无
                    返回参数：
                        {"data": users, "code": 0}
                        data:用户列表
             delete 删除用户
                    必须为管理员
                    请求参数：
                        id：用户id
                    返回参数：
                        {"code": 0}
             post  添加用户
                    必须为管理员
                    请求参数：
                        user_name：用户
                        password:密码
                        sex：性别
                    返回参数：
                        {"code": 0}
/admin/poll  get 展示所有poll项
                 必须为管理员
                 请求参数：
                        无
                 返回参数：
                        {'data': poll_datas, "code": 0}
             post 添加poll项
                  必须为管理员
                  请求参数：
                    poll_name：投票的标题
                    options：字符串，选项，每个选项以，分割
                  返回：
                    {"code": 0}
             delete 删除poll项
                  必须为管理员  
                  请求参数：
                    poll_id：投票id
                  返回：
                    {"code": 0}

             
程序启动：
    1.cd 到 web/pollweb 路径下
    2.第一次启动先 输入 pip install -r requirements.txt
    3.python run.py     
    4.打开 http://127.0.0.1:5000/    可以看到api 接口，点击 default 可以看到所有的api接口
    5.login 登陆，现存用户信息 admin/admin 管理员  用户名 a-f 密码 123456 为普通用户  

