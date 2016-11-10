# -*- coding: utf-8 -*-
import time
import os

import oss2

bucket_name_str = 'momatech-image-gallery'
bucket_name_str += '/FunMovie'

# 以下代码展示了Bucket相关操作，诸如创建、删除、列举Bucket等。

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

def get_file_list(path):
	file_list = next(os.walk(path))[2]
	return list(file_list)

path = "."	#current folder
files = get_file_list(path)
for file in files:
	print(file)
	bucket.put_object_from_file(file, file);
