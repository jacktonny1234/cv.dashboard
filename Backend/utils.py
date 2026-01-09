import os
import base64
import datetime
import random, string

def expect(input, expectedType, field):
    if isinstance(input, expectedType):
        return input
    raise AssertionError("Invalid input for type", field)

def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def getfilepath(pic_data):
    filepath = ""
    if pic_data == None:
        return filepath
    str_time = datetime.datetime.now().strftime('%Y.%m.%d_%H.%M.%S.')
    str_rand = randomword(10)
    if ";base64," in pic_data:
        nFindPos = pic_data.find(";base64,")
        filepath = os.path.abspath(os.path.dirname(__file__)) + '/uploads/' + str_time + str_rand + '.' + pic_data[11:nFindPos]
        fp1 = os.path.join(filepath)
        unpack_data = base64.b64decode(pic_data[nFindPos+8:])
        open(fp1, 'w+b').write(unpack_data)

    return filepath
