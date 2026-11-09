#!/bin/bash
set -e
CUT=$1
echo "merge job for cut $CUT started at $(date) on $(hostname)"
export KRB5CCNAME=FILE:$(pwd)/krb5cc_staged
chmod 600 $(pwd)/krb5cc_staged 2>/dev/null || true
klist 2>/dev/null || true
export EOS_MGM_URL=root://eosuser.cern.ch
cd /afs/cern.ch/user/m/mcortino/private/ANALYSIS/plotsConfigurationsRDF/SSWW/Run3
python /afs/cern.ch/user/m/mcortino/private/ANALYSIS/latinoRDF/scripts/mkMergeYears.py \
    --pycfg /afs/cern.ch/user/m/mcortino/private/ANALYSIS/plotsConfigurationsRDF/SSWW/Run3/merge_configuration.py \
    --cut "$CUT" \
    --output root_file_joined___"$CUT".root \
    --silentMode
echo "done at $(date)"
ls -lh /afs/cern.ch/user/m/mcortino/private/ANALYSIS/plotsConfigurationsRDF/SSWW/Run3/rootFile/SSWW_261026_1030/root_file_joined___"$CUT".root
