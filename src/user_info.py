class UserInfo:
    def __init__(self):
        self.username = ""
        self.password = ""
        self.start_time = "0900"
        self.end_time = "1800"

    def set_info(self, username: str, password: str, start_time: str, end_time: str):
        self.username = username
        self.password = password
        if start_time:
            self.start_time = start_time
        if end_time:
            self.end_time = end_time
