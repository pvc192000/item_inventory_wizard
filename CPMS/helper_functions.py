STATES = {"AL","AK","AS","AZ","AR","CA","CO","CT","DE","DC","FL","GA","GU","HI","ID","IL","IN","IA","KS","KY","LA",
"ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","MP","OH","OK","OR","PA","PR","RI",
"SC","SD","TN","TX","UT","VT","VA","VI","WA","WV","WI","WY"}

def validateStateCode(state):
    if state.upper() in STATES:
        return True
    else:
        return False

def validateZipCode(zip):
    digits = 0
    for i in zip:
        if zip[i].isnumeric():
            digits += 1
    if len(zip) == 5 and digits == 5:
        return True
    else:
        return False

def validateMiddleInitial(mi):
    if len(mi) == 1:
        return True
    else:
        return False

def validatePhone(phone):
    digits = 0
    for i in phone:
        if phone[i].isnumeric():
            digits += 1
    if digits == 10:
        return True
    else:
        return False

def validateFilename(fname):
    if fname.endswith('.pdf') or fname.endswith('.doc') or fname.endswith('.docx') or fname.endswith('.txt'):
        return True
    else:
        return False

def validatePassword(password):
    if len(password) > 5:
        return False
    else: 
        return True

def validateUserDetails(state, zipCode, mi, phone, password):
    if not validateStateCode(state):
        return "Invalid State code, please enter a valid two letter state code"
    elif not validatePhone(phone):
        return "Invalid Phone Number, phone number should have 10 digits"
    elif not validateMiddleInitial(mi):
        return "Invalid Middle Initial, enter only one character"
    elif not validateZipCode(zipCode):
        return "Invalid Zip Code, zip code should have 5 digits "
    elif not validatePassword(password):
        return "Invalid Password, password should be 5 character long"
    else:
        return True
