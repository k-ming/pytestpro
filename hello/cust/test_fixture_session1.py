
def test_fixture1(login):
    print("module1测试函数一...")

def test_fixture2(login):
    print("module1测试函数二...")


class TestLogin:
    def test_login(self, login):
        print("module1 class1 测试方法一...")

    def test_info(self, login):
        print("module1 class1 测试方法二...")

class TestLogin2:
    def test_account(self, login):
        print("module1 class2 测试方法一...")

    def test_logoff(self, login):
        print("module1 class2测试方法二...")