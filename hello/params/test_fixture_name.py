import pytest
'''
本文测试函数的name参数，及返回值
'''

@pytest.fixture(name='fun_1')
def login():
    print("login前置...")
    yield
    print("login后置...done")

@pytest.fixture()
def login1():
    print('login1前置...')
    return 66

def test_login(fun_1):
    print("测试函数一...")


def test_login1(login1):
    print("测试函数二，获取到的return:{}".format(login1))

def test_logins(fun_1, login1):
    print("测试函数三，多调用，获取到的return:{}".format(login1))

if __name__ == '__main__':
    pytest.main()