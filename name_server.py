import redis
from concurrent import futures

class NameServer:
    def __init__(self):
        self.error_occurred = False

        try:
            self.redis_client = redis.StrictRedis(host="localhost", port=6379, password="", decode_responses=True)
            self.redis_client.set("usr:Paco", "127.0.0.1:15830")
            self.redis_client.set("usr:Paca", "127.0.0.1:35733")
        except Exception as e:
            if not self.error_occurred:
                print(f"Error of connection with Redis")
                self.error_occurred = True
            raise

    def get_user_address(self, username):
        return self.redis_client.get(f"usr:{username}")

    def isSign(self, username):
       return self.redis_client.exists(f"usr:{username}")

    def set_user_status(self, username, status):
        status_str = "connected" if status else "disconnected"
        self.redis_client.set(f"usr:{username}:status", status_str)

    def get_user_status(self, username):
        status_str = self.redis_client.get(f"usr:{username}:status")
        return status_str == "connected"

    def get_connected_users(self):
        connected_users = []
        for key in self.redis_client.keys("usr:*:status"):
            username = key.split(":")[1]
            if self.get_user_status(username):
                connected_users.append(username)
        return connected_users