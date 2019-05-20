backup design：
flask and flask-restplus 

db:
sqlite3

name of db library
media.db

name of db table
table user_info 
id, user_name, password, sex（0:male，1:female）, salt

table poll_info
id, poll_name, options

table poll_log
id, poll_id, user_id, sex, select_id


REST API:

/logout      get exit，clean session
                 Request Parameters：null	
                 Return Parameters：{"code": 0}
/login       post login 
                  Request Parameters：user_name
                          password 
                          admin/admin is the admin account
                  Return Parameters：
                         code:0 Login sucessfully
                         code:1 Login failed
                         msg: the reason for why it is failed
                         eg:
                         {"msg": "password is wrong", "code": 1}
/register    post register
                  Request Parameters：user_name
                           password
                           checkout_password
                           sex( 0 is male, 1 is female)
                           Must fill all, also the username is unique 
                  Return parameters：
                         code:0 Login sucessfully
                         code:1 Login failed
                         msg: the reason for why it is failed
                         eg:
                        {"msg": "user already exist", "code": 1} 
/session     get  get the username
                  Request Parameters：Null
                          
                  Return parameters：
                         data:username，if no just left it
                         eg：
                         {data:''} or {'data':'admin'}                 
/poll        get  display the options of poll  
                   Request parameters：
                           null
                   Return parameters：
                         code:0 sucessfully
                         code:1 failed
                         data:the options of poll
                         {"data": poll_datas, "code": 0}
                         poll_data:the detail of poll
                         
                         {'id': poll id, 
                         'name': poll name, 
                         'options': options list 
                         'view': true/false if the user could view the result
                         }
                         view:true for display the poll result
                         view:false for display the poll
                         admin is the admin account username，all the views are true
                         other user,display true/false according to they poll or not
						 Non-login users, all the views are false, it must login before submit poll
                         
             post poll
                   request parameters：
                       poll_id： poll id
                       select_id: select id,correspoding to the above （options） order， start from 0，
                       user_name: user name 
                       Require user must login to poll，so there is session exist
                   return parameters：
                        code:0 login sucessfully
                         code:1 login failed
                        eg:
                            {"msg": "user is not login", "code": 1}
/view/<poll_id> get display the poll result
                     request parameters：
                           poll_id in url：poll id
                     return parameters：
                           {"result": result, "result_sex": result_sex, "code": 0}
                           result:result of poll
                           eg:{a:10,b:20:c:10}
                           result_sex:seperate the result by gender
                           eg:{0:{a:5,b:15,c:2},1:{a:5,b:5,c:8}}
                                 
/user        get show display the information of user
                    request parameters：
                        null
                    return parameters：
                        code:0 sucessfully
                        code:1 failed
                        data:return the user information if it sucessfully
                        {"msg": "user is not login", "code": 1}
                        {"data":{"id": user.id, "name": user.name, "sex": user.sex}, "code":0}
/admin/user  get show manage view all the user information
                    Must be admin
                    request parameters：
                        null
                    return parameters：
                        {"data": users, "code": 0}
                        data:list of user
             delete delete user
                    must be admin
                    request parameter：
                        id：user id
                    return parameter：
                        {"code": 0}
             post  add user
                    must be admin
                    request parameters：
                        user_name： user name
                        password: password
                        sex：sex
                    return parameters：
                        {"code": 0}
/admin/poll  get display all the poll items
                 must be admin
                 request parameters：
                        null
                 return parameters：
                        {'data': poll_datas, "code": 0}
             post add poll itme
                  must be admin
                  request parameters：
                    poll_name：the title of poll
                    options：strings，options，each options will be divide by ,
                  return：
                    {"code": 0}
             delete delete poll itmes
			
                  must be admin  
                  request parameters：
                    poll_id：poll id
                  return：
                    {"code": 0}

             
How to start：
    1.cd web/pollweb 
    2.input pip install -r requirements.txt
    3.python run.py     
    4.then open http://127.0.0.1:5000/    to view the API，click default can view all the API
    5.login ， username admin password admin  is the current admin account,  username John password 123456 is the current normal user.  

