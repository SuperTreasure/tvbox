#coding=utf-8
#!/usr/bin/python
from importlib.machinery import SourceFileLoader
import argparse


def loadFromDisk(fileName):
    name = fileName.split('/')[-1].split('.')[0]
    sp = SourceFileLoader(name, fileName).load_module().Spider()
    return sp


def run(path, name):
    rPath = path
    if len(name) > 0:
        rPath = 'py/plugin/py_{0}.py'.format(name)
    sp = loadFromDisk(rPath)
    sp.categoryContent("热门游戏", 1, 1, 1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='choose your crawler')
    parser.add_argument('--path', type=str, default='py/plugin/py_douyu.py')
    parser.add_argument('--name', type=str, default='douyu')
    args = parser.parse_args()
    run(args.path, args.name)
