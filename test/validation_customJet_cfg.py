import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing

###############################
####### Parameters ############
###############################

options = VarParsing ('python')

options.register('reportEvery', 100,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.int,
    "Report every N events (default is N=10)"
)
options.register('wantSummary', False,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Print out trigger and timing summary"
)

## 'maxEvents' is already registered by the Framework, changing default value
options.setDefault('maxEvents', 100)

options.parseArguments()

process = cms.Process("Validationreal")

process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff")
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '92X_upgrade2017_realistic_v11')

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = options.reportEvery

## Load DQM
process.load("DQMServices.Components.DQMEnvironment_cfi")
process.load("DQMServices.Core.DQM_cfg")

## Events to process
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )

## Input files
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        # /TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM
        #'/store/mc/RunIIFall15MiniAODv2/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/00000/023DCCDE-E3B8-E511-9985-002590DE6C56.root'
       'file:/afs/cern.ch/work/l/lata/test/CMSSW_9_2_8/src/CMSPOS/BTaggingExercise/MiniAODdrop_real.root' 
   )
)

## Options and Output Report
process.options   = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(options.wantSummary),
    allowUnscheduled = cms.untracked.bool(False)
)

#################################################
## Remake jets
#################################################

## Select charged hadron subtracted packed PF candidates
process.pfCHS = cms.EDFilter("CandPtrSelector", src = cms.InputTag("packedPFCandidates"), cut = cms.string("fromPV"))
from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJets
## Define PFJetsCHS
process.ak4PFJetsCHS = ak4PFJets.clone(src = 'pfCHS')

#################################################

## Jet collection we'll be using
jetCollection=cms.InputTag("ak4PFJetsCHS")

## Load b-tagging modules
process.load("RecoBTag.Configuration.RecoBTag_cff")
process.pfImpactParameterTagInfos.jets = jetCollection
process.softPFMuonsTagInfos.jets = jetCollection
process.softPFElectronsTagInfos.jets = jetCollection

process.btagSeq = cms.Sequence(
    # impact parameters and IP-only algorithms
    process.pfImpactParameterTagInfos *
    ( process.pfTrackCountingHighEffBJetTags +
      process.pfTrackCountingHighPurBJetTags +
      process.pfJetProbabilityBJetTags +
      process.pfJetBProbabilityBJetTags +

      # SV tag infos depending on IP tag infos, and SV (+IP) based algos
      process.pfSecondaryVertexTagInfos *
      ( process.pfSimpleSecondaryVertexHighEffBJetTags +
        process.pfSimpleSecondaryVertexHighPurBJetTags +
        process.pfCombinedSecondaryVertexV2BJetTags
      )
      + process.pfInclusiveSecondaryVertexFinderTagInfos *
      process.pfCombinedInclusiveSecondaryVertexV2BJetTags

    ) +

    # soft lepton tag infos and algos
    process.softPFMuonsTagInfos *
    process.softPFMuonBJetTags
    + process.softPFElectronsTagInfos *
    process.softPFElectronBJetTags
)

## For MC-based pileup jet ID
process.ak4GenJetsForPUid = cms.EDFilter("GenJetSelector",
    src = cms.InputTag("slimmedGenJets"),
    cut = cms.string('pt > 8.'),
    filter = cms.bool(False)
)
process.load("PhysicsTools.PatAlgos.mcMatchLayer0.jetMatch_cfi")
process.patJetGenJetMatch.src = jetCollection
process.patJetGenJetMatch.matched = cms.InputTag("ak4GenJetsForPUid")
process.patJetGenJetMatch.maxDeltaR = cms.double(0.25)
process.patJetGenJetMatch.resolveAmbiguities = cms.bool(True)

## Load the jet flavor modules
process.load("PhysicsTools.JetMCAlgos.HadronAndPartonSelector_cfi")
process.load("PhysicsTools.JetMCAlgos.AK4PFJetsMCFlavourInfos_cfi")
process.ak4JetFlavourInfos.jets = jetCollection
process.ak4JetFlavourInfos.hadronFlavourHasPriority = cms.bool(True)
process.flavourSeq = cms.Sequence(
    process.selectedHadronsAndPartons *
    process.ak4JetFlavourInfos
)

