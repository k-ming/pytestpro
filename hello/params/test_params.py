import pytest

@pytest.fixture(params=[1,2,(3,4,5),{"key1":"val1","key2":"val2"}])
def params(request):
    return request.param

@pytest.fixture(params=[1,2,(3,4,5),{"key1":"val1","key2":"val2"}], ids=["id_1","id_2","id_3","id_4"])
def params_ids(request):
    return request.param

def test_params(params):
    print("值:{}".format(params))

def test_params_2(params_ids):
    print(params_ids)