### mcortino: TOBE CHECKED !



ALL = [skey for skey in samples]
mc = [skey for skey in samples if skey not in ('DATA', 'Fake')]
lhesamples = [skey for skey in mc if skey not in ('ggWW', 'ZZ', 'WW_DPS')] ### mcortino: added WW_DPS, as in branch DNN, https://github.com/acmbulla/plotsConfigurationsRDF/blob/DNNTraining/SSWW/2024/nuisances.py


mcProductions = {
    '2022':         'Summer22_130x_nAODv12_Full2022v12',
    '2022EE':       'Summer22EE_130x_nAODv12_Full2022v12',
    '2023':         'Summer23_130x_nAODv12_Full2023v12',
    '2023BPix':     'Summer23BPix_130x_nAODv12_Full2023BPixv12',
    '2024':         'Summer24_150x_nAODv15_Full2024v15'
}
mcStepss = {
    '2022':         'MCl2loose2022v12__MCCorr2022v12JetScaling__l2tight',
    '2022EE':       'MCl2loose2022EEv12__MCCorr2022EEv12JetScaling__l2tight',
    '2023':         'MCl2loose2023v12__MCCorr2023v12JetScaling__l2tight',
    '2023BPix':     'MCl2loose2023BPixv12__MCCorr2023BPixv12JetScaling__l2tight',
    '2024':         'MCl2loose2024v15__MCCorr2024v15__JERFrom23BPix__l2tight'
}

def makeMCDirectory(var='', year=''):
    _treeBaseDir = treeBaseDir + ''
    mcProduction = mcProductions[year]
    mcSteps = mcStepss[year]
    if useXROOTD:
        _treeBaseDir = redirector + treeBaseDir
    if var== '':
        return '/'.join([_treeBaseDir, mcProduction, mcSteps])
    else:
        return '/'.join([_treeBaseDir, mcProduction, mcSteps + '__' + var])

treeBaseDir = '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano'

useXROOTD = True
redirector = 'root://eoscms.cern.ch/'

# merge cuts
_mergedCuts = []
for cut in list(cuts.keys()):
    __cutExpr = ''
    if type(cuts[cut]) == dict:
        __cutExpr = cuts[cut]['expr']
        for cat in list(cuts[cut].get('categories', {}).keys()):
            _mergedCuts.append(cut + '_' + cat)
    elif type(cuts[cut]) == str:
        _mergedCuts.append(cut)

cuts2j = _mergedCuts




years = ['2022', '2022EE', '2023', '2023BPix', '2024'] ## '2025', '2026']

for y in years:
    nuisances[f'JER_{y}'] = {
        'name': f'CMS_res_j_{y}',
        'skipCMS' : 1,
        'kind': 'suffix',
        'type': 'shape',
        'mapUp': 'jerup',
        'mapDown': 'jerdo',
        #'separator': '__',
        'samples': dict((skey, ['1', '1']) for skey in mc),
        'folderUp': makeMCDirectory('jerup_suffix', y),
        'folderDown': makeMCDirectory('jerdo_suffix', y),
        'AsLnN': '0'
    }

for y in years: # yes i know, rewriting the non year specific nuisances
    jes_sources = [f'Absolute_{y}', 'Absolute', f'BBEC1_{y}','BBEC1', f'EC2_{y}','EC2','FlavorQCD', f'HF_{y}','HF','RelativeBal', f'RelativeSample_{y}']
    jes_sources = ["jesRegroed_"+ _ for _ in jes_sources] 
    for js in jes_sources:
        nuisances[js] = {
            'name': f'CMS_scale_{js}',
            'skipCMS' : 1,
            'kind': 'suffix',
            'type': 'shape',
            'mapUp': f'{js}up',
            'mapDown': f'{js}do',
            #'separator': '__',
            'samples': dict((skey, ['1', '1']) for skey in mc),
            'folderUp': makeMCDirectory(f'{js}up_suffix', y),
            'folderDown': makeMCDirectory(f'{js}do_suffix', y),
            'AsLnN': '0'
        }

