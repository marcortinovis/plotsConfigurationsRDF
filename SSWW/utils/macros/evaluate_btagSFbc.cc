#ifndef BTAGSF
#define BTAGSF

#include <vector>
#include <map>
#include <string>
#include <iostream>
#include <algorithm>
#include <atomic>
#include <cmath>
#include "TVector2.h"
#include "Math/Vector4Dfwd.h"
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"
#include "TString.h"

#include "ROOT/RVec.hxx"
#include "TH2D.h"
#include "TFile.h"
#include "correction.h"
#include <memory>

using namespace ROOT;
using namespace ROOT::VecOps;
using correction::CorrectionSet;

// Shared by all btag functors: limits diagnostic output to the first few events.
inline bool btagSF_shouldWarn() {
    static std::atomic<int> nWarn{0};
    return nWarn++ < 20;
}

// --- BTag SF class ---
class btagSFbc {

  public:
    btagSFbc(TString eff_map, const std::string corr_year, const std::string WP,
            const std::string shift, const std::string tagger,
            const std::string eff_map_year);

    std::shared_ptr<TH2F> h_bjet_eff;
    std::shared_ptr<TH2F> h_cjet_eff;

    // shared_ptr rather than unique_ptr: RDataFrame's typed Define() takes the
    // callable by value, so this class must stay copyable. Copies share the
    // efficiency maps and the CorrectionSet instead of reloading them.
    std::shared_ptr<CorrectionSet> cset;

    // fixed per instance — one instance per (WP, shift) variation
    std::string WP_;
    std::string shift_;
    std::string eff_map_year_;

    // resolved once in the constructor instead of on every event
    correction::Correction::Ref cset_btag_comb_;
    correction::Correction::Ref cset_btag_wps_;
    double wp_value_ = 0.;   // WP threshold, event-independent

    float operator()(
        RVecF CleanJet_pt,
        RVecF CleanJet_eta,
        RVec<ULong64_t> CleanJet_jetIdx,
        unsigned int nCleanJet,
        RVecI Jet_hadronFlavour,
        RVecF Jet_btag
      )
    {
        // Never trust nCleanJet alone: in varied universes it can disagree with
        // the (varied) CleanJet_* vector sizes.
        const size_t n = std::min<size_t>({ (size_t)nCleanJet,
                                            CleanJet_pt.size(),
                                            CleanJet_eta.size(),
                                            CleanJet_jetIdx.size() });
        if (n != (size_t)nCleanJet && btagSF_shouldWarn())
            std::cerr << "[btagSFbc] size mismatch: nCleanJet=" << nCleanJet
                      << " pt=" << CleanJet_pt.size()
                      << " eta=" << CleanJet_eta.size()
                      << " idx=" << CleanJet_jetIdx.size() << std::endl;

        const bool useCharm = (eff_map_year_ != "None");
        float btag_sf = 1.f;

        for (size_t iJ = 0; iJ < n; ++iJ)
        {
          const double pt  = CleanJet_pt[iJ];
          const double aeta = std::abs(CleanJet_eta[iJ]);
          if (pt <= 20. || aeta >= 2.5) continue;

          const ULong64_t idx = CleanJet_jetIdx[iJ];
          if (idx >= (ULong64_t)Jet_btag.size() || idx >= (ULong64_t)Jet_hadronFlavour.size()) {
              if (btagSF_shouldWarn())
                  std::cerr << "[btagSFbc] bad jetIdx " << idx
                            << " (nJet btag=" << Jet_btag.size()
                            << ", flav=" << Jet_hadronFlavour.size() << ")" << std::endl;
              continue;
          }

          const int flav = Jet_hadronFlavour[idx];
          if (flav != 5 && !(flav == 4 && useCharm)) continue;   // only b (and c) jets

          const double sf = cset_btag_comb_->evaluate({shift_, WP_, flav, aeta, pt});

          if (Jet_btag[idx] > wp_value_)
          {
            btag_sf *= sf;
          }
          else
          {
            const float btag_eff = getEff(pt, CleanJet_eta[iJ], flav);
            if (btag_eff == 1.f) continue;
            btag_sf *= (1. - btag_eff * sf) / (1. - btag_eff);
          }
        }
        return btag_sf;
    }

  private:
    float getEff(float pt, float eta, int flavour);

};

inline btagSFbc::btagSFbc(TString eff_map, const std::string corr_year, const std::string WP,
                  const std::string shift, const std::string tagger,
                  const std::string eff_map_year)
  : WP_(WP), shift_(shift), eff_map_year_(eff_map_year) {

  if (corr_year == "None")
    {
        cset = CorrectionSet::from_file("/cvmfs/cms-griddata.cern.ch/cat/metadata/BTV/" + corr_year + "/latest/btagging_preliminary.json.gz");
    }
    else
    {
       cset = CorrectionSet::from_file("/cvmfs/cms-griddata.cern.ch/cat/metadata/BTV/" + corr_year + "/latest/btagging.json.gz");
    }

  // resolved here, once per job, rather than per event in operator()
  if (eff_map_year_ == "None")
    cset_btag_comb_ = cset->at(tagger + "_kinfit");
  else
    cset_btag_comb_ = cset->at(tagger + "_comb");
  cset_btag_wps_ = cset->at(tagger + "_wp_values");
  wp_value_ = cset_btag_wps_->evaluate({WP_});

  TFile *reff = TFile::Open(eff_map, "READ");
  if (!reff || reff->IsZombie()) {
      std::cerr << "Error opening file " << eff_map << std::endl;
      return;
  }

  if (auto* _h = dynamic_cast<TH2F*>(reff->Get("bjet_eff"))) {
    auto* _clone = static_cast<TH2F*>(_h->Clone());
    _clone->SetDirectory(nullptr);
    h_bjet_eff.reset(_clone);
  } else {
    std::cerr << "[btagSFbc] 'bjet_eff' missing or not a TH2F in " << eff_map << std::endl;
  }
  if (auto* _h = dynamic_cast<TH2F*>(reff->Get("cjet_eff"))) {
    auto* _clone = static_cast<TH2F*>(_h->Clone());
    _clone->SetDirectory(nullptr);
    h_cjet_eff.reset(_clone);
  }
  reff->Close();
}

inline float btagSFbc::getEff(float pt, float eta, int flavour) {
  float eff = 1.;
  if (flavour == 5) {
    if (!h_bjet_eff) return 1.0;   // was an unchecked dereference
    const int xbin = h_bjet_eff->GetXaxis()->FindBin(pt);
    const int ybin = h_bjet_eff->GetYaxis()->FindBin(eta);
    eff  = h_bjet_eff->GetBinContent(xbin, ybin);
  }
  else if (flavour == 4) {
    if (!h_cjet_eff) return 1.0;
    const int xbin = h_cjet_eff->GetXaxis()->FindBin(pt);
    const int ybin = h_cjet_eff->GetYaxis()->FindBin(eta);
    eff  = h_cjet_eff->GetBinContent(xbin, ybin);
  }
  return eff;
}

#endif