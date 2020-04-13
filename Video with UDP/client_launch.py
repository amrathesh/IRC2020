import os
from multiprocessing import Pool

'''
os.system('python client1.py --host 192.168.1.33 --port 10080')

os.system('python client2.py --host 192.168.1.33 --port 10081')

os.system('python client3.py --host 192.168.1.33 --port 10082')
'''


processes = ('cam1/client1.py --host 192.168.1.33 --port 10080' , 'cam2/client2.py --host 192.168.1.33 --port 10081' , 'cam3/client3.py --host 192.168.1.33 --port 10082')
def run_process(process):
	os.system('python {}'.format(process))

pool = Pool(processes=3)
pool.map(run_process, processes)
