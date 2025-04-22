"""
共享机制，该文件名称固定，路径在根目录
session 的前后置，只会在所有函数和方法开始前和结束后执行一次前后置
"""
import pytest


@pytest.fixture(scope='session')
def login():
    print("session级别前置...")
    yield
    print("session级别后置...done")
