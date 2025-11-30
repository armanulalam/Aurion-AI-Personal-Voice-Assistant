# Email
arman = "xxxx@gmail.com"
nipun = "xxxxx@gmail.com"

def get_email_add(statement):
    email_add = ""
    statement = str(statement).lower()
    if 'arman' in statement:
        email_add += arman
    elif 'nipun' in statement:
        email_add += nipun
    else:
        email_add = "Email address is not found in the Email contact. Please add it."
    return email_add

def is_in_email_contact(statement):
    if get_email_add(statement).startswith("Email"):
        return False
    else:
        return True