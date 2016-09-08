"""
Pseudo-random django secret key generator.
- Does print SECRET key to terminal which can be seen as unsafe.
Copied from https://gist.github.com/mattseymour/9205591
"""

import string
import random

# Get ascii Characters numbers and punctuation
# (minus quote characters as they could terminate string).
char_list = [string.ascii_letters, string.digits, string.punctuation]
chars = ''.join(char_list).replace('\'', '').replace('"', '').replace('\\', '')

SECRET_KEY = ''.join([random.SystemRandom().choice(chars) for i in range(50)])

print(SECRET_KEY)
