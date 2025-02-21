# -*- coding: utf-8 -*-
from time import sleep
from datetime import datetime
import os

import oss2

folders = ['advertisement','banners','banners_intouch','famous','files','homepicture','posters','topic','videotype']

def get_file_list(path):
	file_list = next(os.walk(path))[2]
	return list(file_list)

for folder in folders:
	bucket_name_str = 'momatech-image-gallery/FunMovie/pictures/' + folder
	print(("\r\n>>>>>> %s") % bucket_name_str)

	#start-time
	start_time = datetime.now()

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
	service = oss2.Service(oss2.Auth(access_key_id, access_key_secret), endpoint)

	# 创建Bucket对象，所有Object相关的接口都可以通过Bucket对象来进行
	bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)

	count=0
	path = 'D:\VirtualDir\FunMovie\pictures\\' + folder + '\\'
	files = get_file_list(path)
	for file in files:
		if ".py" not in file:
			full_path = path + file
			try:
				with open(full_path, 'rb') as fileobj:
					print(('%d. %s') % (count, full_path))
					bucket.put_object(file, fileobj);
				count += 1
				fileobj.close()
			except:
				pass
	print(count)

	#end-time
	end_time = datetime.now()
	#elapsed-time
	elapsed_time = end_time - start_time
	
	print("Start Time\t%s" % start_time)
	print("End Time\t%s" % end_time)
	print("Elapsed Time\t%s" % elapsed_time)
