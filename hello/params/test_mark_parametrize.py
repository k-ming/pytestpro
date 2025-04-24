import pytest

from hello.params.test_params import params

'''
pytest.mark.parametrize()参数化
'''

@pytest.mark.parametrize('a', [3,6])
@pytest.mark.parame
def test_a(a):
    print("函数数据参数化...")
    assert a%3 == 0


@pytest.mark.parametrize('a,b', [(1,2), (2,1)])
@pytest.mark.parame
def test_b(a,b):
    print("多个参数...")
    assert a+b == 3 # 对a b元组中的数据分别取数想加


def datas():
    return [(1,2), (2,1),(0,3),(2,2)]

@pytest.mark.parametrize('a,b', datas())
@pytest.mark.parame3
def test_c(a,b):
    print("函数返回值作为入参：{}+{}".format(a,b))
    assert a+b == 3

@pytest.mark.parametrize("inp,expected", [('1+2', 3), ("2*2", 4),
                                          pytest.param("6*6", 42, marks=pytest.mark.xfail(reason="参数化验证失败", run=True)) ,
                                          pytest.param("6*9", 53, marks=pytest.mark.skip(reason="跳过此case")),
                                          pytest.param("3*9", 27, marks=pytest.mark.parame4),
                                          pytest.param("8*7", 55, marks=pytest.mark.parame5)])
@pytest.mark.parame4
def test_d(inp, expected):
    assert eval(inp) == expected


data_1 = (1,2,3)
data_2 = (4,5,6)

@pytest.mark.parametrize('a', data_1)
@pytest.mark.parametrize('b', data_2)
@pytest.mark.parame6
def test_d(a, b):
    assert a+b == 3