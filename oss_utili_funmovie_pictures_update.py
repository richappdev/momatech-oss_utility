### oss_util_funmovie_pictures_update ###

# -*- coding: utf-8 -*-
from time import sleep
from datetime import datetime
import os
import sys

import oss2

def get_local_image_file_list(path):
	mtime_list = []
	file_list = []

	files = next(os.walk(path))[2]
	for file in files:
		if file.endswith('.jpg') or file.endswith('.png'):
			file_list.append(file)
			mtime_list.append(os.path.getmtime(path+file))
	return file_list, mtime_list

def get_oss_image_file_list(bucket):
	prefix = 'FunMovie/pictures/' + folder + '/'
	mtime_list = []
	file_list = []

	for obj in oss2.ObjectIterator(bucket, prefix):
		if obj.key.endswith('.jpg') or obj.key.endswith('.png'):
			file_list.append((obj.key.split('/'))[len(obj.key.split('/'))-1])	#remove prefix and get only file name
			mtime_list.append(int(obj.last_modified))
	return file_list, mtime_list

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

for i, folder in enumerate(folders):

	bucket_name_str = bucket_name_prefix + folder
	print(("\r\n>>>>>> %s") % bucket_name_str)

	start_time = datetime.now()

	### Get local files list ###
	path = local_path_prefix + folder + '\\'
	files_local, mtime_local = get_local_file_list(path)
	print('Local IMAGE files count: %d' % len(files_local))

	### GEt OSS files list ###
	try:
		bucket = open_bucket('momatech-image-gallery')
		files_oss, mtime_oss = get_oss_file_list(bucket)
		print('OSS IMAGE files count: %d' % len(files_oss))
	except:
		print('Open bucket fail ...')
		break

	### Compare two lists ###
	list_diff = list(set(files_local)^set(files_oss))
	print('Difference IMAGE count: %d' % len(list_diff))
	if len(list_diff) > 0:
		#print('%d. %s' % (list_diff.index(file)+1, file))
		pass
	else:
		print('Folder is already synced')

	### Check UPDATED files by Last_Modified time ###
	### 規則：本機檔案的mtime 只要大於 OSS檔案的mtime, 則加入list_diff當中，準備上傳
	### 目前只有在兩端檔案個數一樣的時候，才去檢查更新動作，避免list range exception
	if len(list_diff) == 0:
		for j, time in enumerate(mtime_local):
			if time > mtime_oss[j]:
				list_diff.append(files_local[j])

	### Sync/Upload file to OSS ###
	if len(list_diff) > 0:
		print('\r\nReady to upload/update files to OS:')

		try:
			bucket_upload = open_bucket('momatech-image-gallery/FunMovie/pictures/'+folder)
		except:
			print('Open bucket_upload fail ...')
			break
		
		for file in list_diff:
			full_path = path + file

			try:
				print(('%d. %s') % (list_diff.index(file)+1, full_path), end='', flush=True)
				with open(full_path, 'rb') as fileobj:
					bucket_upload.put_object(file, fileobj);
					fileobj.close()
					print(' ... OK')
			except:
				print(' ... fail')

	print('\r\n')
	get_elapsed_time(start_time, datetime.now(), False)