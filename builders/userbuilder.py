from .user import Users


class UserBuilder:
    def __init__(self):
        self.id = 0
        self.first_name = ""
        self.last_name = ""
        self.username = ""
        self.email = ""
        self.password = ""

    @staticmethod
    def item():
        return UserBuilder()

    def with_first_name(self, first_name):
        self.first_name = first_name
        return self

    def with_last_name(self, last_name):
        self.last_name = last_name
        return self

    def with_username(self, username):
        self.username = username
        return self

    def with_email(self, email):
        self.email = email
        return self

    def with_password(self, password):
        self.password = password
        return self

    def with_id(self, id):
        self.id = id
        return self

    def build(self):
        return Users(self.id, self.first_name, self.last_name, self.username, self.email, self.password)
