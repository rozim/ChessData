import logging
import sys
import os
import json
import random

import time
import sqlitedict

from absl import app
from absl import flags

FLAGS = flags.FLAGS

def main(argv):
  print(len(argv[1])
  print(argv[1])
  db = sqlitedict.open(filename=argv[1:],
                       flag='c',
                       encode=json.dumps,
                       decode=json.loads)


if __name__ == "__main__":
  app.run(main)
