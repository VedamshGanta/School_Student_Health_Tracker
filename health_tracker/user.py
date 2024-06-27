class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.health_data = []

    def add_health_data(self, data):
        self.health_data.append(data)
