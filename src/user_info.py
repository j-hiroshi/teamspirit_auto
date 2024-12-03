class UserInfo:
    def __init__(self):
        self.username = ""
        self.password = ""
        self.start_time = ""
        self.end_time = ""
        self.start_date = ""
        self.end_date = ""

    def set_info(
        self,
        username: str,
        password: str,
        start_time: str,
        end_time: str,
        start_date: str,
        end_date: str,
    ):
        self.username = username
        self.password = password
        if start_time:
            self.start_time = start_time
        if end_time:
            self.end_time = end_time
        self.start_date = start_date
        self.end_date = end_date
