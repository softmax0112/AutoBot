class Users:

    def __init__(self, id, first_name, last_name, username, email, password):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = password

    def set_id(self, id):
        self.id = id

    def set_first_name(self, first_name):
        self.first_name = first_name

    def set_last_name(self, last_name):
        self.last_name = last_name

    def set_username(self, username):
        self.username = username

    def set_email(self, email):
        self.email = email

    def set_password(self, password):
        self.password = password

    def get_first_name(self) -> str:
        return self.first_name

    def get_last_name(self) -> str:
        return self.last_name

    def get_username(self) -> str:
        return self.username

    def get_email(self) -> str:
        return self.email

    def get_password(self) -> str:
        return self.password

    def get_id(self):
        return self.id

    def to_dict(self):
        return {
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'password': self.password
        }

    def display(self):
        print("\t\t\t User")
        print("Username: ", self.username)
        print("FirstName: ", self.first_name)
        print("LastName: ", self.last_name)
        print("Email: ", self.email)
