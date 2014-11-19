#!/bin/bash
path=`pwd`
for i in 2 4 6
do
	cd $path/$i_p1
	pwd
	/usr/local/bin/ffmpeg -framerate 1/0.2 -i trj_$i_0_%d.png  -c:v libx264 -r 30 -pix_fmt yuv420p $i_ratio_1_frame_5.mp4
	/usr/local/bin/ffmpeg -framerate 1/0.5 -i trj_$i_0_%d.png  -c:v libx264 -r 30 -pix_fmt yuv420p $i_ratio_1_frame_2.mp4
	
	cd $path/$i_p3
	/usr/local/bin/ffmpeg -framerate 1/0.2 -i trj_$i_0_%d.png  -c:v libx264 -r 30 -pix_fmt yuv420p $i_ratio_3_frame_5.mp4
	/usr/local/bin/ffmpeg -framerate 1/0.5 -i trj_$i_0_%d.png  -c:v libx264 -r 30 -pix_fmt yuv420p $i_ratio_3_frame_2.mp4
done
