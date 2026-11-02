#!/bin/bash
set -e
echo "Job started at $(date)"
echo "Running on node $(hostname)"
cd /afs/cern.ch/user/m/mcortino/private/ANALYSIS/plotsConfigurationsRDF/SSWW/2023
make WW_DPS
