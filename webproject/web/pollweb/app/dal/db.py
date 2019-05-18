from sqlite3 import connect
from app.model.user import User
from app.model.pollLog import PollLog
from app.model.pollInfo import PollInof
db_name = "media.db"


def create_user_info_db():
    con = connect(db_name)
    cur = con.cursor()
    #cur.execute('''drop table user_info''')
    cur.execute('''create table if not exists user_info (
        id integer primary key autoincrement,
        sex integer ,
        user_name varchar(50),
        password varchar(50),
        salt varchar(4)
    );''')
    con.close()

def create_poll_info_db():
    con = connect(db_name)
    cur = con.cursor()
    #cur.execute('''drop table poll_info''')
    cur.execute('''create table if not exists poll_info (
        id integer primary key autoincrement ,
        poll_name varchar(500),
        options varchar (5000)
    );''')
    con.close()


def create_poll_log_db():
    con = connect(db_name)
    cur = con.cursor()
    #cur.execute('''drop table poll_log''')
    cur.execute('''create table if not exists poll_log (
        id integer primary key autoincrement ,
        poll_id integer ,
        user_id integer ,
        sex integer ,
        select_id integer 
    );''')
    cur.close()

def insert_poll_log(poll_id, user_id, sex, select_id):
    con = connect(db_name)
    cur = con.cursor()
    cur.execute('''insert into poll_log(poll_id, user_id, sex, select_id) values(?,?,?,?)''',
                (poll_id, user_id, sex, select_id))
    id = cur.lastrowid
    con.commit()
    con.close()
    return id

def search_poll_by_poll_id(poll_id):
    con = connect(db_name)
    cur = con.cursor()
    cur.execute('''select * from poll_info where id =?''', (poll_id,))
    data = cur.fetchone()
    if data is not None:
        return data[2].split(',')
    else:
        return None

def search_poll_log_by_poll_id(poll_id, name_list):
    con = connect(db_name)
    cur = con.cursor()
    cur.execute('''select * from poll_log where poll_id =?''', (poll_id,))
    datas = cur.fetchall()
    result = {}
    result_sex = {0:{},1:{}}
    if datas is not None:
        for data in datas:
            select_id = data[4]
            sex = data[3]
            if name_list[select_id] not in result:
                result[name_list[select_id]] = 0
            if name_list[select_id] not in result_sex[sex]:
                result_sex[sex][name_list[select_id]] = 0
            result[name_list[select_id]] += 1
            result_sex[sex][name_list[select_id]] += 1
        r = sorted(result.items(), key=lambda d:d[1],reverse=True)
        result.clear()
        for key,v in r:
            result[key] = v
        r = sorted(result_sex[0].items(), key=lambda d: d[1],reverse=True)
        result_sex[0].clear()
        for k,v in r:
            result_sex[0][k] = v
        r = sorted(result_sex[1].items(), key=lambda d: d[1],reverse=True)
        result_sex[1].clear()
        for k, v in r:
            result_sex[1][k] = v
    return result, result_sex



def search_all_poll_info():
    con = connect(db_name)
    cur = con.cursor()
    cur.execute('''select * from poll_info ''')
    datas = cur.fetchall()
    poll_infos = []
    if datas is not None:
        for data in datas:
            poll_infos.append(PollInof(data[1], data[2], data[0]))
    return poll_infos


def search_user_by_name(user_name):
    con = connect(db_name)
    cur = con.cursor()
    cur.execute('''select * from user_info where user_name =?''', (user_name,))
    user_info = cur.fetchone()
    if user_info is None:
        return None
    else:
        return User(user_info[2],
                    user_info[3],
                    user_info[1],
                    user_info[4],
                    user_info[0])

def search_poll_by_user_id(user_id):
    con = connect(db_name)
    cur = con.cursor()
    cur.execute('''select * from poll_log where user_id =?''', (user_id,))
    datas = cur.fetchall()
    result = {}
    if datas is not None:
        for data in datas:
            result[data[1]] = ""
    return result


def search_all_users():
    con = connect(db_name)
    cur = con.cursor()
    cur.execute('''select * from user_info ''')
    datas = cur.fetchall()
    user_infos = []
    if datas is not None:
        for data in datas:
            user_infos.append(User(
                data[2],
                data[3],
                data[1],
                data[4],
                data[0]))
    return user_infos


def insert_user_info(user):
    con = connect(db_name)
    cur = con.cursor()
    cur.execute('''insert into user_info(sex, user_name, password, salt) values(?,?,?,?)''',
                (user.sex, user.name, user.password, user.salt))
    id = cur.lastrowid
    con.commit()
    con.close()
    return id

def insert_poll_info(poll_info):
    con = connect(db_name)
    cur = con.cursor()
    cur.execute('''insert into poll_info(poll_name,options) values(?,?)''',
                (poll_info.poll_name, poll_info.options))
    id = cur.lastrowid
    con.commit()
    con.close()
    return id

def delete_poll_id(poll_id):
    con = connect(db_name)
    cur = con.cursor()
    cur.execute('''delete from poll_info where id=?''', (poll_id,))
    con.commit()
    con.close()

def delete_by_poll_id(poll_id):
    con = connect(db_name)
    cur = con.cursor()
    cur.execute('''delete from poll_log where poll_id=?''', (poll_id,))
    con.commit()
    con.close()

def delete_user_info(user_id):
    con = connect(db_name)
    cur = con.cursor()
    cur.execute('''delete from user_info where id=?''',(user_id,))
    con.commit()
    con.close()



if __name__=="__main__":
    create_user_info_db()
    create_poll_info_db()
    create_poll_log_db()