class User:
    def __init__(self, username:str, name:str, password:str, friends: list["User"] = None):
        self.__username = username
        self.__name = name
        self.__password = password
        self.__walk_streak = 0
        self.__work_streak = 0
        self.__friends = friends if friends is not None else []

    def __repr__(self) -> str:
        return f"<User {self.username}: {self.name}>"

    def __eq__(self, other) -> bool:
        return self.__streak == other.__streak

    def __lt__(self, other) -> bool:
        return self.__streak < other.__streak

    def __gt__(self, other) -> bool:
        return self.__streak > other.__streak

    def __hash__(self) -> int:
        return hash(self.__username)

    @property
    def username(self) -> str:
        return self.__username

    @property
    def name(self) -> str:
        return self.__name

    @property
    def walk_streak(self):
        return self.__walk_streak

    @property
    def work_streak(self):
        return self.__work_streak

    @property
    def friends(self):
        return self.__friends

    def increment_walk_streak(self):
        self.__walk_streak += 1

    def lose_walk_streak(self):
        self.__walk_streak = 0

    def increment_work_streak(self):
        self.__work_streak += 1

    def lose_work_streak(self):
        self.__work_streak = 0

    def change_username(self, username:str):
        self.__username = username

    def remove_friend(self, friend:str):
        self.__friends.remove(friend)

    def add_friend(self, friend:str):
        if isinstance(friend, User):
            self.__friends.append(friend)
