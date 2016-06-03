#!/usr/bin/python
#coding:utf-8
import requests
import time
import json
import copy
from multiprocessing.dummy import Pool as ThreadPool

hostlist = [
			{"endpoint":"agent_host_ip","url":"http://agent_host_ip:1988/health"}
			]
push_url = "http://agent_host/v1/push"

#################################################################

payload = []
data = {"endpoint":"","metric":"agent.latency","timestamp":"","step":60,"value":"","counterType":"GAUGE","tags":""}

def main():
	time_start = time.clock()
	pool = ThreadPool(8)
	pool.map(push_payload,hostlist)
	pool.close()
	pool.join()
	#print time.clock()-time_start
	print json.dumps(payload)


def push_payload(host):
	ts = int(time.time())
	latency = agent_healh_latency(host["url"])
	data["endpoint"] = host["endpoint"]
	data["value"] = latency
	data["timestamp"] = ts
	payload.append(copy.copy(data))

	#r = requests.post(push_url, data=json.dumps(payload))

def agent_healh_latency(url):
	result = -1
	try:
		r = requests.get(url,timeout=3)
		if r.status_code == 200:
			result = r.elapsed.microseconds/1000
			return result
	except Exception,e:
		return result

if __name__ == '__main__':
	main()