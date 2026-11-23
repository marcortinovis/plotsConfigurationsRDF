import ROOT, glob, os, re, collections
ROOT.gErrorIgnoreLevel = ROOT.kError

folder = "snapshots/261113_0915"          # folder_where_to_save_trees
files  = sorted(glob.glob(f"{folder}/nanoLatino_snapshot____*.root"))

def tag(f):                                   # sample_subname, without the job index
    m = re.search(r'____(.+)_(\d+)\.root$', os.path.basename(f))
    return m.group(1) if m else None          # None -> shape-nuisance file / orphan

branches = {}                                 # file -> set of branch names
skipped  = 0
for f in files:
    if tag(f) is None:
        continue
    tf = ROOT.TFile.Open(f)
    t  = tf.Get("Events") if tf and not tf.IsZombie() else None
    if not t or t.GetEntries() == 0:          # unreadable or empty: haddnano skips empty ones
        skipped += 1
        if tf: tf.Close()
        continue
    branches[f] = {b.GetName() for b in t.GetListOfBranches()}
    tf.Close()

allbr = set().union(*branches.values())
print(f"{len(branches)} files checked ({skipped} skipped: unreadable or empty)")

n_missing = 0
for br in sorted(allbr):
    lacking = [f for f, s in branches.items() if br not in s]
    if lacking:
        n_missing += 1
        tags = sorted({tag(f) for f in lacking})
        print(f"\n{br}: missing in {len(lacking)}/{len(branches)} files, {len(tags)} samples")
        for t_ in tags:
            print(f"   {t_}")

if n_missing == 0:
    print("No missing branches: all files have the same set.")