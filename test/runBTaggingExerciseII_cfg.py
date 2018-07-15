import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing

###############################
####### Parameters ############
###############################

options = VarParsing ('python')

options.register('reportEvery', 10,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.int,
    "Report every N events (default is N=10)"
)
options.register('outputFilename', 'exerciseII_histos_posEta.root',
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    "Output file name"
)
options.register('process', 'TTbar_HE',
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

process = cms.Process("USER")


process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff")
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '101X_upgrade2018_realistic_HEmiss_v1')

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = options.reportEvery

## Events to process
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )

## Input files
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
         '/store/relval/CMSSW_10_1_7/RelValTTbar_13/MINIAODSIM/PU25ns_101X_upgrade2018_realistic_HEmiss_v1-v1/10000/6002343D-1780-E811-906C-0CC47A7C3422.root'
    )
)

if options.process == "QCD":
    process.source.fileNames = [
           '/store/relval/CMSSW_10_1_7/RelValQCD_FlatPt_15_3000HS_13/MINIAODSIM/PU25ns_101X_upgrade2018_realistic_HEmiss_v1-v1/10000/BEE776E1-2380-E811-A67A-00248C55CC3C.root',
	   '/store/relval/CMSSW_10_1_7/RelValQCD_FlatPt_15_3000HS_13/MINIAODSIM/PU25ns_101X_upgrade2018_realistic_HEmiss_v1-v1/10000/B46E1834-5880-E811-B31B-0CC47A4D7694.root'
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
    'pfDeepCSVJetTags:probudsg',        
    'pfDeepCSVJetTags:probb',           
    'pfDeepCSVJetTags:probc',           
    'pfDeepCSVJetTags:probbb',          
    'pfDeepFlavourJetTags:probb',
    'pfDeepFlavourJetTags:probbb',
    'pfDeepFlavourJetTags:probc',
    'pfDeepFlavourJetTags:probudsg'
]

from PhysicsTools.PatAlgos.tools.jetTools import *
## Update the slimmedJets in miniAOD: corrections from the chosen Global Tag are applied and the b-tag discriminators are re-evaluated
"""updateJetCollection(
    process,
    jetSource = cms.InputTag('slimmedJets'),
    jetCorrections = ('AK4PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'None'),
    btagDiscriminators = bTagDiscriminators
)"""

"""updateJetCollection(
    process,
    labelName='FatPF',
    jetSource=cms.InputTag('slimmedJetsAK8'),
    jetCorrections = ('AK8PFPuppi', ['L2Relative', 'L3Absolute'], 'None'), 
    btagDiscriminators = bTagDiscriminators,
)"""

"""updateJetCollection(
    process,
    labelName='SoftDropSubjetsPF',
    jetSource=cms.InputTag('slimmedJetsAK8PFPuppiSoftDropPacked:SubJets'),
    jetCorrections = ('AK4PFPuppi', ['L2Relative', 'L3Absolute'], 'None'),
    btagDiscriminators = bTagDiscriminators,
)"""

## Initialize analyzer
process.bTaggingExerciseIIAK4Jets = cms.EDAnalyzer('BTaggingExerciseII',
    jets = cms.InputTag('slimmedJets'), # input jet collection name
    bDiscriminators = cms.vstring(      # list of b-tag discriminators to access
        'pfTrackCountingHighEffBJetTags',
        'pfTrackCountingHighPurBJetTags',
        'pfJetProbabilityBJetTags',
        'pfJetBProbabilityBJetTags',
        'pfSimpleSecondaryVertexHighEffBJetTags',
        'pfSimpleSecondaryVertexHighPurBJetTags',
        'pfCombinedSecondaryVertexV2BJetTags',
        'pfCombinedInclusiveSecondaryVertexV2BJetTags',
        'pfCombinedMVAV2BJetTags',
        'pfDeepCSVJetTags:probudsg',        
        'pfDeepCSVJetTags:probb',           
        'pfDeepCSVJetTags:probc',           
        'pfDeepCSVJetTags:probbb',
        'pfDeepFlavourJetTags:probb',
        'pfDeepFlavourJetTags:probbb',
        'pfDeepFlavourJetTags:probc',
        'pfDeepFlavourJetTags:probudsg'          
    )
)

"""process.bTaggingExerciseIIAK8Jets = cms.EDAnalyzer('BTaggingExerciseII',
    jetsak8 = cms.InputTag('selectedUpdatedPatJetsFatPF'), # input jet collection name
    bDiscriminators = cms.vstring(      # list of b-tag discriminators to access
        'pfTrackCountingHighEffBJetTags',
        'pfTrackCountingHighPurBJetTags',
        'pfJetProbabilityBJetTags',
        'pfJetBProbabilityBJetTags',
        'pfSimpleSecondaryVertexHighEffBJetTags',
        'pfSimpleSecondaryVertexHighPurBJetTags',
        'pfCombinedSecondaryVertexV2BJetTags',
        'pfCombinedInclusiveSecondaryVertexV2BJetTags',
        'pfCombinedMVAV2BJetTags',
        'pfDeepCSVJetTags:probudsg',        
        'pfDeepCSVJetTags:probb',           
        'pfDeepCSVJetTags:probc',           
        'pfDeepCSVJetTags:probbb',          
    )
)"""

"""process.bTaggingExerciseIISubJets = cms.EDAnalyzer('BTaggingExerciseII',
    jets = cms.InputTag('selectedUpdatedPatJetsSoftDropSubjetsPF'), # input jet collection name
    bDiscriminators = cms.vstring(      # list of b-tag discriminators to access
        'pfTrackCountingHighEffBJetTags',
        'pfTrackCountingHighPurBJetTags',
        'pfJetProbabilityBJetTags',
        'pfJetBProbabilityBJetTags',
        'pfSimpleSecondaryVertexHighEffBJetTags',
        'pfSimpleSecondaryVertexHighPurBJetTags',
        'pfCombinedSecondaryVertexV2BJetTags',
        'pfCombinedInclusiveSecondaryVertexV2BJetTags',
        'pfCombinedMVAV2BJetTags',
        'pfDeepCSVJetTags:probudsg',        
        'pfDeepCSVJetTags:probb',           
        'pfDeepCSVJetTags:probc',           
        'pfDeepCSVJetTags:probbb',          
    )
)"""

process.task = cms.Task()
for mod in process.producers_().itervalues():
    process.task.add(mod)
for mod in process.filters_().itervalues():
    process.task.add(mod)

## Let it run
process.p = cms.Path(
     process.bTaggingExerciseIIAK4Jets
    ,process.task ) 

open('dump.py', 'w').write(process.dumpPython())
