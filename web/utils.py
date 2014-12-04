import beanstalkc
import json
import sys
from config import BEANSTALK

try:
    b = beanstalkc.Connection(
        host=BEANSTALK['HOST'], port=BEANSTALK['PORT'])
except beanstalkc.SocketError:
    print "Error connect to beanstalk, make sure beanstalk is running"
    sys.exit()

b.use('verification')


def send_verification_code(phone, verification):
    # Send encoded json string to queue
    msg = {
        "number": phone.number,
        "message": "Kode verifikasi " + verification.code
    }
    b.put(json.dumps(msg))
