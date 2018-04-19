// -*- C++ -*-
//
// Package:    CMSDAS2015/BTaggingExercise
// Class:      BTaggingExerciseII
// 
/**\class BTaggingExerciseII BTaggingExerciseII.cc CMSDAS2015/BTaggingExercise/plugins/BTaggingExerciseII.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Dinko Ferencek
//         Created:  Tue, 16 Dec 2014 00:09:47 GMT
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/PatCandidates/interface/Jet.h"

#include "TH2F.h"

#include <boost/algorithm/string.hpp>

//
// class declaration
//

class BTaggingExerciseII : public edm::EDAnalyzer {
   public:
      explicit BTaggingExerciseII(const edm::ParameterSet&);
      ~BTaggingExerciseII();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      //virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
      //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;

      // ----------member data ---------------------------
//      const edm::EDGetTokenT<std::vector<pat::Jet> > jets_;
      const edm::EDGetTokenT<std::vector<pat::Jet> > jetsak8_;
      const std::vector<std::string> bDiscriminators_;

      edm::Service<TFileService> fs;

      // declare a map of b-tag discriminator histograms
      std::map<std::string, TH2F *> bDiscriminatorsMap;
      std::map<std::string, TH2F *> bDiscriminatorsMap_sjBDiscMin;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
BTaggingExerciseII::BTaggingExerciseII(const edm::ParameterSet& iConfig) :

//  jets_(consumes<std::vector<pat::Jet> >(iConfig.getParameter<edm::InputTag>("jets"))),
  jetsak8_(consumes<std::vector<pat::Jet> >(iConfig.getParameter<edm::InputTag>("jetsak8"))),
  bDiscriminators_(iConfig.getParameter<std::vector<std::string> >("bDiscriminators"))

{
   std::string bDiscr_flav = "";
   // initialize b-tag discriminator histograms
   for( const std::string &bDiscr : bDiscriminators_ )
   {
     for( const std::string &flav : {"b","c","udsg"} )
     {
       bDiscr_flav = bDiscr + "_" + flav;
       if( bDiscr.find("Counting") != std::string::npos ) // track counting discriminator can be both positive and negative and covers a wider range then other discriminators
         bDiscriminatorsMap[bDiscr_flav] = fs->make<TH2F>(bDiscr_flav.c_str(), (bDiscr_flav + ";Jet p_{T} [GeV];b-tag discriminator").c_str(), 100, 0, 1000, 11000, -15, 40);
       else if ( bDiscr.find("probbb") != std::string::npos || bDiscr.find("probb") != std::string::npos ) {
         bDiscr_flav = std::string("pfDeepCSVJetTagsProbB") + "_" + flav;
         if ( bDiscriminatorsMap.find(bDiscr_flav) == bDiscriminatorsMap.end() ) 
           bDiscriminatorsMap[bDiscr_flav] = fs->make<TH2F>(bDiscr_flav.c_str(), (bDiscr_flav + ";Jet p_{T} [GeV];b-tag discriminator").c_str(), 100, 0, 1000, 4400, -11, 11);
       }
       else 
         bDiscriminatorsMap[bDiscr_flav] = fs->make<TH2F>(bDiscr_flav.c_str(), (bDiscr_flav + ";Jet p_{T} [GeV];b-tag discriminator").c_str(), 100, 0, 1000, 4400, -11, 11);

       bDiscr_flav = bDiscr + "_" + flav + "_";
       if( bDiscr.find("Counting") != std::string::npos ) // track counting discriminator can be both positive and negative and covers a wider range then other discriminators                                                     
	   bDiscriminatorsMap_sjBDiscMin[bDiscr_flav] = fs->make<TH2F>(bDiscr_flav.c_str(), (bDiscr_flav + ";Jet p_{T} [GeV];b-tag discriminator").c_str(), 100, 0, 1000, 11000, -15, 40);
	 else if ( bDiscr.find("probbb") != std::string::npos || bDiscr.find("probb") != std::string::npos ) {
	   bDiscr_flav = std::string("pfDeepCSVJetTagsProbb") + "_" + flav ;
	   if ( bDiscriminatorsMap_sjBDiscMin.find(bDiscr_flav) == bDiscriminatorsMap_sjBDiscMin.end() )
	     bDiscriminatorsMap_sjBDiscMin[bDiscr_flav] = fs->make<TH2F>(bDiscr_flav.c_str(), (bDiscr_flav + ";Jet p_{T} [GeV];b-tag discriminator").c_str(), 100, 0, 1000, 4400, -11, 11);
	 }
	 else
	  bDiscriminatorsMap_sjBDiscMin[bDiscr_flav] = fs->make<TH2F>(bDiscr_flav.c_str(), (bDiscr_flav + ";Jet p_{T} [GeV];b-tag discriminator").c_str(), 100, 0, 1000, 4400, -11, 11);
       }

   }
}




BTaggingExerciseII::~BTaggingExerciseII()
{

  // do anything here that needs to be done at desctruction time
  // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
  void
BTaggingExerciseII::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  // define a jet handle
//  edm::Handle<std::vector<pat::Jet> > jets;
  // get jets from the event
  //iEvent.getByToken(jets_, jets);

  // define a jet handle
  edm::Handle<std::vector<pat::Jet> > h_jetsak8;
  // get jets from the event
  iEvent.getByToken(jetsak8_, h_jetsak8);
  
  std::string bDiscr_flav = "";
 //loop over AK8 jets
for( auto jetak8 = h_jetsak8->begin(); jetak8 != h_jetsak8->end(); ++jetak8 ){
  if(jetak8->mass() < 80 && jetak8->mass() > 160) continue;
  if(jetak8->pt() < 750  && jetak8->pt() > 1150) continue; 
  if(std::abs(jetak8->eta()) > 1.5 ) continue; 
  std::vector<edm::Ptr<pat::Jet> > const& jets = jetak8->subjets("SoftDropPuppi") ;
  // loop over jets
  int n = jets.size();
 //for( auto jet = jets.begin(); jet != jets.end(); ++jet )
  for(int i=0 ; i < n ; i++)
  {
    int flavor = std::abs( jets.at(i)->hadronFlavour() );
    // fill discriminator histograms
    for( const std::string &bDiscr : bDiscriminators_ )
    {
     
      if( flavor==5 ) // b jet
        bDiscr_flav = bDiscr + "_b";
      else if( flavor==4 ) // c jets
        bDiscr_flav = bDiscr + "_c";
      else // light-flavor jet
        bDiscr_flav = bDiscr + "_udsg";

      if ( bDiscr.find("probbb") != std::string::npos ) continue; //// We will sum the DeepCSV::probbb and DeepCSV::probb together
      if ( bDiscr.find("probb") != std::string::npos ) {
        boost::replace_all(bDiscr_flav, bDiscr, "pfDeepCSVJetTagsProbB") ; 
        bDiscriminatorsMap[bDiscr_flav]->Fill( jets.at(i)->pt(), jets.at(i)->bDiscriminator("pfDeepCSVJetTags:probb") + jets.at(i)->bDiscriminator("pfDeepCSVJetTags:probbb") );
      }
      else bDiscriminatorsMap[bDiscr_flav]->Fill( jets.at(i)->pt(), jets.at(i)->bDiscriminator(bDiscr) );

    }
  }
    if (n<2) continue;
      int flavor0 = std::abs( jets.at(0)->hadronFlavour() );
      int flavor1 = std::abs( jets.at(1)->hadronFlavour() );
      double bdisc_0 = jets.at(0)->bDiscriminator("pfDeepCSVJetTags:probb") + jets.at(0)->bDiscriminator("pfDeepCSVJetTags:probbb");
      double bdisc_1 = jets.at(1)->bDiscriminator("pfDeepCSVJetTags:probb") + jets.at(1)->bDiscriminator("pfDeepCSVJetTags:probbb");
  // fill discriminator histograms
                                                                              
      for( const std::string &bDiscr : bDiscriminators_ )
	{

	  if( flavor0==5 && flavor1==5 ) // b jet                                                                                    
	    bDiscr_flav = bDiscr + "_b";
	  else if( flavor0==4 && flavor1==4  ) // c jets                                                                              
	    bDiscr_flav = bDiscr + "_c";
	  else // light-flavor jet                                                                               

	    bDiscr_flav = bDiscr + "_udsg";

	  if ( bDiscr.find("probbb") != std::string::npos ) continue; //// We will sum the DeepCSV::probbb and DeepCSV::probb together                                                                                                 
	    if ( bDiscr.find("probb") != std::string::npos ) {
	      boost::replace_all(bDiscr_flav, bDiscr, "pfDeepCSVJetTagsProbb") ;
	     
	      if ( bdisc_0 <  bdisc_1)
	      bDiscriminatorsMap_sjBDiscMin[bDiscr_flav]->Fill(jets.at(0)->pt(), bdisc_0 );
	      else
		bDiscriminatorsMap_sjBDiscMin[bDiscr_flav]->Fill(jets.at(1)->pt(), bdisc_1 );
       }
	    //	    else bDiscriminatorsMap_sjBDiscMin[bDiscr_flav]->Fill( jets.at(i)->pt(), jets.at(i)->bDiscriminator(bDiscr) );

	
    }
 }


}


// ------------ method called once each job just before starting event loop  ------------
  void 
BTaggingExerciseII::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
  void 
BTaggingExerciseII::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
/*
   void 
   BTaggingExerciseII::beginRun(edm::Run const&, edm::EventSetup const&)
   {
   }
   */

// ------------ method called when ending the processing of a run  ------------
/*
   void 
   BTaggingExerciseII::endRun(edm::Run const&, edm::EventSetup const&)
   {
   }
   */

// ------------ method called when starting to processes a luminosity block  ------------
/*
   void 
   BTaggingExerciseII::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
   {
   }
   */

// ------------ method called when ending the processing of a luminosity block  ------------
/*
   void 
   BTaggingExerciseII::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
   {
   }
   */

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
BTaggingExerciseII::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(BTaggingExerciseII);
