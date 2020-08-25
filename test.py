from utils.gui import convert_input

def check_none(ret):
    if ret is not None:
        raise Exception

def test_convert_input():
    ret = convert_input("1", "bool", "param", "correct_type")
    check_none(ret)

    ret = convert_input("3.67", "bool", "param", "correct_type")
    check_none(ret)

    ret = convert_input("-1000", "bool", "param", "correct_type")
    check_none(ret)

test_convert_input()