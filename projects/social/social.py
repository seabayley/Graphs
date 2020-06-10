import random


class User:
    def __init__(self, name):
        self.name = name


class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME

        for user in range(num_users):
            self.add_user(f"user_{self.last_id}")

        for user in self.users:
            aof = random.randint(1, avg_friendships*2)
            c_fs = self.friendships[user]
            c_nof = len(c_fs)
            af = set(self.users.keys()) - c_fs
            af.remove(user)
            while c_nof < aof:
                random_friend = random.choice(list(af))
                if len(self.friendships[random_friend]) < avg_friendships*2:
                    self.add_friendship(user, random_friend)
                    c_nof += 1
                af.remove(random_friend)

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        queue = [[user_id]]

        # Iterate over each friend the user has.
        # Add each friend to visited, along with the path.
        while len(queue) > 0:
            path = queue.pop(0)
            user = path[-1]
            if user not in visited.keys():
                for friend in self.friendships[user]:
                    new_path = list(path)
                    new_path.append(friend)
                    queue.append(new_path)
                    visited[user] = path

        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)
