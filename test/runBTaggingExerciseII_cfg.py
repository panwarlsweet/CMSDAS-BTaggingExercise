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
options.register('outputFilename', 'exerciseII_histos.root',
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    "Output file name"
)
options.register('process', 'Subjet',
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    "MC-simulated event type"
)
options.register('wantSummary', False,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Print out trigger and timing summary"
)

## 'maxEvents' is already registered by the Framework, changing default value
options.setDefault('maxEvents', 50000)

options.parseArguments()

process = cms.Process("real")


process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff")
#process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load('Configuration.Geometry.GeometryExtended2023D17Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2023D17_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '93X_upgrade2023_realistic_v2')

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = options.reportEvery

## Events to process
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )

## Input files
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        # /TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM
        #'root://cmseos.fnal.gov//store/user/cmsdas/2017/short_exercises/BTagging/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/0806AB92-99BE-E611-9ECD-0025905A6138.root'
        #  '/store/mc/RunIISummer17MiniAOD/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/MINIAODSIM/92X_upgrade2017_realistic_v10_ext1-v1/110000/004132F1-7785-E711-A143-008CFAFC53C6.root'
         #'file:/afs/cern.ch/work/l/lata/public/941021E6-1FCF-E511-969E-FA163E8CF0DE.root'
       '/store/mc/PhaseIITDRFall17MiniAOD/VBF_RS_bulk_M3000_W01pc_14TeV-madgraph/MINIAODSIM/PU200_93X_upgrade2023_realistic_v2-v2/00000/5216F0F5-29C1-E711-BF8C-0CC47A7C35A4.root',
'/store/mc/PhaseIITDRFall17MiniAOD/VBF_RS_bulk_M3000_W01pc_14TeV-madgraph/MINIAODSIM/PU200_93X_upgrade2023_realistic_v2-v2/00000/5462AFE4-C2C2-E711-A057-0CC47A4D76B6.root',
'/store/mc/PhaseIITDRFall17MiniAOD/VBF_RS_bulk_M3000_W01pc_14TeV-madgraph/MINIAODSIM/PU200_93X_upgrade2023_realistic_v2-v2/00000/742B99AF-76C1-E711-903F-B499BAABD28C.root',
'/store/mc/PhaseIITDRFall17MiniAOD/VBF_RS_bulk_M3000_W01pc_14TeV-madgraph/MINIAODSIM/PU200_93X_upgrade2023_realistic_v2-v2/00000/80D9376B-6BC2-E711-95B8-0CC47A7C35E0.root',
'/store/mc/PhaseIITDRFall17MiniAOD/VBF_RS_bulk_M3000_W01pc_14TeV-madgraph/MINIAODSIM/PU200_93X_upgrade2023_realistic_v2-v2/00000/881BE5E9-8CC1-E711-BF4E-5065F3810292.root',
'/store/mc/PhaseIITDRFall17MiniAOD/VBF_RS_bulk_M3000_W01pc_14TeV-madgraph/MINIAODSIM/PU200_93X_upgrade2023_realistic_v2-v2/00000/8A8680EF-3DC1-E711-8AC0-0CC47A4C8ED8.root',
'/store/mc/PhaseIITDRFall17MiniAOD/VBF_RS_bulk_M3000_W01pc_14TeV-madgraph/MINIAODSIM/PU200_93X_upgrade2023_realistic_v2-v2/00000/E8DA49D3-5AC2-E711-AE0A-0CC47A78A360.root',
'/store/mc/PhaseIITDRFall17MiniAOD/VBF_RS_bulk_M3000_W01pc_14TeV-madgraph/MINIAODSIM/PU200_93X_upgrade2023_realistic_v2-v2/00000/EEB6FB3E-43C1-E711-967F-0CC47A4DED42.root',
'/store/mc/PhaseIITDRFall17MiniAOD/VBF_RS_bulk_M3000_W01pc_14TeV-madgraph/MINIAODSIM/PU200_93X_upgrade2023_realistic_v2-v2/150000/1A34B1A1-1DC1-E711-B4E6-A4BF01125D56.root',
'/store/mc/PhaseIITDRFall17MiniAOD/VBF_RS_bulk_M3000_W01pc_14TeV-madgraph/MINIAODSIM/PU200_93X_upgrade2023_realistic_v2-v2/150000/6C145C80-7AC1-E711-B90C-0CC47AD9914C.root',
'/store/mc/PhaseIITDRFall17MiniAOD/VBF_RS_bulk_M3000_W01pc_14TeV-madgraph/MINIAODSIM/PU200_93X_upgrade2023_realistic_v2-v2/150000/7EE5A078-FFC1-E711-82FC-0025905A48EC.root',
'/store/mc/PhaseIITDRFall17MiniAOD/VBF_RS_bulk_M3000_W01pc_14TeV-madgraph/MINIAODSIM/PU200_93X_upgrade2023_realistic_v2-v2/150000/884D6531-39C1-E711-95DD-24BE05C6E7E1.root',
'/store/mc/PhaseIITDRFall17MiniAOD/VBF_RS_bulk_M3000_W01pc_14TeV-madgraph/MINIAODSIM/PU200_93X_upgrade2023_realistic_v2-v2/150000/90585B8D-51C1-E711-8A74-6C3BE5B5B108.root',
'/store/mc/PhaseIITDRFall17MiniAOD/VBF_RS_bulk_M3000_W01pc_14TeV-madgraph/MINIAODSIM/PU200_93X_upgrade2023_realistic_v2-v2/150000/ACE215A5-10C1-E711-8DCB-002590DE6C9A.root',
'/store/mc/PhaseIITDRFall17MiniAOD/VBF_RS_bulk_M3000_W01pc_14TeV-madgraph/MINIAODSIM/PU200_93X_upgrade2023_realistic_v2-v2/150000/B0E5EA20-22C1-E711-A4E4-1CC1DE1D03FC.root',
'/store/mc/PhaseIITDRFall17MiniAOD/VBF_RS_bulk_M3000_W01pc_14TeV-madgraph/MINIAODSIM/PU200_93X_upgrade2023_realistic_v2-v2/20000/E00B69B6-60C3-E711-9F50-0CC47A7C353E.root'
   )

)

