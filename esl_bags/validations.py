import re

def emailValidate(email):
    if not isValid(email):
        return True
    return False

regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

def isValid(email):
    if re.fullmatch(regex, email):
      return True
    return False


def valueBlankValidate(value):
    print("teste")
    print(value)
    if value == "" or value == None:
        return True
    return False
