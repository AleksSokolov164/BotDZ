class Singleton:
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[cls] = instance
        return cls._instances[cls]

    def __init__(self):
        self.users = dict()


s = Singleton()
s.users[283998956] = [[1, 2, 0, 0], [[' '] * 3 for _ in range(3)]]
print(s.users[283998956][0][0])

# # 283998956,0,0,0,0
# d = [['0'] * 3 for _ in range(3)]
# print(d[2][2])