if options.process == "QCD":
    process.source.fileNames = [
        # /QCD_Pt-15to7000_TuneCUETP8M1_Flat_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_magnetOn_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM
        'root://cmseos.fnal.gov//store/user/cmsdas/2017/short_exercises/BTagging/PUFlat0to70_80X_mcRun2_asymptotic_2016_TrancheIV_v4-v1/50000/00BC8956-278B-E611-99AD-0CC47A4D763C.root'
    ]

## Output file
process.TFileService = cms.Service("TFileService",
   fileName = cms.string(options.outputFilename.replace('.root','_' + options.process + '.root'))
)

## Options and Output Report
process.options   = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(options.wantSummary),
    allowUnscheduled = cms.untracked.bool(True)
)


#################################################
## Update PAT jets
#################################################

from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection

## b-tag discriminators
bTagDiscriminators = [
    'pfTrackCountingHighEffBJetTags',
    'pfTrackCountingHighPurBJetTags',
    'pfJetProbabilityBJetTags',
    'pfJetBProbabilityBJetTags',
    'pfSimpleSecondaryVertexHighEffBJetTags',
    'pfSimpleSecondaryVertexHighPurBJetTags',
    'pfCombinedSecondaryVertexV2BJetTags',
    'pfCombinedInclusiveSecondaryVertexV2BJetTags',
    'pfCombinedMVAV2BJetTags',
    'pfDeepCSVJetTags:probb',
    'pfDeepCSVJetTags:probbb'
  #  'pfDeepCSVJetTags:probb+pfDeepCSVJetTags:probbb'

]

from PhysicsTools.PatAlgos.tools.jetTools import *
## Update the slimmedJets in miniAOD: corrections from the chosen Global Tag are applied and the b-tag discriminators are re-evaluated
"""updateJetCollection(
    process,
    jetSource = cms.InputTag('slimmedJets'),
    jetCorrections = ('AK4PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'None'),
    btagDiscriminators = bTagDiscriminators
)"""

## Initialize analyzer
process.bTaggingExerciseII = cms.EDAnalyzer('BTaggingExerciseII',
    jets = cms.InputTag('slimmedJetsAK8'), # input jet collection name
    bDiscriminators = cms.vstring(      # list of b-tag discriminators to access
        'pfTrackCountingHighEffBJetTags',
        'pfTrackCountingHighPurBJetTags',
        'pfJetProbabilityBJetTags',
        'pfJetBProbabilityBJetTags',
        'pfSimpleSecondaryVertexHighEffBJetTags',
        'pfSimpleSecondaryVertexHighPurBJetTags',
        'pfCombinedSecondaryVertexV2BJetTags',
        'pfCombinedInclusiveSecondaryVertexV2BJetTags',
        'pfCombinedMVABJetTags',
        'pfDeepCSVJetTags'
    )
)

## Let it run
process.p = cms.Path(process.bTaggingExerciseII)
