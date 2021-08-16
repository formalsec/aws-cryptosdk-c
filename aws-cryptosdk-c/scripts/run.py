#!/usr/bin/env python3
import os
import sys
import csv
import glob
import time
import json
import logging
import resource
import threading
import subprocess

# constants ------------------------------------------------
THREADS=4
TIMEOUT=900
INSTR_MAX=4611686018427387803
ROOT_DIR = '../wasp'

# globals --------------------------------------------------
dirs = glob.glob(f'_build/tests')
table = [['test', 'spec', 'T', 'L', 'S', 'cnt']]
errors = list()

# helpers --------------------------------------------------
cmd  = lambda p : [
    f'./{ROOT_DIR}/wasp', 
    p, 
    '-e', 
    f'(invoke \"{os.path.basename(p).replace(".wat", "")}\")',
    '-m', 
    str(INSTR_MAX)
]

def limit_ram():
    limit = 15 * 1024 * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (limit, limit))

def run(test : str):
    try:
        out = subprocess.check_output(
            cmd(test), 
            timeout=TIMEOUT,
            stderr=subprocess.STDOUT, 
            preexec_fn=limit_ram
        )
    except (subprocess.CalledProcessError, \
            subprocess.TimeoutExpired) as e:
        return None
    return out
#-----------------------------------------------------------

# main -----------------------------------------------------
fmt = '%(asctime)s: %(message)s'
date_fmt = '%H:%M:%S'
logging.basicConfig(format=fmt, level=logging.INFO, \
        datefmt=date_fmt)

def main():
    tests = []
    lock = threading.Lock()

    def run_benchmark(test):
        t0    = time.time()
        out   = run(test)
        delta = time.time() - t0
        
        # Oh no! we crashed!!
        if out is None:
            lock.acquire()
            errors.append(test)
            lock.release()
            logging.info(f'Crashed/Timeout {os.path.basename(test)}')
            return

        report = json.loads(out)
        if not report['specification']:
            lock.acquire()
            errors.append(test)
            lock.release()

        logging.info(f'Test {os.path.basename(test)} ' \
              f'({report["specification"]}, ' \
              f'T={round(delta,2)}s, L={float(report["loop_time"])}, S={float(report["solver_time"])}' \
              f'{report["paths_explored"]})')

        lock.acquire()
        table.append([
            f'{test}',
            report["specification"],
            round(delta, 2),
            float(report["loop_time"]),
            float(report["solver_time"]),
            report["paths_explored"]
        ])
        lock.release()

    def t_loop(i):
        while True:
            try:
                lock.acquire()
                test = tests.pop()
            except IndexError:
                break
            finally:
                lock.release()
            run_benchmark(test)

    for dir in dirs:
        tests = tests + glob.glob(f'{dir}/*.wat')

    threads = []
    for i in range(THREADS):
        t = threading.Thread(target=t_loop, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    
    with open('table.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(table)

    for err in errors:
        logging.info('Failed Test: ' + err)

if __name__ == '__main__':
    main()
#-----------------------------------------------------------
