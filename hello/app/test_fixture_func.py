import pytest
'''
fixture function 级别的前后置处理，scope="function",或者不指定，默认就是function级别
需要在函数或者方法的入参中显示调用，执行时，会在所有测试函数或方法开始和结束后执行
'''

@pytest.fixture(scope='function')
def loginByPwd():
    # name = 'kingming'
    print("function级别前置..")  # 前置处理
    yield
    print("function级别后置...done") # 后置处理
    # return name

def test_get_user(loginByPwd):
    print("测试函数一...")

def test_get_account(loginByPwd):
    print("测试函数二...")


class TestLogin:
    def test_login(self, loginByPwd):
        print('test_login...')

    def test_getInfo(self, loginByPwd):
        print("test_getInfo...")

if __name__ == '__main__':
    pytest.main()