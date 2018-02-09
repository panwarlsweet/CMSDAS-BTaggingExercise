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
options.register('process', '80',
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
options.setDefault('maxEvents', 10000)

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
    '/store/mc/RunIISummer16MiniAODv2/BulkGravTohhTohbbhbb_narrow_M-3000_13TeV-madgraph/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/70000/1E26D4B1-A015-E711-918C-001EC9ADFD3D.root',
'/store/mc/RunIISummer16MiniAODv2/BulkGravTohhTohbbhbb_narrow_M-3000_13TeV-madgraph/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/70000/20B29E41-0915-E711-9540-549F358EB77C.root',
'/store/mc/RunIISummer16MiniAODv2/BulkGravTohhTohbbhbb_narrow_M-3000_13TeV-madgraph/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/70000/245ED84B-B515-E711-B87D-A0369F836288.root',
'/store/mc/RunIISummer16MiniAODv2/BulkGravTohhTohbbhbb_narrow_M-3000_13TeV-madgraph/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/70000/32EFA84A-B515-E711-BA9A-0242AC130005.root',
'/store/mc/RunIISummer16MiniAODv2/BulkGravTohhTohbbhbb_narrow_M-3000_13TeV-madgraph/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/70000/34B57314-3115-E711-93A6-008CFA110AA8.root',
'/store/mc/RunIISummer16MiniAODv2/BulkGravTohhTohbbhbb_narrow_M-3000_13TeV-madgraph/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/70000/42759766-B515-E711-B176-008CFA1113E8.root',
'/store/mc/RunIISummer16MiniAODv2/BulkGravTohhTohbbhbb_narrow_M-3000_13TeV-madgraph/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/70000/46155E51-B515-E711-8E7F-0025905B859A.root'
    )
)

if options.process == "QCD":
    process.source.fileNames = [
        # /QCD_Pt-15to7000_TuneCUETP8M1_Flat_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_magnetOn_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM
        #'root://cmseos.fnal.gov//store/user/cmsdas/2017/short_exercises/BTagging/PUFlat0to70_80X_mcRun2_asymptotic_2016_TrancheIV_v4-v1/50000/00BC8956-278B-E611-99AD-0CC47A4D763C.root'
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
updateJetCollection(
    process,
    jetSource = cms.InputTag('slimmedJets'),
    jetCorrections = ('AK4PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'None'),
    btagDiscriminators = bTagDiscriminators
)

updateJetCollection(
    process,
    labelName='FatPF',
    jetSource=cms.InputTag('slimmedJetsAK8'),
    jetCorrections = ('AK8PFPuppi', ['L2Relative', 'L3Absolute'], 'None'), 
    btagDiscriminators = bTagDiscriminators,
)

updateJetCollection(
    process,
    labelName='SoftDropSubjetsPF',
    jetSource=cms.InputTag('slimmedJetsAK8PFPuppiSoftDropPacked:SubJets'),
    jetCorrections = ('AK4PFPuppi', ['L2Relative', 'L3Absolute'], 'None'),
    btagDiscriminators = bTagDiscriminators,
)

## Initialize analyzer
process.bTaggingExerciseIIAK4Jets = cms.EDAnalyzer('BTaggingExerciseII',
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
        'pfDeepCSVJetTags'
        #'pfDeepCSVJetTags:probudsg',        
        #'pfDeepCSVJetTags:probb',           
        #'pfDeepCSVJetTags:probc',           
        #'pfDeepCSVJetTags:probbb',          
    )
)

process.bTaggingExerciseIIAK8Jets = cms.EDAnalyzer('BTaggingExerciseII',
    jets = cms.InputTag('selectedUpdatedPatJetsFatPF'), # input jet collection name
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
        'pfDeepCSVJetTags'
        #'pfDeepCSVJetTags:probudsg',        
        #'pfDeepCSVJetTags:probb',           
        #'pfDeepCSVJetTags:probc',           
        #'pfDeepCSVJetTags:probbb',          
    )
)

process.bTaggingExerciseIISubJets = cms.EDAnalyzer('BTaggingExerciseII',
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
        'pfDeepCSVJetTags'
    )
)

"""process.task = cms.Task()
for mod in process.producers_().itervalues():
    process.task.add(mod)
for mod in process.filters_().itervalues():
    process.task.add(mod)"""

## Let it run
process.p = cms.Path(
    process.bTaggingExerciseIIAK4Jets
    * process.bTaggingExerciseIIAK8Jets
    * process.bTaggingExerciseIISubJets)
#    ,process.task ) 

open('dump.py', 'w').write(process.dumpPython())
