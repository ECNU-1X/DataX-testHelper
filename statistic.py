"""
DataX 基于日志的性能分析工具

限时1小时做工具，做成啥样是啥样
2018-06
"""

__python__ = 3.6
__author__ = "Liu Kun"

import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))



def time_cost_info_extract(content, file_name):
	try:
		time_info_pattern = re.compile("StandAloneJobContainerCommunicator(.*?)%")
		result = re.findall(time_info_pattern, content)
		total_time_pattern = re.compile("任务总计耗时.*?(\d*?)s")
		total_items_pattern = re.compile("读出记录总数.*?(\d+)")
		total_time_cost = re.findall(total_time_pattern, content)[-1]
		total_item_num = re.findall(total_items_pattern, content)[-1]
		wait_writer_time = re.findall("All Task WaitWriterTime (.*?)s", content)[-1]
		wait_reader_time = re.findall("All Task WaitReaderTime (.*?)s", content)[-1]
		transformer_time = re.findall("Transformer usedTime (.*?)s", content)[-1]
		transformer_name = re.findall("transformer init success. name=(.*?),", content)[-1]
		channel_num = re.findall('"channel":(\d+)', content)[-1]
		paras = re.findall('Using (.*?) encryption', content)
		if paras and paras[0] in ["AES_E", "AES_D", "FPE", "RSA"]:
			transformer_name = transformer_name + "-"+ paras[0]
			if paras[0] == "RSA":
				transformer_name = file_name.split('1')[0]
		return {
			"wait_writer_time":wait_writer_time, 
			"wait_reader_time":wait_reader_time, 
			"transformer_time":transformer_time,
			"item_num":total_item_num,
			"total_time":total_time_cost,
			"transformer":transformer_name,
			"channel": channel_num
		}
	except IndexError as e:
		print(e)
		print("fail for %s"%file_name)


def system_info_extract(content):
	system_pattern = """	osInfo:	(.*)
	jvmInfo:	(.*)
	cpu num:	(\d+)"""
	result = re.findall(system_pattern, content)[-1]
	return {
		"os":result[0], 
		"jvm":result[1],
		"cpu num":result[2]
	}


def check_log_dir(directory):
	"""建议输入dataX的log目录"""
	result = {}
	logs = filter(lambda x:x.endswith('.log'), os.listdir(directory))
	for log_name in logs:
		try:
			try:
				file_content = open(os.path.join(directory, log_name), encoding="utf-8").read()
				time_info = time_cost_info_extract(file_content, log_name)
				sys_info = system_info_extract(file_content)
				if time_info:
					key = time_info["transformer"]+"-"+ time_info["item_num"] 
					result[key] = {**time_info, **sys_info}
			except IndexError as e:
				print(e)
		except UnicodeDecodeError as e:
			print(e)
	return result


def transformer_plot(log_result):
	from collections import defaultdict
	import matplotlib.pyplot as plt
	import numpy as np
	data_set = defaultdict(list)
	for item_name in log_result:
		item = log_result[item_name]
		transformer = item["transformer"]
		data_set[transformer].append(float(item["transformer_time"].replace(",","")))
	x_axis = ["1000", "10000", "100000", "1 million", "10 million", "100 million","1G"]
	plt.xlabel("Data Size")
	plt.ylabel("logarithmic Cost Time (log10) in second")
	plt.xticks(range(len(x_axis)), x_axis)
	for data in data_set:
		y = data_set[data]
		y.sort()
		for _ in range(len(x_axis)-len(y)) :
			y.append(0)
		print(y)
		plt.plot(np.log10(y), label=data)
	plt.legend()
	plt.show()



if __name__ == '__main__':
	import pprint
	result = check_log_dir(r"C:\Users\LabUser\Desktop\DataXMasker\性能实验\性能曲线绘制\实验结果\并发情况下的性能测试\channel5_log")
	# pprint.pprint(transformer_plot(result))
	pprint.pprint(result)