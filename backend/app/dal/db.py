from sqlite3 import connect
from app.model.user import User
from app.model.pollLog import PollLog
from app.model.pollLog import PollLog
db_name = "media.db"


def create_user_inof_db():
    con = connect(db_name)
    cur = con.cursor()
    #cur.execute('''drop table user_info''')
    cur.execute('''create table if not exists user_info (
        id integer primary key autoincrement,
        sex integer ,
        user_name varchar(50),
        password varchar(50),
        user_identity integer
    );''')
    con.close()

def create_poll_info_db():
    con = connect(db_name)
    cur = con.cursor()
    # cur.execute('''drop table poll_info''')
    cur.execute('''create table if not exists poll_info (
        id integer primary key autoincrement ,
        poll_name varchar(500),
        options varchar (5000), 
    );''')
    con.close()


def create_poll_log_db():
    con = connect(db_name)
    cur = con.cursor()
    # cur.execute('''drop table poll_log''')
    cur.execute('''create table if not exists poll_log (
        id integer primary key autoincrement ,
        poll_id integer ,
        user_id integer ,
        sex integer ,
        select_id integer 
    );''')
    cur.close()


def search_user_by_name(user_name):
    con = connect(db_name)
    cur = con.cursor()
    cur.execute('''select * from user_info where user_name =?''',(user_name,))
    user_info = cur.fetchone()
    if user_info is None:
        return None
    else:
        return User(user_info['user_name'],
                    user_info['password'],
                    user_info['sex'],
                    user_info['user_identity'],
                    user_info['id'])

def insert_user_info(user):
    con = connect(db_name)
    cur = con.cursor()
    cur.execute('''insert into user_info(sex,user_name,password,user_identity) values(?,?,?,?)''',
                (user.sex, user.name, user.password, user.identity))
    id = cur.lastrowid
    con.commit()
    con.close()
    return id

def delete_user_info(user_id):
    con = connect(db_name)
    cur = con.cursor()
    cur.execute('''delete from user_info where id=?''',(user_id,))
    con.commit()
    con.close()




if __name__=="__main__":
    create_user_inof_db()
    create_poll_info_db()
    create_poll_log_db()