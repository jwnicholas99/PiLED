from utils.gui import convert_input

def check_none(ret):
    if ret is not None:
        raise Exception

def test_convert_input():
    # Test bool
    ret = convert_input("1", "bool", "param", "bool")
    check_none(ret)

    ret = convert_input("3.67", "bool", "param", "bool")
    check_none(ret)

    ret = convert_input("-1000", "bool", "param", "bool")
    check_none(ret)

    # Test int
    ret = convert_input("1.0", "int", "param", " positive int")
    check_none(ret)

    ret = convert_input("-1", "int", "param", " positive int")
    check_none(ret)

    ret = convert_input("-1.0", "int", "param", " positive int")
    check_none(ret)

    ret = convert_input("True", "int", "param", " positive int")
    check_none(ret)

    ret = convert_input("[hello, moshi]", "int", "param", " positive int")
    check_none(ret)

    # Test float
    ret = convert_input("-1", "float", "param", " positive float")
    check_none(ret)

    ret = convert_input("-1.0", "float", "param", " positive float")
    check_none(ret)

    ret = convert_input("True", "float", "param", " positive float")
    check_none(ret)

    ret = convert_input("[hello, moshi]", "float", "param", " positive float")
    check_none(ret)

    # Test intensity
    ret = convert_input("25.01", "intensity", "param", "positive and between 0 and 255")
    check_none(ret)
    
    ret = convert_input("-1", "intensity", "param", "positive and between 0 and 255")
    check_none(ret)

    ret = convert_input("-1.0", "intensity", "param", "positive and between 0 and 255")
    check_none(ret)

    ret = convert_input("True", "intensity", "param", "positive and between 0 and 255")
    check_none(ret)

    ret = convert_input("[hello, moshi]", "intensity", "param", "positive and between 0 and 255")
    check_none(ret)

    # Test color
    ret = convert_input([], "color", "param", "non-empty")
    check_none(ret)

test_convert_input()