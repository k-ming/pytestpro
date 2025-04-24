import pytest
import pdb


@pytest.fixture(scope='function')
def login():
    print("前置处理...")
    yield
    print("后置处理...done")

@pytest.mark.pdb
def test_pdb(login):
    print("测试函数一...")
    # pdb.set_trace()
    print('断点之后不会执行...')

@pytest.mark.pdb
def test_pdb2(login):
    print("测试函数二,不受断点影响...")

# pdb.set_trace()
@pytest.mark.pdb
def test_pdb3(login):
    print("测试函数三, 断点之后不执行...")