## Load b-tag validation
process.load("Validation.RecoB.bTagAnalysis_cfi")
## Some common parameters to be set below
flavPlots = "allbcl" # if contains "all" plots for all jets booked, if contains "bcl" histograms for b, c and light jets booked, if contains "dusg" all histograms booked
ptRanges = cms.vdouble(30.0,80.0,120.0,200.0)
etaRanges = cms.vdouble(0.0,1.4,2.4)
## Specify taggers for which we want to produce the validation plots
from DQMOffline.RecoB.bTagCommon_cff import *
tags = cms.VPSet(
    cms.PSet(
        bTagTrackCountingAnalysisBlock,
        label = cms.InputTag("pfTrackCountingHighEffBJetTags"),
        folder = cms.string("pfTCHE")
        ),
    cms.PSet(
        bTagTrackCountingAnalysisBlock,
        label = cms.InputTag("pfTrackCountingHighPurBJetTags"),
        folder = cms.string("pfTCHP")
        ),
    cms.PSet(
        bTagProbabilityAnalysisBlock,
        label = cms.InputTag("pfJetProbabilityBJetTags"),
        folder = cms.string("pfJP")
        ),
    cms.PSet(
        bTagBProbabilityAnalysisBlock,
        label = cms.InputTag("pfJetBProbabilityBJetTags"),
        folder = cms.string("pfJBP")
        ),
    cms.PSet(
        bTagSimpleSVAnalysisBlock,
        label = cms.InputTag("pfSimpleSecondaryVertexHighEffBJetTags"),
        folder = cms.string("pfSSVHE")
        ),
    cms.PSet(
        bTagSimpleSVAnalysisBlock,
        label = cms.InputTag("pfSimpleSecondaryVertexHighPurBJetTags"),
        folder = cms.string("pfSSVHP")
        ),
    cms.PSet(
        bTagGenericAnalysisBlock,
        label = cms.InputTag("pfCombinedSecondaryVertexV2BJetTags"),
        folder = cms.string("pfCSVv2")
        )
#,
############ DeepCSV
 #       cms.PSet(
  #          bTagGenericAnalysisBlock,
   #         label = cms.InputTag("pfDeepCSVJetTags:probb"),
    #        folder = cms.string("deepCSV_probb")
     #   ),
#	cms.PSet(
 #           bTagGenericAnalysisBlock,
  #          label = cms.InputTag("pfDeepCSVJetTags:probc"),
   #         folder = cms.string("deepCSV_probc")
    #    ),
#	cms.PSet(
 #           bTagGenericAnalysisBlock,
  #          label = cms.InputTag("pfDeepCSVJetTags:probudsg"),
   #         folder = cms.string("deepCSV_probudsg")
    #    ),
#	cms.PSet(
 #           bTagGenericAnalysisBlock,
  #          label = cms.InputTag("pfDeepCSVJetTags:probbb"),
   #         folder = cms.string("deepCSV_probbb")
    #    )
)
## Tweak the validation configuration
process.bTagValidation.jetMCSrc = 'ak4JetFlavourInfos'
process.bTagValidation.applyPtHatWeight = False
process.bTagValidation.genJetsMatched = cms.InputTag("patJetGenJetMatch")
process.bTagValidation.doPUid = cms.bool(True)
process.bTagValidation.flavPlots = flavPlots
process.bTagValidation.ptRanges = ptRanges
process.bTagValidation.etaRanges = etaRanges
process.bTagValidation.tagConfig = tags
## The following harvesting parameters need to have the same values as in the validation
process.bTagHarvestMC.flavPlots = flavPlots
process.bTagHarvestMC.ptRanges = ptRanges
process.bTagHarvestMC.etaRanges = etaRanges
process.bTagHarvestMC.tagConfig = tags

## As the validation is embedded in the DQM environment, we also need to configure a few DQM parameters to make sure
## the histograms from the validation are saved correctly (further explanations of DQM are beyond the scope of this tutorial)
process.dqmEnv.subSystemFolder = 'BTAG'
process.dqmSaver.producer = 'DQM'
process.dqmSaver.workflow = '/POG/BTAG/BJET'
process.dqmSaver.convention = 'Offline'
process.dqmSaver.saveByRun = cms.untracked.int32(-1)
process.dqmSaver.saveAtJobEnd =cms.untracked.bool(True) 
process.dqmSaver.forceRunNumber = cms.untracked.int32(1)

## Adapt module configurations to MiniAOD input
process.pfImpactParameterTagInfos.primaryVertex = cms.InputTag("offlineSlimmedPrimaryVertices")
process.pfImpactParameterTagInfos.candidates = cms.InputTag("packedPFCandidates")
process.pfInclusiveSecondaryVertexFinderTagInfos.extSVCollection = cms.InputTag('slimmedSecondaryVertices')
process.softPFMuonsTagInfos.primaryVertex = cms.InputTag("offlineSlimmedPrimaryVertices")
process.softPFMuonsTagInfos.muons = cms.InputTag("slimmedMuons")
process.softPFElectronsTagInfos.primaryVertex = cms.InputTag("offlineSlimmedPrimaryVertices")
process.softPFElectronsTagInfos.electrons = cms.InputTag("slimmedElectrons")
process.selectedHadronsAndPartons.particles = cms.InputTag("prunedGenParticles")

## Let it run
process.dqm = cms.Path(process.pfCHS * process.ak4PFJetsCHS * process.btagSeq * process.ak4GenJetsForPUid * process.patJetGenJetMatch * process.flavourSeq * process.bTagValidation * process.bTagHarvestMC * process.dqmSaver)
