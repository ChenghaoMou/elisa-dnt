#!/bin/sh

declare -a lan=("tgl" "hau" "swa" "tur" "urd" "hu" "rukr" "ukr")
declare -a data=("train_1" "tune" "test")

for i in "${lan[@]}"
do
	for j in "${data[@]}"
	do
		/auto/nlg-05/chengham/env/bin/python preprocess.py $1/$i-en/elisa.$j.$i $2/elisa.$j.$i.sub.dnt $2/elisa.$j.$i.sub.dnt.ini sub
		/auto/nlg-05/chengham/env/bin/python preprocess.py $1/$i-en/elisa.$j.en $2/elisa.$j.$i_en.sub.dnt $2/elisa.$j.$i_en.sub.dnt.ini sub
	done
done

for i in "${lan[@]}"
do
	/auto/nlg-05/chengham/env/bin/python preprocess.py $1/$i-en/elisa.test.$i $2/elisa.test.$i.del.dnt $2/elisa.test.$i.del.dnt.ini del
done
