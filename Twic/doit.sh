#!/bin/bash
set -e

for i in {1650..1666}
do
    echo wget http://www.theweekinchess.com/zips/twic${i}g.zip
    echo unzip -q twic${i}g.zip
    echo rm -f twic${i}g.zip
done
