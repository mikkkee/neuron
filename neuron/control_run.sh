#!/bin/bash

NRUN=20
d=control_6
DATA=${d}/t_percentage_6_speed_25.dat
i=6
OUT=${d}/6_123.dat
settings=settings.py


mkdir $d

echo -n '' > $OUT

for j in $(seq 1 $NRUN);
do
    python exp.py $i -d $d
    cat $DATA >> $OUT
    echo '' >> $OUT
done
