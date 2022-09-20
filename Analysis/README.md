
split -b 45M  -a 2 -d  sinqcup22.sql  sinqcup22-split
git add sinqcup22-split*

-----

prompt: sqlite3
SQLite version 3.39.2 2022-07-21 15:24:47
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database.
sqlite> .output ../Analysis/twic1300.sql
sqlite> .open twic1300.sqlite
sqlite> .dump
sqlite> .quit

-----

sh ./dump.sh
git commit -m ... *.sql
rm mega.sqlite
cat *.sql | sqlite3 mega.sqlite
