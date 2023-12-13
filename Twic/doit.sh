#!/bin/bash

for i in {1517..1518}
do
    echo wget http://www.theweekinchess.com/zips/twic${i}g.zip
    echo unzip -q twic${i}g.zip
    echo rm twic${i}g.zip
done
