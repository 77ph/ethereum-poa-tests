#!/bin/bash
nohup python3 benchmark_tr2_thread_counter.py > benchmark_tr2-1-counter-th.log &
nohup python3 benchmark_tr2_thread_counter.py > benchmark_tr2-2-counter-th.log &
nohup python3 benchmark_tr2_thread_counter.py > benchmark_tr2-3-counter-th.log &
# nohup python3 benchmark_tr2_thread_counter.py > benchmark_tr2-4-counter-th.log &
# nohup python3 benchmark_tr2_thread_counter.py > benchmark_tr2-5-counter-th.log &





