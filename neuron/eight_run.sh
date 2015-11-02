#!/bin/bash

NRUN=1
d=8
DATA=${d}/8_temp.dat
i=8
OUT=${d}/8_results.dat
settings=settings.py


mkdir $d

echo -n '' > $OUT

for j in $(seq 1 $NRUN);
do
    python exp.py $i -d $d
    cat $DATA >> $OUT
    echo '' >> $OUT
done