# #BUGGED FIXME TODO
# '''
# for y in years:
    # nuisances[f'MET_{y}'] = {
    #     'name': f'CMS_scale_met_{y}',
    #     'skipCMS' : 1,
    #     'kind': 'suffix',
    #     'type': 'shape',
    #     'mapUp': 'unclustEnup',
    #     'mapDown': 'unclustEndo',
    #     #'separator': '__',
    #     'samples': dict((skey, ['1', '1']) for skey in mc),
    #     'folderUp': makeMCDirectory('unclustEnup_suffix'),
    #     'folderDown': makeMCDirectory('unclustEndo_suffix'),
    #     'AsLnN': '0'
    # }
# '''

##### Lepton scale
for y in years:
    nuisances[f'lepscale_{y}'] = {
        'name': f'CMS_lepscale_{y}',
        'skipCMS' : 1,
        'kind': 'suffix',
        'type': 'shape',
        'mapUp': 'leptonScaleup',
        'mapDown': 'leptonScaledo',
        #'separator': '__',
        'samples': dict((skey, ['1', '1']) for skey in mc),
        'folderUp': makeMCDirectory('leptonScaleup_suffix', y),
        'folderDown': makeMCDirectory('leptonScaledo_suffix', y),
        'AsLnN': '0'
    }

##### Lepton resolution
for y in years:
    nuisances[f'lepres_{y}'] = {
        'name': f'CMS_lepres_{y}',
        'skipCMS' : 1,
        'kind': 'suffix',
        'type': 'shape',
        'mapUp': 'leptonResolutionup',
        'mapDown': 'leptonResolutiondo',
        #'separator': '__',
        'samples': dict((skey, ['1', '1']) for skey in mc),
        'folderUp': makeMCDirectory('leptonResolutionup_suffix', y),
        'folderDown': makeMCDirectory('leptonResolutiondo_suffix', y),
        'AsLnN': '0'
    }

# # # ## B-tagger
# # # Fixed BTV SF variations
nuisance_sources = {
    'bc': ['bfragmentation', 'fsrdef', 'hdamp', 'isrdef', 'jer', 'jes', 'muf', 'mur', 'pdfas', 'pileup', 'statistic', 'topmass', 'type3'],   
    'light': [ 'correlated', 'uncorrelated'],
}

for y in years:
    for flavour in ['bc', 'light']:
        for corr in ['uncorrelated', 'correlated']:
            btag_syst = [f'btagSF{flavour}_up_{corr}/btagSF{flavour}', f'btagSF{flavour}_down_{corr}/btagSF{flavour}']
            if corr == 'correlated':
                name = f'CMS_btagSF{flavour}_{corr}'
            else:
                name = f'CMS_btagSF{flavour}_{y}'
            nuisances[f'btagSF{flavour}{corr}'+(f'_{y}' if corr!='correlated' else '')] = {
                'name': name,
                'skipCMS' : 1,
                'kind': 'weight',
                'type': 'shape',
                'samples': dict((skey, btag_syst) for skey in mc),
            }


# ##### Trigger Scale Factors                                                                                                                                                                                

trig_syst = ['TriggerSFWeight_2l_u/TriggerSFWeight_2l', 'TriggerSFWeight_2l_d/TriggerSFWeight_2l']

for y in years:
    nuisances[f'trigg_{y}'] = {
        'name': f'CMS_eff_hwwtrigger_{y}',
        'kind': 'weight',
        'type': 'shape',
        'samples': dict((skey, trig_syst) for skey in mc)
    }

##### Electron Efficiency 

for y in years:
    nuisances[f'eff_e_{y}'] = {
        'name': f'CMS_eff_e_{y}',
        'kind': 'weight',
        'type': 'shape',
        'samples': dict((skey, ['SFweightEleUp', 'SFweightEleDown']) for skey in mc), #TODO: IN THIS SAMPLES THERE'S AN ERROR AND SFUP AND SFDO ARE THE SAME, NEEDS TO BE FIXED
    }

##### Muon Efficiency 

for y in years:
    nuisances[f'eff_m_{y}'] = {
        'name': f'CMS_eff_m_{y}',
        'kind': 'weight',
        'type': 'shape',
        'samples': dict((skey, ['SFweightMuUp', 'SFweightMuDown']) for skey in mc),
    }


for y in years:
    nuisances[f'PU_{y}'] = {
        'name'    : f'CMS_pileup_{y}',
        'type'    : 'lnN',
        'samples' : dict((skey, '1.05') for skey in mc),
    }

