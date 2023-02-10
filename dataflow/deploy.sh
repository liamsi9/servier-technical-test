#!/usr/bin/env bash

python -m pipeline --runner=DataflowRunner --worker_machine_type n1-standard-1 --max_num_workers 1