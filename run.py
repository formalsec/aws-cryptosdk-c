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
THREADS=1
TIMEOUT=900
INSTR_MAX=4000000000000000000

# globals --------------------------------------------------
dirs = glob.glob(f'_build/tests')
table = [['test', 'spec', 'Twasp', 'Tloop', 'Tsolver', 'paths', 'Cov']]
errors = list()

# helpers --------------------------------------------------
cmd  = lambda p, r : [
    'wasp', 
    p, 
    '-e', 
    f'(invoke \"__original_main\")',
    '-b',
    '-m', 
    str(INSTR_MAX),
    '--workspace', r,
    '--smt-assume'
]

def limit_ram() -> None:
    limit = 15 * 1024 * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (limit, limit))

def run(test: str, out_dir: str):
    try:
        out = subprocess.check_output(
            cmd(test, out_dir), 
            timeout=TIMEOUT,
            stderr=subprocess.STDOUT, 
            preexec_fn=limit_ram
        )
    except (subprocess.CalledProcessError, \
            subprocess.TimeoutExpired) as e:
        logging.error('crashed')
        return None
    return out
#-----------------------------------------------------------

# main -----------------------------------------------------
fmt = '%(asctime)s: %(message)s'
date_fmt = '%H:%M:%S'
logging.basicConfig(format=fmt, level=logging.INFO, \
        datefmt=date_fmt)

def main(argv):
    tests = []
    lock = threading.Lock()

    def run_benchmark(test):
        out_dir = os.path.join('output', os.path.basename(test))
        t0    = time.time()
        run(test, out_dir)
        delta = time.time() - t0
        
        report_file = os.path.join(out_dir, 'report.json')
        if not os.path.exists(report_file):
            lock.acquire()
            errors.append(test)
            lock.release()
            logging.info(f'Crashed/Timeout {os.path.basename(test)}')
            return

        
        with open(report_file, 'r') as f:
            try:
                report = json.load(f)
            except json.decoder.JSONDecodeError:
                logging.info(f'Thread {i}: Can not read report \'{report_file}\'.')
                return

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
            report['specification'],
            round(delta, 2),
            float(report['loop_time']),
            float(report['solver_time']),
            report['paths_explored'],
            report['coverage']
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

    if argv == []:
        for dir in dirs:
            tests = tests + glob.glob(f'{dir}/*.wat')
    else:
            tests = argv

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
    main(sys.argv[1:])
#-----------------------------------------------------------