##### PS

nuisances['PS_ISR']  = {
    'name'    : 'ps_isr',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : dict((skey, ['PSWeight[2]', 'PSWeight[0]']) for skey in mc),
    'AsLnN'   : '0',
}

nuisances['PS_FSR']  = {
    'name'    : 'ps_fsr',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : dict((skey, ['PSWeight[3]', 'PSWeight[1]']) for skey in mc),
    'AsLnN'   : '0',
}

nuisances['UE_CP5']  = {
    'name'    : 'UEPS',
    'skipCMS' : 1,
    'type'    : 'lnN',
    'samples' : dict((skey, '1.015') for skey in mc),
}


# ## QCD scale uncertainties - RDataFrame syntax (no Alt())
# ## Works for samples with either 8 or 9 LHE scale weights

_lhe_up   = '(LHEScaleWeight_vec.size() > 0 ? LHEScaleWeight_vec[0] : 1.)'
_lhe_down = '(LHEScaleWeight_vec.size() > 0 ? LHEScaleWeight_vec[LHEScaleWeight_vec.size()-1] : 1.)'

_qcdScaleGroups = {
    # --- signal: same-sign WW
    # WW_EWK and the three polarisation samples are the same process (the
    # polarised ones are its decomposition), so one correlated parameter.
    # the inclusive VBS_SSWW is commented out in samples.py (it double counts
    # WW_EWK + WW_QCD + WW_Int); add it back here if it is ever re-enabled.
    'QCDscale_VBS_SSWW' : ['WW_EWK'], # 'VBS_SSWW','VBS_SSWW_WWCM_LL', 'VBS_SSWW_WWCM_TL', 'VBS_SSWW_WWCM_TT'],
    'QCDscale_SSWW_QCD' : ['WW_QCD', 'WW_Int'],

    # --- WZ, split EWK / QCD exactly as groupPlot does in plot.py
    'QCDscale_WZ_EWK'   : ['WZJJ_EWK', 'WZSJJ_EWK'],
    'QCDscale_WZ'       : ['WZJJ_QCD', 'WZSJJ_QCD', 'WZJJ_Int'],

    # --- top
    'QCDscale_ttbar'    : ['top'],
    'QCDscale_tVx'      : ['tVx'],

    # --- wrong-sign / charge-mismeasurement sources (groupPlot 'Wrong sign')
    'QCDscale_DY'       : ['DY'],
    'QCDscale_OSWW'     : ['OSWW'],

    # --- remaining diboson / triboson (groupPlot 'VV(V)')
    # name kept as QCDscale_VV so the datacards do not change parameter name
    'QCDscale_VV'       : ['Wg', 'Zg', 'WgS', 'ZgS'],
    'QCDscale_VVV'      : ['VVV'],

    # --- Higgs
    'QCDscale_ggH'      : ['ggH_hww'],
    'QCDscale_qqH'      : ['qqH_hww'],
    'QCDscale_higgs'    : ['higgs'],
}

for _nuis, _slist in _qcdScaleGroups.items():
    nuisances[_nuis] = {
        'name'    : _nuis,
        'kind'    : 'weight',
        'type'    : 'shape',
        'samples' : {s: [_lhe_up, _lhe_down] for s in _slist}
    }

# coherence check: every LHE sample covered once, and no group naming a sample
# that samples.py does not define.
_qcdScaleFlat    = [s for _l in _qcdScaleGroups.values() for s in _l]
_qcdScaleUnknown = sorted(set(_qcdScaleFlat) - set(samples))
_qcdScaleDup     = sorted(s for s in set(_qcdScaleFlat) if _qcdScaleFlat.count(s) > 1)
_qcdScaleMissing = sorted(set(lhesamples) - set(_qcdScaleFlat))
if _qcdScaleUnknown or _qcdScaleDup or _qcdScaleMissing:
    raise ValueError(
        'QCD scale nuisances out of sync with samples.py:'
        + (f' unknown samples {_qcdScaleUnknown};' if _qcdScaleUnknown else '')
        + (f' sample in two groups {_qcdScaleDup};' if _qcdScaleDup else '')
        + (f' LHE samples with no scale nuisance {_qcdScaleMissing};' if _qcdScaleMissing else '')
    )

