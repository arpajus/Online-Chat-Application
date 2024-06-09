import redis
from concurrent import futures

class NameServer:
    """
    Initialize the NameServer class by establishing a connection to Redis and setting up initial user data.

    Parameters:
        - self: the NameServer object itself

    Raises:
        - Exception: If there is an error connecting to Redis

    Returns:
        - None
    """
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

    """
    Set the status of a user in the Redis database.

    Parameters:
        - username (str): The username of the user whose status is being set.
        - status (bool): The status to set for the user. True for connected, False for disconnected.

    Returns:
        - None

    Example:
        set_user_status("Paco", True)  # Sets the status of user "Paco" to connected
    """
    def set_user_status(self, username, status):
        status_str = "connected" if status else "disconnected"
        self.redis_client.set(f"usr:{username}:status", status_str)

    """
    Get the status of a user from the Redis database.

    Parameters:
        - username (str): The username of the user whose status is being retrieved.

    Returns:
        - bool: True if the user is connected, False if the user is disconnected.

    Example:
        get_user_status("Paco")  # Returns True if user "Paco" is connected, False otherwise
    """
    def get_user_status(self, username):
        status_str = self.redis_client.get(f"usr:{username}:status")
        return status_str == "connected"

    """
    Get a list of usernames for users who are currently connected based on their status in the Redis database.

    Parameters:
        - self: The NameServer object itself

    Returns:
        - list: A list of usernames for users who are currently connected

    Example:
        get_connected_users()  # Returns a list of usernames for users who are currently connected
    """
    def get_connected_users(self):
        connected_users = []
        for key in self.redis_client.keys("usr:*:status"):
            username = key.split(":")[1]
            if self.get_user_status(username):
                connected_users.append(username)
        return connected_users