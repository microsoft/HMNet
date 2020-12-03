# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import argparse
import os
import torch
from torch.autograd import Variable
import sys
from Models.Trainers.HMNetTrainer import HMNetTrainer
from Utils.Arguments import Arguments
from Utils.distributed import distributed

# Configurations for training process, task, and model are in the config file.
# Settings for the training environment (cluster, cuda, fp16) are in commandline options

parser = argparse.ArgumentParser(description='HMNet: Pretrain or fine-tune models for HMNet model.')
parser.add_argument('command', help='Command: train/evaluate')
parser.add_argument('conf_file', help='Path to the BigLearn conf file.')
parser.add_argument('--PYLEARN_MODEL', help='Overrides this option from the conf file.')
parser.add_argument('--master_port', help='Overrides this option default', default=None)
parser.add_argument('--cluster', help='local, philly or aml', default='local')
parser.add_argument('--dist_init_path', help='Distributed init path for AML', default='./tmp')
parser.add_argument('--fp16', action='store_true', help="Whether to use 16-bit float precision instead of 32-bit")
parser.add_argument('--fp16_opt_level', type=str, default='O1', help="For fp16: Apex AMP optimization level selected in ['O0', 'O1', 'O2', and 'O3']."
                    "See details at https://nvidia.github.io/apex/amp.html")
parser.add_argument('--no_cuda', action='store_true', help="Disable cuda.")
parser.add_argument('--config_overrides', help='Override parameters on config, VAR=val;VAR=val;...')

cmdline_args = parser.parse_args()
command = cmdline_args.command
conf_file = cmdline_args.conf_file
conf_args = Arguments(conf_file)
opt = conf_args.readArguments()

if cmdline_args.config_overrides:
    for config_override in cmdline_args.config_overrides.split(';'):
        config_override = config_override.strip()
        if config_override:
            var_val = config_override.split('=')
            assert len(var_val) == 2, f"Config override '{var_val}' does not have the form 'VAR=val'"
            conf_args.add_opt(opt, var_val[0], var_val[1], force_override=True)

# print(opt)

opt['cuda'] = torch.cuda.is_available() and not cmdline_args.no_cuda
opt['confFile'] = conf_file
if 'datadir' not in opt:
    opt['datadir'] = os.path.dirname(conf_file)  # conf_file specifies where the data folder is
opt['basename'] = os.path.basename(conf_file)  # conf_file specifies where the name of save folder is
opt['command'] = command

# combine cmdline_args into opt dictionary
for key,val in cmdline_args.__dict__.items():
    # if val is not None and key not in ['command', 'conf_file']:
    if val is not None:
        opt[key] = val

print(opt)

# enable attaching from PDB; use 'kill -10 PID' to enter the debugger
def handle_pdb(sig, frame):
    import pdb
    pdb.Pdb().set_trace(frame)
import signal
signal.signal(signal.SIGUSR1, handle_pdb)

trainer = HMNetTrainer(opt)

print('Select command: ' + command)
if command == "train":
    trainer.train()

elif command == "evaluate":
    trainer.eval()

else:
    assert False, f"Unknown command: {command}"
