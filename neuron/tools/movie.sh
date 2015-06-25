#!/bin/bash
path=`pwd`
for i in 2 4 6
do
	pwd
	/usr/local/bin/ffmpeg -framerate 1/0.2 -i trj_${i}_0_%d.png  -c:v libx264 -r 30 -pix_fmt yuv420p ${i}_ratio_1_frame_5.mp4
	/usr/local/bin/ffmpeg -framerate 1/0.5 -i trj_${i}_0_%d.png  -c:v libx264 -r 30 -pix_fmt yuv420p ${i}_ratio_1_frame_2.mp4

	cd $path/s_${i}_p3
	/usr/local/bin/ffmpeg -framerate 1/0.2 -i trj_${i}_0_%d.png  -c:v libx264 -r 30 -pix_fmt yuv420p ${i}_ratio_3_frame_5.mp4
	/usr/local/bin/ffmpeg -framerate 1/0.5 -i trj_${i}_0_%d.png  -c:v libx264 -r 30 -pix_fmt yuv420p ${i}_ratio_3_frame_2.mp4
done
