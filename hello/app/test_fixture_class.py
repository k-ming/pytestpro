import pytest
'''
fixture class 级别前后置处理scope="class", 只影响当前文件中所有class下面的方法
函数和方法需要在入参中显式调用，会在每一个类下方法执行前调用前置，在所有方法执行后调用后置，
函数不受影响
'''

@pytest.fixture(scope='class')
def login():
    print("class级别前置...")
    yield
    print("class级别后置...done")


def test_getUser(login):
    print("测试函数一...")

def test_getInfo(login):
    print("测试函数二...")


class TestLogin:
    def test_login(self, login):
        print("类一测试方法一...")

    def test_logout(self, login):
        print("类一测试方法二...")

    def test_logoff(self, login):
        print("类一测试方法三...")


class TestAccount:
    def test_amount(self, login):
        print("类二测试方法一...")

    def test_getInfo(self, login):
        print("类二测试方法二...")


if __name__ == '__main__':
    pytest.main()