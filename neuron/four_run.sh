#!/bin/bash

NRUN=20
i=4
d=$i
DATA=${d}/t_percentage_${i}_speed_25.dat

OUT=${d}/${i}_all.dat
settings=settings.py


mkdir $d

echo -n '' > $OUT

for j in $(seq 1 $NRUN);
do
    python exp.py $i -d $d
    cat $DATA >> $OUT
    echo '' >> $OUT
done
