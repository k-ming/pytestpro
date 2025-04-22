# pytest 测试框架
## 一、框架约束
### 1.1、命名规则
- module 文件以test结尾或开头，如test_login.py
- class 以Test开头，且不能有构造方法，如class TestLogin：
- function 以test开头 如def test_login():
## 二、运行方式
### 2.1、主函数运行
```
class TestLogin:
    def test_login(self):
        print('test_login...')

if __name__ == '__main__':
    pytest.main()
```
### 2.2、命令行运行
```
# 当前路径运行
pytest ./test_login.py 
```
### 2.3、配置文件 pytest.ini 运行(常用)
```
[pytest]
addopts=-vs -m slow --html=./report/report.html
testpaths=testcase
test_files=test_*.py
test_classes=Test*
test_functions=test_*
makerers=
    smock:冒烟测试
```
## 三、共享机制 conftest.py
## 四、前后置处理 fixture装饰器
### 4.1、fixture调用方式
#### 4.1.1、入参式调用
```
@pytest.fixture()
def loginByPwd():
    print("loginByPwd...")

class TestLogin:
    def test_login(self, loginByPwd): # 状态shi
        print('test_login...')
```
#### 4.1.2、fixture相互调用
### 4.2、fixture做用域
#### 4.2.1 function域
- scope="function"时，会在所有调用的测试函数或方法的前后各执行一次，默认就是function
级别，有如下测试module test_fixture_function
```python
import pytest

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
```
- 可以看到，不管是外部函数， 还是测试类中的测试方法，只要显式调用了前置函数，都会在前后各执行一次
```
============================= test session starts ==============================
collecting ... collected 4 items

test_fixture_func.py::test_get_user function级别前置..
PASSED                               [ 25%]测试函数一...
function级别后置...done

test_fixture_func.py::test_get_account function级别前置..
PASSED                            [ 50%]测试函数二...
function级别后置...done

test_fixture_func.py::TestLogin::test_login function级别前置..
PASSED                       [ 75%]test_login...
function级别后置...done

test_fixture_func.py::TestLogin::test_getInfo function级别前置..
PASSED                     [100%]test_getInfo...
function级别后置...done
```
#### 4.2.2 class域
- scope="class"时，会在测试类下面的测试方法开始前和结束后执行一次，而在外部的测试函数不受影响，例如有如下测试module test_fixture_class.py
``` python
import pytest

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
```
- 则执行结果如下, 可以看到 外部的两个测试函数，各自执行了一次前置和后置，而在测试类下面的测试方法执行前后只执行了一次前后置函数
```
============================= test session starts ==============================
collecting ... collected 7 items

test_fixture_class.py::test_getUser class级别前置...
PASSED                               [ 14%]测试函数一...
class级别后置...done

test_fixture_class.py::test_getInfo class级别前置...
PASSED                               [ 28%]测试函数二...
class级别后置...done

test_fixture_class.py::TestLogin::test_login class级别前置...
PASSED                      [ 42%]类一测试方法一...

test_fixture_class.py::TestLogin::test_logout PASSED                     [ 57%]类一测试方法二...

test_fixture_class.py::TestLogin::test_logoff PASSED                     [ 71%]类一测试方法三...
class级别后置...done

test_fixture_class.py::TestAccount::test_amount class级别前置...
PASSED                   [ 85%]类二测试方法一...

test_fixture_class.py::TestAccount::test_getInfo PASSED                  [100%]类二测试方法二...
class级别后置...done


============================== 7 passed in 0.01s ===============================
```
#### 4.2.3 module域
- scope="module" 时，是对当前py文件生效，和class类似，有如下测试文件 test_fixture_module.py
```python
import pytest

'''
fixture module 级别前后置处理scope="module", 同一个python文件中，所有的测试函数和方法都受影响
函数和方法需要在入参中显式调用，但是在第一个测试函数前调用前置，在最后一个测试函数或方法执行后调用后置
'''
@pytest.fixture(scope='module')
def login():
    print("module级别前置...")
    yield
    print("module级别后置...done")


def test_getInfo(login):
    print("测试函数一...")

def test_getUser(login):
    print("测试函数二...")

class TestLogin:
    def test_login(self, login):
        print("测试方法一...")

    def test_logout(self, login):
        print("测试方法二...")


if __name__ == '__main__':
    pytest.main()
```
- 则测试结果如下，和class唯一的区别是，不会区分外部测试函数 ，还是测试类下面的测试方法，在第一个case前执行一次前置，在做后一个case后面执行一次后置
```
============================= test session starts ==============================
collecting ... collected 4 items

test_fixture_module.py::test_getInfo module级别前置...
PASSED                              [ 25%]测试函数一...

test_fixture_module.py::test_getUser PASSED                              [ 50%]测试函数二...

test_fixture_module.py::TestLogin::test_login PASSED                     [ 75%]测试方法一...

test_fixture_module.py::TestLogin::test_logout PASSED                    [100%]测试方法二...
module级别后置...done


============================== 4 passed in 0.01s ===============================
```
#### 4.2.4 session域
- scope="session" 时和共享文件conftest.py 一期使用，则根目录下的所有测试类、测试方法、测试函数都会受影响，且前后置只会在开始和结束后执行一次，有如下目录和文件
```
__init__.py
conftest.py
run.py
test_fixture_session1.py
test_fixture_session2.py
```
- conftest.py 内容如下
```python
import pytest

@pytest.fixture(scope='session')
def login():
    print("session级别前置...")
    yield
    print("session级别后置...done")
```
- run.py 内容如下
```python
import pytest

if __name__ == "__main__":
    pytest.main(['-vs', './test_fixture_session1.py', './test_fixture_session2.py'])
```
- test_fixture_session1.py 和 test_fixture_session2.py内容相似
```python
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
```
- 则在run.py 中执行方法后会发现，这个目录下只执行了一次前后置函数
```
============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.3.5, pluggy-1.5.0 -- /Users/hb32366/devs/PyTestPro/venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/hb32366/devs/PyTestPro/hello/cust
collecting ... collected 12 items

test_fixture_session1.py::test_fixture1 session级别前置...
module1测试函数一...
PASSED
test_fixture_session1.py::test_fixture2 module1测试函数二...
PASSED
test_fixture_session1.py::TestLogin::test_login module1 class1 测试方法一...
PASSED
test_fixture_session1.py::TestLogin::test_info module1 class1 测试方法二...
PASSED
test_fixture_session1.py::TestLogin2::test_account module1 class2 测试方法一...
PASSED
test_fixture_session1.py::TestLogin2::test_logoff module1 class2测试方法二...
PASSED
test_fixture_session2.py::test_fixture1 module2测试函数一...
PASSED
test_fixture_session2.py::test_fixture2 module2测试函数二...
PASSED
test_fixture_session2.py::TestLogin::test_logout module2 class1 测试方法一...
PASSED
test_fixture_session2.py::TestLogin::test_register module2 class1 测试方法二...
PASSED
test_fixture_session2.py::TestLogin2::test_cor module2 class2 测试方法一...
PASSED
test_fixture_session2.py::TestLogin2::test_card module2 class2测试方法二...
PASSEDsession级别后置...done

============================== 12 passed in 0.01s ==============================
```
### 4.3、fixture参数
#### 4.3.1 name参数

