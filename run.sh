#!/bin/bash

NRUN=20
DATA=t_percentage_6_speed_25.dat
OUT=6_123.dat
i=6

for j in $(seq 1 $NRUN);
do
    python exp.py $i
    sed -n '9p' $DATA >> $OUT
    sed -n '17p' $DATA >> $OUT
    sed -n '25p' $DATA >> $OUT
    echo '' >> $OUT
done
