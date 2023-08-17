print("hello world")
print("hello world")
print("hello world")
print("hello world")


def validate_password(password):
    import re # regular expression
    if len(password) < 8:
        return ("Password should be at least 8 characters or longer")
    elif not re.search("[0-9]", password):
        return ("Password must contain at least one digit")
    elif not re.search("[A-Z]", password):
        return ("Password must contain at least one uppercase letter")
    elif not re.search("[@_!#$%&^*()<>?~+-/\{}:]",password):
        return ("password must contain at least one special charaster")