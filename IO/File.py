class FileReadAndWrite:
    @staticmethod
    def read(path):
        file = open(path, mode='r')
        content = file.read()
        file.close()
        return content

    @staticmethod
    def write(path, content):
        file = open(path, mode='w')
        file.write(content)
        file.close()