# ## PDF uncertainties - RDataFrame syntax (no Alt())
for i in range(103):
    _pdf_w = f'(LHEPdfWeight_vec.size() > {i} ? LHEPdfWeight_vec[{i}] : 1.)'
    nuisances[f'pdf_ev{i}'] = {
        'name'    : f'pdf_ev{i}',
        'kind'    : 'weight',
        'type'    : 'shape',
        'samples' : {s: [_pdf_w, _pdf_w] for s in lhesamples}
    }


nuisances['fake_syst'] = {
    'name': 'CMS_fake_syst',
    'type': 'lnN',
    'samples': {
        'Fake': '1.3'
    },
}


for y in years:
    nuisances[f'fake_ele_{y}'] = {
        'name': f'CMS_fake_e_{y}',
        'skipCMS' : 1,
        'kind': 'weight',
        'type': 'shape',
        'samples': {
            'Fake': ['fakeWEleUp', 'fakeWEleDown'],
        }
    }

for y in years:
    nuisances[f'fake_ele_stat_{y}'] = {
        'name': f'CMS_fake_stat_e_{y}',
        'skipCMS' : 1,
        'kind': 'weight',
        'type': 'shape',
        'samples': {
            'Fake': ['fakeWStatEleUp', 'fakeWStatEleDown'],
        }
    }

for y in years:
    nuisances[f'fake_mu_{y}'] = {
        'name': f'CMS_fake_m_{y}',
        'skipCMS' : 1,
        'kind': 'weight',
        'type': 'shape',
        'samples': {
            'Fake': ['fakeWMuUp', 'fakeWMuDown'],
        }
    }

for y in years:
    nuisances[f'fake_mu_stat_{y}'] = {
        'name': f'CMS_fake_stat_m_{y}',
        'skipCMS' : 1,
        'kind': 'weight',
        'type': 'shape',
        'samples': {
            'Fake': ['fakeWStatMuUp', 'fakeWStatMuDown'],
        }
    }

autoStats = True
if autoStats:
    ## Use the following if you want to apply the automatic combine MC stat nuisances.
    nuisances['stat'] = {
        'type': 'auto',
        'maxPoiss': '10',
        'includeSignal': '0',
        #  nuisance ['maxPoiss'] =  Number of threshold events for Poisson modelling
        #  nuisance ['includeSignal'] =  Include MC stat nuisances on signal processes (1=True, 0=False)
        'samples': {}
    }

nuisances['DYttnorm2j']  = {
               'name'  : 'CMS_hww_DYttnorm2j',
               'skipCMS' : 1,
               'samples'  : {
                   'DY' : '1.00',
                   },
               'type'  : 'rateParam',
               'cuts'  : cuts2j
              }

nuisances['WWnorm2j']  = {
               'name'  : 'CMS_hww_WWnorm2j',
               'skipCMS' : 1,
               'samples'  : {
                   'WW_QCD' : '1.00', # 'WWjj_QCD' was 'WW_QCD', is it right?
                   },
               'type'  : 'rateParam',
               'cuts'  : cuts2j
              }

nuisances['ggWWnorm2j']  = {
               'name'  : 'CMS_hww_WWnorm2j',
               'skipCMS' : 1,
               'samples'  : {
                   'ggWW' : '1.00',
                   },
               'type'  : 'rateParam',
               'cuts'  : cuts2j
              }

nuisances['Topnorm2j']  = {
               'name'  : 'CMS_hww_Topnorm2j',
               'skipCMS' : 1,
               'samples'  : {
                   'top' : '1.00',
                   },
               'type'  : 'rateParam',
               'cuts'  : cuts2j
              }


nuisances['QCDscale_CRSR_accept_dytt']  = {
               'name'  : 'QCDscale_CRSR_accept_dytt',
               'type'  : 'lnN',
               'samples'  : {
                   'DY' : '1.02',
                   },
               'cuts'  : [
                 'hww2l2v_13TeV_dytt_of0j',
                 'hww2l2v_13TeV_dytt_of1j',
                 'hww2l2v_13TeV_dytt_of2j',
                 'hww2l2v_13TeV_dytt_of2j_vbf',
                 'hww2l2v_13TeV_dytt_of2j_vh2j'
                ]
              }