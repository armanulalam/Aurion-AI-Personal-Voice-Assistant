# Whatsapp
nipun = "01xxxxxxx"
ammu = "01xxxxxxx"
friend = "" # whatsapp group ID

def get_mobile_or_group(person):
    country_code = "+88"
    mobile_or_group = ""
    person = str(person).lower()
    if "nipun" in person:
        mobile_or_group = country_code + nipun
    elif "ammu" in person:
        mobile_or_group = country_code + ammu
    elif "friend" in person:
        mobile_or_group = friend
    else:
        mobile_or_group = "Person or Group not found in the contact. Please add it."

    return mobile_or_group

def IsGroup(person):
    m_or_id = str(get_mobile_or_group(person))
    if m_or_id.isdigit():
        return False
    else:
        return True
    
def IsInContact(person):
    if get_mobile_or_group(person).startswith("Person"):
        return False
    else:
        return True