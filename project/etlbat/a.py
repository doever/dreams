import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

print(os.path.dirname(os.path.dirname(__file__)))
print(sys.path)
from common.db import test

test()
