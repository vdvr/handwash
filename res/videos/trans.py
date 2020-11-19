import os

for videoname in filter(lambda filename: filename != __file__, os.listdir()):
	print(videoname[:-4])
	print(os.system(f"ffmpeg -i {videoname} -c:v libvpx-vp9 -b:v 2M {videoname[:-4] + '-vp9.webm'}"))
