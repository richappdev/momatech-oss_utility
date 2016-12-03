# -*- coding: utf-8 -*-
from time import sleep
from datetime import datetime
import os
import sys

import oss2

def get_file_list(path):
	file_list = next(os.walk(path))[2]
	return list(file_list)

def get_elapsed_time(start, end, show_detail):
	elapsed_time = end - start
	if show_detail is True:
		print("Start Time\t%s" % start)
		print("End Time\t%s" % end)
	print("Elapsed Time\t%s" % elapsed_time)

def open_bucket(bucket_name_str):
	try:
		# 首先初始化AccessKeyId、AccessKeySecret、Endpoint等信息。
		# 通过环境变量获取，或者把诸如“<你的AccessKeyId>”替换成真实的AccessKeyId等。
		access_key_id = os.getenv('OSS_TEST_ACCESS_KEY_ID', 'OOepyKdFufHSV01J')
		access_key_secret = os.getenv('OSS_TEST_ACCESS_KEY_SECRET', 'Tpp4rc2DVWhyah4GNZwri7oFGKpBHu')
		bucket_name = os.getenv('OSS_TEST_BUCKET', bucket_name_str)
		endpoint = os.getenv('OSS_TEST_ENDPOINT', 'oss-cn-hangzhou.aliyuncs.com')

		# 确认上面的参数都填写正确了
		for param in (access_key_id, access_key_secret, bucket_name, endpoint):
			assert '<' not in param, '请设置参数：' + param

		# 列举所有的Bucket
		#   1. 先创建一个Service对象
		#   2. 用oss2.BucketIterator遍历
		service = oss2.Service(oss2.Auth(access_key_id, access_key_secret), endpoint, connect_timeout=10)
		#print('\n'.join(info.name for info in oss2.BucketIterator(service)))

		# 创建Bucket对象，所有Object相关的接口都可以通过Bucket对象来进行
		bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)

	except oss2.exceptions.OSS_REQUEST_ERROR_STATUS as e:
		print('status={0}, request_id={1}'.format(e.status, e.request_id))

	return bucket

### Main ###

bucket_name_prefix = 'momatech-image-gallery/FunMovie/pictures/'
local_path_prefix = 'D:\VirtualDir\FunMovie\pictures\\'
folders = ['advertisement','banners','banners_intouch','famous','files','homepicture','posters','topic','videotype']

if len(sys.argv) < 2:
	print('Please select an optaion in argv2 !\r\nExit.')
	sys.exit()

for folder in folders:
	#if folder is not 'advertisement' and folder is not 'homepicture':
	#	continue

	bucket_name_str = bucket_name_prefix + folder
	print(("\r\n>>>>>> %s") % bucket_name_str)

	start_time = datetime.now()

	### Get local files list ###
	path = local_path_prefix + folder + '\\'
	list_files = get_file_list(path)
	for file in list_files:
		if file.endswith('.jpg') or file.endswith('.png'):
			pass
		else:
			list_files.remove(file)
	print('Local IMAGE files count: %d' % len(list_files))		
	#print(list_files)

	### GEt OSS files list ###
	try:
		bucket = open_bucket('momatech-image-gallery')

		prefix = 'FunMovie/pictures/' + folder + '/'
		list_obj = []
		for obj in oss2.ObjectIterator(bucket, prefix):
			if obj.key.endswith('.jpg') or obj.key.endswith('.png'):
				list_obj.append((obj.key.split('/'))[len(obj.key.split('/'))-1])	#remove prefix and get only file name
		print('OSS IMAGE files count: %d' % len(list_obj))
		#print(list_obj)
	except:
		print('Open bucket fail ...')
		break

	### Compare two lists ###
	list_diff = list(set(list_files)^set(list_obj))
	print('Difference IMAGE count: %d' % len(list_diff))
	if len(list_diff) > 0:
		for file in list_diff:
			if file.endswith('.jpg') or file.endswith('.png'):
				if sys.argv[2] is '-detail':
					print('%d. %s' % (list_diff.index(file)+1, file))
			else:
				list_diff.remove(file)
	else:
		print('Folder is SYNC')

	### Sync/Upload file to OSS ###
	if len(list_diff) > 0:
		print('\r\nReady to upload to OS:')

		if sys.argv[1] is '-sync':
			bucket_upload = open_bucket('momatech-image-gallery/FunMovie/pictures/'+folder)
		
		for file in list_diff:
			if sys.argv[2] is '-detail':
				print(('%d. %s') % (list_diff.index(file)+1, path+file), end='', flush=True)
			
			try:
				with open(full_path, 'rb') as fileobj:
					if sys.argv[1] is '-sync':
						bucket_upload.put_object(file, fileobj);
					else:
						pass
					fileobj.close()
					print(' ... OK')
			except:
				print(' ... fail')

	print('\r\n')
	get_elapsed_time(start_time, datetime.now(), False)