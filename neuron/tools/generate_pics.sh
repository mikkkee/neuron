#!/bin/bash

for i in 2 4 6
do
    mkdir ss_${i}_p1 ss_${i}_p3
    python exp.py ${i} -s settings_p1.py
    mv trj_${i}_* ss_${i}_p1
    python exp.py ${i} -s settings_p3.py
    mv trj_${i}_* ss_${i}_p3
done
