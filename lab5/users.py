class user:
    def __init__(self, id_user, name, password):
        self.id = id_user
        self.name = name
        self._password = password

    def show_user_info(self):
        return (f"{self.id} - {self.name}")