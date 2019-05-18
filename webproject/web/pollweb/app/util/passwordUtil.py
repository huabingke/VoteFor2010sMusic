from hashlib import md5
from random import Random


def create_salt(length=4):
    salt = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    char_len = len(chars) - 1
    random = Random()
    for i in range(length):
        salt += chars[random.randint(0,char_len)]
    return salt

def create_md5(password, salt):
    md5_obj = md5()
    md5_obj.update((password+salt).encode('utf-8'))
    return md5_obj.hexdigest()


if __name__=="__main__":
    pwd = "123456"
    salt = create_salt()
    md5_pwd = create_md5(pwd, salt)
    print(salt)
    print(md5_pwd)