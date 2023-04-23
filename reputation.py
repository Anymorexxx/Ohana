import datetime
from datetime import datetime

class User:
    def __init__(self, member):
        self.member = member
        self.connect_time_in_channel = datetime.now()

    def get_total_time(self):
        return datetime.now() - self.connect_time_in_channel

