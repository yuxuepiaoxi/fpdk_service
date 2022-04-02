
from threading import Thread
from functools import wraps
from flask import Flask, jsonify
app = Flask(__name__)


def asyncz(f):
	wraps(f)
	def wrapper(*args, **kwargs):
		thr = Thread(target=f, args=args, kwargs=kwargs)
		thr.start()
	return wrapper


@asyncz
def long_task():
	"""耗时处理逻辑

	:return:
	"""
	import time
	time.sleep(60)
	print('长时间处理')
	print('更新状态')
	print('OK')


def insert_data():
	print('插入记录')
	return '插入成功'


@app.route('/test')
def index():

	# 同步执行插入
	res = insert_data()
	print('插入：', res)

	# 耗时处理逻辑
	long_task()

	# 同步返回结果
	result = {'code': '000000', 'message': 'message', 'data': {}}
	return jsonify(result)


if __name__ == '__main__':
	app.run(debug=True)

