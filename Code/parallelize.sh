

fn=$1
bn=$(basename $fn)

out_dir=/tmp/$$
mkdir -p ${out_dir}
split -d -l 10 -a 3 ${fn} ${out_dir}/${bn}
ls ${out_dir}/${bn}* | xargs -P 5 -I % -t  python -u fen-analysis-db.py --fen=% --output=%.sqlite --depth=32 --reference=../Analysis/nn-ad9b42354671/pv1-deep/deep.sqlite

# lines=$(wc -l ${fn})
# nice python -u fen-analysis-db.py --fen=../Release/2022-10-05/mega-clean-sample-1000.txt --depth=31 --output=../Analysis/nn-ad9b42354671/pv1-deep/deep.sqlite >& deep31.shh

# seq 0 9 | nice xargs -P 3 -I % -t python -u fen-analysis-db.py --fen=../Analysis/nn-ad9b42354671/pv1/sinqcup22_%.txt --output=../Analysis/nn-ad9b42354671/pv1/sinqcup22_%.sqlite --depth=20 --reference=../Analysis/nn-ad9b42354671/pv1/mega.sqlite >& cup.txt
