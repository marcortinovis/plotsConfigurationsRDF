#ifndef NLOSIGSF
#define NLOSIGSF

#include <iostream>

#include "TH1.h"
#include "TFile.h"
#include <memory>

using namespace ROOT;


class NLOsignalSF {

    public:
        NLOsignalSF(TString sourceHisto, const std::string histoBase, const std::string shift);

        std::shared_ptr<TH1> h_nlosig_eff;

        float operator()(float mjj) {
            float nlosig_eff = getEff(mjj);
            return nlosig_eff;
        }

    private:
        float getEff(float mjj);

};

NLOsignalSF::NLOsignalSF(TString sourceHisto, const std::string histoBase, const std::string shift) {

    TFile *shisto = TFile::Open(sourceHisto, "READ");
    if (!shisto || shisto->IsZombie()) {
        std::cerr << "Error opening file " << sourceHisto << std::endl;
        return;
    }

    const std::string hname = histoBase + shift;
    if (auto* _h = dynamic_cast<TH1*>(shisto->Get(hname.c_str()))) {
        if (_h->GetDimension() != 1)
            throw std::runtime_error("NLOsignalSF: expected a 1D histogram");
        auto* _clone = static_cast<TH1*>(_h->Clone());
        _clone->SetDirectory(nullptr);
        h_nlosig_eff.reset(_clone);
    }
    shisto->Close();

}

float NLOsignalSF::getEff(float mjj) {
    // clamp between [1, N] ?
    const int nBins = h_nlosig_eff->GetNbinsX();
    int bin = h_nlosig_eff->GetXaxis()->FindFixBin(mjj);
    bin = std::max(1, std::min(bin, nBins));
    return static_cast<float>(h_nlosig_eff->GetBinContent(bin));
    /// if you don't want clamping: return static_cast<float>(h_nlosig_eff->GetBinContent(h_nlosig_eff->FindBin(mjj)));
}


#endif