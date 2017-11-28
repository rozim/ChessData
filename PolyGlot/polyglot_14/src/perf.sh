for f in `cat pgn.txt`
do
    echo $f
    ./reader_perf $f > last
    if [ $? -ne 0 ]; then
        echo " "
        echo "ERROR"
        echo $f
        cat last
        echo " "
    fi
done