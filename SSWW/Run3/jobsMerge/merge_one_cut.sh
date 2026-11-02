#!/bin/bash
set -e
CUT=$1
echo "merge job for cut $CUT started at $(date) on $(hostname)"
cd /afs/cern.ch/user/m/mcortino/private/ANALYSIS/plotsConfigurationsRDF/SSWW/Run3
python /afs/cern.ch/user/m/mcortino/private/ANALYSIS/latinoRDF/scripts/mkMergeYears.py \
    --pycfg /afs/cern.ch/user/m/mcortino/private/ANALYSIS/plotsConfigurationsRDF/SSWW/Run3/merge_configuration.py \
    --cut "$CUT" \
    --output root_file_joined___"$CUT".root \
    --silentMode
echo "done at $(date)"
ls -lh /afs/cern.ch/user/m/mcortino/private/ANALYSIS/plotsConfigurationsRDF/SSWW/Run3/rootFile/SSWW_261026_1030/root_file_joined___"$CUT".root
