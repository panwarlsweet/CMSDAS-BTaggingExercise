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
options.register('outputFilename', 'exerciseII_histos.root',
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    "Output file name"
)
options.register('process', 'BG2000',
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
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc')

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = options.reportEvery

## Events to process
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )

## Input files
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
'/store/mc/RunIISummer17MiniAOD/BulkGravTohhTohbbhbb_narrow_M-2000_13TeV-madgraph/MINIAODSIM/92X_upgrade2017_realistic_v10-v2/90000/30128937-4D99-E711-8420-0CC47AB0B826.root',
'/store/mc/RunIISummer17MiniAOD/BulkGravTohhTohbbhbb_narrow_M-2000_13TeV-madgraph/MINIAODSIM/92X_upgrade2017_realistic_v10-v2/90000/301A108C-549A-E711-86A5-60EB69BACBC6.root',
'/store/mc/RunIISummer17MiniAOD/BulkGravTohhTohbbhbb_narrow_M-2000_13TeV-madgraph/MINIAODSIM/92X_upgrade2017_realistic_v10-v2/90000/349299C5-069A-E711-B772-0090FAA573E0.root',
'/store/mc/RunIISummer17MiniAOD/BulkGravTohhTohbbhbb_narrow_M-2000_13TeV-madgraph/MINIAODSIM/92X_upgrade2017_realistic_v10-v2/90000/3E57125C-1F99-E711-9519-44A842CFC9BF.root',
'/store/mc/RunIISummer17MiniAOD/BulkGravTohhTohbbhbb_narrow_M-2000_13TeV-madgraph/MINIAODSIM/92X_upgrade2017_realistic_v10-v2/90000/46F8D1F9-F499-E711-BDC3-0CC47A4D75F6.root',
'/store/mc/RunIISummer17MiniAOD/BulkGravTohhTohbbhbb_narrow_M-2000_13TeV-madgraph/MINIAODSIM/92X_upgrade2017_realistic_v10-v2/90000/5AB9168D-ED99-E711-B81A-44A842CFC9F3.root',
'/store/mc/RunIISummer17MiniAOD/BulkGravTohhTohbbhbb_narrow_M-2000_13TeV-madgraph/MINIAODSIM/92X_upgrade2017_realistic_v10-v2/90000/5C9E22A9-CA99-E711-B00F-001E67E6F616.root',
'/store/mc/RunIISummer17MiniAOD/BulkGravTohhTohbbhbb_narrow_M-2000_13TeV-madgraph/MINIAODSIM/92X_upgrade2017_realistic_v10-v2/90000/6267F4DC-C399-E711-B5B8-002590DE6C9A.root',
'/store/mc/RunIISummer17MiniAOD/BulkGravTohhTohbbhbb_narrow_M-2000_13TeV-madgraph/MINIAODSIM/92X_upgrade2017_realistic_v10-v2/90000/669C37B2-4A99-E711-A3A3-008CFAC93FD0.root',
'/store/mc/RunIISummer17MiniAOD/BulkGravTohhTohbbhbb_narrow_M-2000_13TeV-madgraph/MINIAODSIM/92X_upgrade2017_realistic_v10-v2/90000/7E67357F-1599-E711-BC9F-68B5996BD98E.root',
'/store/mc/RunIISummer17MiniAOD/BulkGravTohhTohbbhbb_narrow_M-2000_13TeV-madgraph/MINIAODSIM/92X_upgrade2017_realistic_v10-v2/90000/84448261-169A-E711-9D78-0CC47ABB518A.root'
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
    'pfDeepCSVJetTags:probudsg',        
    'pfDeepCSVJetTags:probb',           
    'pfDeepCSVJetTags:probc',           
    'pfDeepCSVJetTags:probbb',          
]

from PhysicsTools.PatAlgos.tools.jetTools import *
## Update the slimmedJets in miniAOD: corrections from the chosen Global Tag are applied and the b-tag discriminators are re-evaluated
"""updateJetCollection(
    process,
    jetSource = cms.InputTag('slimmedJets'),
    jetCorrections = ('AK4PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'None'),
    btagDiscriminators = bTagDiscriminators
)"""

updateJetCollection(
    process,
    labelName='FatPF',
    jetSource=cms.InputTag('slimmedJetsAK8'),
    jetCorrections = ('AK8PFPuppi', ['L2Relative', 'L3Absolute'], 'None'), 
    btagDiscriminators = bTagDiscriminators,
)

"""updateJetCollection(
    process,
    labelName='SoftDropSubjetsPF',
    jetSource=cms.InputTag('slimmedJetsAK8PFPuppiSoftDropPacked:SubJets'),
    jetCorrections = ('AK4PFPuppi', ['L2Relative', 'L3Absolute'], 'None'),
    btagDiscriminators = bTagDiscriminators,
)"""

## Initialize analyzer
"""process.bTaggingExerciseIIAK4Jets = cms.EDAnalyzer('BTaggingExerciseII',
    jets = cms.InputTag('selectedUpdatedPatJets'), # input jet collection name
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

process.bTaggingExerciseIIAK8Jets = cms.EDAnalyzer('BTaggingExerciseII',
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
)

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
     process.bTaggingExerciseIIAK8Jets
    ,process.task ) 

open('dump.py', 'w').write(process.dumpPython())
