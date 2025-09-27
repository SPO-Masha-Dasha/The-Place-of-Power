import datetime

class BattleLogger:
    def __init__(self):
        self.logs = []

    def log(self, message):
        timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
        full_message = f"{timestamp} {message}"
        self.logs.append(full_message)
        print(full_message)

    def get_logs(self):
        return self.logs

    def clear(self):
        self.logs.clear()