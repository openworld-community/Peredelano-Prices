from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user_data):
        self.id = user_data['_id']
        self.username = user_data['user']['name']
        self.password = user_data['user']['password']
        self.role = user_data['role']
        self.subscription_level = user_data['subscription_level']

    def is_admin(self):
        return self.role == 'admin'
