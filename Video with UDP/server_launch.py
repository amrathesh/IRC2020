import os
from multiprocessing import Pool

processes = ('cam1/server1.py --port 10080' , 'cam2/server2.py --port 10081' , 'cam3/server3.py --port 10082')
def run_process(process):
	os.system('sudo python {}'.format(process))

pool = Pool(processes=3)
pool.map(run_process, processes)
