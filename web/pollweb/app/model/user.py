
class User():
    def __init__(self, name, password, sex, salt, id=None):
        self.name = name
        self.password = password
        self.sex = sex
        self.id = id
        self.salt = salt


