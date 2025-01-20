-----

nice time python headers2tsv_simple.py --pgn=../Release/2023-12-14/mega-clean-2400.pgn  > ../Release/2023-12-14/mega-clean-2400-headers.tsv

fast: 30 secs

-----

wc -l ../Release/2023-12-14/mega-clean-2400-headers.tsv
  808201 ../Release/2023-12-14/mega-clean-2400-headers.tsv

-----

sqlite3 mega-clean-2400-headers.db < headers2tsv_simple_schema.sql

-----

sqlite3 mega-clean-2400-headers.db
sqlite> .mode tabs
sqlite> .import ../Release/2023-12-14/mega-clean-2400-headers.tsv h
