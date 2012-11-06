import random
import os
import time
import datetime

SECONDS = datetime.timedelta(days=1000).total_seconds()
NOW = int(time.time())

def main():
    FileGenerator(load_words()).generate('files').create()

def load_words():
    with open('words.txt') as words_file:
        return tuple(word.strip() for word in words_file)

class FileGenerator(object):

    def __init__(self, names):
        self.names = names

    def generate(self, dirname, depth=3):
        sample_names = random.sample(self.names, 10)
        files = [File(name) for name in sample_names[:7]]
        dir_names = sample_names[7:] if depth > 0 else []
        dirs = [self.generate(name, depth=depth - 1) for name in dir_names]
        return Directory(dirname, files + dirs)

class File(object):

    def __init__(self, name):
        self.name = name

    def create(self, basedir=None):
        path = self.make_path(basedir)
        os.mknod(path)
        File.change_time(path)

    def make_path(self, basedir):
        if basedir is None:
            return self.name
        return os.path.join(basedir, self.name)

    @classmethod
    def change_time(cls, path):
        new_time = NOW + random.randint(-SECONDS, SECONDS)
        os.utime(path, (new_time, new_time))

class Directory(File):
    
    def __init__(self, name, children):
        super(Directory, self).__init__(name)
        self.children = children

    def create(self, basedir=None):
        path = self.make_path(basedir)
        os.mkdir(path)
        for child in self.children:
            child.create(path)
        File.change_time(path)

if __name__ == '__main__':
    main()
