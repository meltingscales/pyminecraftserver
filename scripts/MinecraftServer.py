import os


class MinecraftServer:

    def __init__(self, path: str):
        self.path = os.path.abspath(path)

        if not os.path.exists(self.path):
            raise Exception("Path does not exist!", self.path)




if __name__ == '__main__':
    mcs = MinecraftServer(path='../persistent/server/')

    print(mcs)
