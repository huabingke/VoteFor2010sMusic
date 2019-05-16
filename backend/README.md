db:
sqlite3

media.db

table user_info 
id, user_name, password, sex, identity,status

table poll_info
id, poll_name, options, status

table poll_log
id, poll_info_id, user_id, sex, select_id


REST API:

/hello       say hello
/login       post 登陆
/register    post 注册
/poll        get  展示投票选项  
             post 投票
/view        get 展示投票结果
/user        get show 展示用户信息
/admin/user  get show 所有的用户信息
             delete 删除用户
             post  添加用户
/admin/poll  get 展示所有poll项
             post 添加poll项
             delete 删除poll项
             
               

