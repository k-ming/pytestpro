import pytest
'''
pytest.skip() module级别跳过，和内部跳过
'''

@pytest.fixture()
def login():
    print('前置处理器...')
    yield
    print('后置处理器...done')

# @pytest.skip(reason="随机跳过", allow_module_level=True)
def test_login1(login):
    print('测试函数一...')

def test_login2(login):
    print('测试函数二...')

# @pytest.skip(reason ="跳过测试类",allow_module_level=True)
class TestLogin:
    def test_login(self, login):
        print("测试方法一...")
    # @pytest.skip(reason ="跳过测试方法二",allow_module_level=True)
    def test_login2(self, login):
        i = 0
        while i < 10:
            print("测试方法二,循环{}...".format(i))
            i += 1
            if i == 6:
                pytest.skip(" 后面的不执行了...")


# if __name__ == '__main__':
#     pytest.main()