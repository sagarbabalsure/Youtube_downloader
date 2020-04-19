#import all required libraries
from pytube import YouTube
from pytube import exceptions
from pytube.cli import on_progress
import os

print("\n")
print("\t**** This is simple command line interface for downloading videos or audios from youtube ****")
print("\n\tYou want to download Single file(video or audio) or Multiple files(video or audio)")

#Take input as yow want to download single file or multiple files
while True:
	single_or_mult = input("\tType 'S' for single file or 'M' for multiple files : ")
	if single_or_mult == "S" or single_or_mult == 'M':
		break
	else:
		print("\n\tError : Please enter valid keyword")

#make new directories in your file system for storing downloaded files
cwd = os.getcwd()
new_dir1 = "videos"
new_dir2 = "audios"
path_for_vid = os.path.join(cwd,new_dir1)
path_for_aud = os.path.join(cwd,new_dir2)
try:
	os.mkdir(path_for_vid)
	os.mkdir(path_for_aud)
except:
	pass
 
if single_or_mult == 'S':
	#Take the youtube link from the user
	link = input("\n\tCopy & paste the youtube link from search bar : ")
	print("\n\tLoading please wait...")
	#all exception handled
	try:
		yt = YouTube(link,on_progress_callback=on_progress)
	except exceptions.RegexMatchError:
		print("\tError : Your url pattern not matching please copy proper url.")
		exit()
	except exceptions.VideoUnavailable as vu:
		print("\tError :",vu,"please try another video.")
		exit()
	except KeyError:
		print("\tError : video is streaming live and cannot be loaded")
		exit()
	except exceptions.PytubeError as pte:
		print("\tError :",pte)
		exit()
	
	#Select video or audio
	print("\n\tWhat you want to download video or audio? ")
	audio_or_video = input("\tType 'V' for Video and 'A' for Audio and 'E' for exit: ")

	if audio_or_video == 'V':
		video = yt.streams.filter(progressive=True).all()
		res_list = list()
		for v in range(len(video)):
			res_list.append(video[v].resolution)
		print("\tAvailable resolutions for downloading: ")
		for res in range(0,len(res_list)):
			print("\t\t",res+1,":",res_list[res],"(",(yt.streams.filter(progressive=True, subtype="mp4", resolution=str(res_list[res])).first().filesize)/10**6,"MB)")
		res = int(input("\n\tEnter resolution type: "))
		stream = yt.streams.filter(progressive=True, subtype="mp4", resolution=str(res_list[res-1])).first()
		print("\n\tdownloading ", yt.title)
		stream.download(path_for_vid)
		print("\n\tvideo downloading completed")
		res_list.clear()
	elif audio_or_video == 'A':
		audio = yt.streams.filter(only_audio=True).first()
		print("\n\tdownloading ",audio.title,"(",(audio.filesize)/10**6,"MB)")
		audio.download(path_for_aud)
		print("\n\taudio downloading completed")
	else:
		exit()


elif single_or_mult == 'M':
	file = input("\n\tEnter file name: ")
	try:
		with open(file,'r') as fh:
			links = fh.readlines()
	except FileNotFoundError as fnfe:
		print("\tError : No such file or directory: ",file)
		exit()

	print("\n\tWhat you want to download video or audio? ")
	audio_or_video = input("\tType 'V' for Video and 'A' for Audio and 'E' for exit: ")
	i=1

	if audio_or_video == 'V':
		for ln in links:
			try:
				yt1 = YouTube(ln,on_progress_callback=on_progress)
			except exceptions.RegexMatchError:
				print("\tError : Your url pattern not matching please copy proper url.")
				continue
			except exceptions.VideoUnavailable as vu:
				print("\tError :",vu,"please try another video.")
				continue
			except KeyError:
				print("\tError : video is streaming live and cannot be loaded")
				continue
			except exceptions.PytubeError as pte:
				print("\t",pte)
				continue
			video = yt1.streams.filter(progressive=True).all()
			res_list = list()
			for v in range(len(video)):
				res_list.append(video[v].resolution)
			print("\t",i,".Available resolutions for downloading (video title : ",yt1.title,") : ")
			for res in range(0,len(res_list)):
				print("\t\t",res+1,":",res_list[res],"(",(yt1.streams.filter(progressive=True, subtype="mp4", resolution=str(res_list[res])).first().filesize)/10**6,"MB)")
			res = int(input("\n\tEnter resolution type: "))
			stream = yt1.streams.filter(progressive=True, subtype="mp4", resolution=str(res_list[res-1])).first()
			print("\n\tdownloading ", yt1.title)
			stream.download(path_for_vid)
			print("\n\t",i,"videos downloaded")
			i=i+1
			res_list.clear()
	elif audio_or_video == 'A':
		for ln in links:
			try:
				yt1 = YouTube(ln,on_progress_callback=on_progress)
			except exceptions.RegexMatchError:
				print("\tError : Your url pattern not matching please copy proper url.")
				continue
			except exceptions.VideoUnavailable as vu:
				print("\tError :",vu,"please try another video.")
				continue
			except KeyError:
				print("\tError : video is streaming live and cannot be loaded")
				continue
			except exceptions.PytubeError as pte:
				print("\t",pte)
				continue
			audio = yt1.streams.filter(only_audio=True).first()
			print("\n\tdownloading ",audio.title,"(",(audio.filesize)/10**6,"MB)")
			audio.download(path_for_aud)
			print("\n\t",i,"audios downloaded")
			i=i+1
	else:
		exit()


else:
	exit()
