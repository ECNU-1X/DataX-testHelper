import random
import os
import math

def generate_data_file():
	with open("100M.txt", "w", encoding="utf-8") as fw:
	    for i in range(1,100000001):
	        str_list = [chr(i) for i in range(97,123)]   #a-z
	        string = ''.join(random.sample(str_list, 15))
	        fw.write(",".join([str(i), string, str(i*0.1)]) + "\n")

def get_chunks(l, chunk_size):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), chunk_size):
        yield l[i:i + chunk_size]

def file_split(file_path, to_dir, piece_num):
	with open(file_path) as fr:
		data_set = fr.readlines()
		chunk_size = 1 + len(data_set) // piece_num
		chunks = get_chunks(data_set, chunk_size)
		counter = 1
		for data in chunks:
			write_to = os.path.join(to_dir, os.path.basename(file_path) + "_part_%d.txt"%counter)
			with open(write_to, "w") as fw:
				for item in data:
					fw.write(item)

			counter += 1

def split_data_into_pieces():
	"""为了测试并发读取txt文件，将数据文件进行切片"""
	file_path_list = ["1000/1000.txt","10000/10000.txt","100000/100000.txt","1m/1m.txt","10m/10m.txt","100m/100m.txt"]
	to_dir_list = ["1000", "10000","100000","1m","10m","100m"]
	piece_num = 5
	for file_path, to_dir in zip(file_path_list, to_dir_list):
		file_split(file_path, to_dir, piece_num)