#### 4.3.2 parame参数
- @pytest.fixture(params=[1,2,(3,4,5),{"key1":"val1","key2":"val2"}]) 支持可迭代参数
- 则下面的测试脚本执行结果如下
```python
import pytest

@pytest.fixture(params=[1,2,(3,4,5),{"key1":"val1","key2":"val2"}])
def params(request):
    return request.param
```
```
============================= test session starts ==============================
collecting ... collected 4 items

test_params.py::test_params[1] PASSED                                    [ 25%]值:1

test_params.py::test_params[2] PASSED                                    [ 50%]值:2

test_params.py::test_params[params2] PASSED                              [ 75%]值:(3, 4, 5)

test_params.py::test_params[params3] PASSED                              [100%]值:{'key1': 'val1', 'key2': 'val2'}


============================== 4 passed in 0.01s ===============================
```
#### 4.3.3 ids参数
- ids 一般与 params 配合使用，和参数一一对应，则下面的代码执行后结果如下
```python
import  pytest

@pytest.fixture(params=[1,2,(3,4,5),{"key1":"val1","key2":"val2"}], ids=["id_1","id_2","id_3","id_4"])
def params_ids(request):
    return request.param


def test_params_2(params_ids):
    print(params_ids)
```
```
============================= test session starts ==============================
collecting ... collected 4 items

test_params.py::test_params_2[id_1] PASSED                               [ 25%]1

test_params.py::test_params_2[id_2] PASSED                               [ 50%]2

test_params.py::test_params_2[id_3] PASSED                               [ 75%](3, 4, 5)

test_params.py::test_params_2[id_4] PASSED                               [100%]{'key1': 'val1', 'key2': 'val2'}

============================== 4 passed in 0.01s ===============================
```
#### 4.3.4 autouse参数
- 当@fixture(autouse=true)时，即使不显式调用，也会自动在测试方法或函数前调用，按照指定的作用域执行，例如 test_fixture_autouse.py
```python
import pytest

@pytest.fixture(scope='class', autouse=True)
def login():
    print("autouse前置处理...")
    yield
    print("autouse后置处理...")


def test_fix1():
    print("测试函数一...")

def test_fix2():
    print("测试函数二...")

class TestLogin:
    def test_login(self):
        print("类一测试方法一")
    def test_login2(self):
        print("类二测试方法二...")

class TestLogout:
    def test_logout(self):
        print()

if __name__ == '__main__':
    pytest.main()
```
- 则执行结果如下,测试函数一、二各执行了一次前后置，测试类一、二各执行了一次前后置
```
============================= test session starts ==============================
collecting ... collected 5 items

test_fixture_autouse.py::test_fix1 autouse前置处理...
PASSED                                [ 20%]测试函数一...
autouse后置处理...

test_fixture_autouse.py::test_fix2 autouse前置处理...
PASSED                                [ 40%]测试函数二...
autouse后置处理...

test_fixture_autouse.py::TestLogin::test_login autouse前置处理...
PASSED                    [ 60%]类一测试方法一

test_fixture_autouse.py::TestLogin::test_login2 PASSED                   [ 80%]类二测试方法二...
autouse后置处理...

test_fixture_autouse.py::TestLogout::test_logout autouse前置处理...
PASSED                  [100%]
autouse后置处理...


============================== 5 passed in 0.01s ===============================

```
## 五、用例管理
### 5.1、 跳过用例skip、skipif
### 5.2、 pytest.skip() 装饰器
### 5.3、执行顺序
### 5.4、失败标记和失败重试
### 5.5、设置断点
## 六、数据驱动
### 6.1、 pytest.mark.parametrize参数化
## 七、测试报告管理
## 八、日志级别