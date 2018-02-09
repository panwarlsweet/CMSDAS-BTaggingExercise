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
options.register('process', 'QCD_phase2',
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
  '/store/mc/PhaseIITDRFall17MiniAOD/QCD_Mdijet-1000toInf_TuneCUETP8M1_14TeV-pythia8/MINIAODSIM/noPU_93X_upgrade2023_realistic_v2-v1/00000/0409BE50-26AC-E711-990B-0CC47A6C063E.root',
'/store/mc/PhaseIITDRFall17MiniAOD/QCD_Mdijet-1000toInf_TuneCUETP8M1_14TeV-pythia8/MINIAODSIM/noPU_93X_upgrade2023_realistic_v2-v1/00000/065D172D-D7AB-E711-A5CB-1866DAEB1FCC.root',
'/store/mc/PhaseIITDRFall17MiniAOD/QCD_Mdijet-1000toInf_TuneCUETP8M1_14TeV-pythia8/MINIAODSIM/noPU_93X_upgrade2023_realistic_v2-v1/00000/0A2D6042-27AC-E711-B340-001E6779245C.root',
'/store/mc/PhaseIITDRFall17MiniAOD/QCD_Mdijet-1000toInf_TuneCUETP8M1_14TeV-pythia8/MINIAODSIM/noPU_93X_upgrade2023_realistic_v2-v1/00000/0EAE4109-27AC-E711-9290-E0071B7A4550.root',
'/store/mc/PhaseIITDRFall17MiniAOD/QCD_Mdijet-1000toInf_TuneCUETP8M1_14TeV-pythia8/MINIAODSIM/noPU_93X_upgrade2023_realistic_v2-v1/00000/1C20C80D-26AC-E711-B87C-0CC47A0AD74E.root',
'/store/mc/PhaseIITDRFall17MiniAOD/QCD_Mdijet-1000toInf_TuneCUETP8M1_14TeV-pythia8/MINIAODSIM/noPU_93X_upgrade2023_realistic_v2-v1/00000/261C4EEC-99AA-E711-9751-001E67A3EF48.root',
'/store/mc/PhaseIITDRFall17MiniAOD/QCD_Mdijet-1000toInf_TuneCUETP8M1_14TeV-pythia8/MINIAODSIM/noPU_93X_upgrade2023_realistic_v2-v1/00000/2A0157D6-25AC-E711-8F32-2C768AAF879E.root',
'/store/mc/PhaseIITDRFall17MiniAOD/QCD_Mdijet-1000toInf_TuneCUETP8M1_14TeV-pythia8/MINIAODSIM/noPU_93X_upgrade2023_realistic_v2-v1/00000/2A39D0E8-67AB-E711-81A5-001E675A6A63.root',
'/store/mc/PhaseIITDRFall17MiniAOD/QCD_Mdijet-1000toInf_TuneCUETP8M1_14TeV-pythia8/MINIAODSIM/noPU_93X_upgrade2023_realistic_v2-v1/00000/40091B08-26AC-E711-8E94-A4BF01013F8D.root',
'/store/mc/PhaseIITDRFall17MiniAOD/QCD_Mdijet-1000toInf_TuneCUETP8M1_14TeV-pythia8/MINIAODSIM/noPU_93X_upgrade2023_realistic_v2-v1/00000/56AA38E3-25AC-E711-9AC7-B083FED3EE24.root',
'/store/mc/PhaseIITDRFall17MiniAOD/QCD_Mdijet-1000toInf_TuneCUETP8M1_14TeV-pythia8/MINIAODSIM/noPU_93X_upgrade2023_realistic_v2-v1/00000/6C20C8D6-25AC-E711-836F-549F358EB7D7.root',
'/store/mc/PhaseIITDRFall17MiniAOD/QCD_Mdijet-1000toInf_TuneCUETP8M1_14TeV-pythia8/MINIAODSIM/noPU_93X_upgrade2023_realistic_v2-v1/00000/C28C711F-04AB-E711-91B9-A4BADB1CFD4E.root',
'/store/mc/PhaseIITDRFall17MiniAOD/QCD_Mdijet-1000toInf_TuneCUETP8M1_14TeV-pythia8/MINIAODSIM/noPU_93X_upgrade2023_realistic_v2-v1/00000/C4A32C90-27AC-E711-8EC4-008CFAFC0122.root',
'/store/mc/PhaseIITDRFall17MiniAOD/QCD_Mdijet-1000toInf_TuneCUETP8M1_14TeV-pythia8/MINIAODSIM/noPU_93X_upgrade2023_realistic_v2-v1/150000/0C4A4293-5AB3-E711-8844-008CFAF28DCE.root',
'/store/mc/PhaseIITDRFall17MiniAOD/QCD_Mdijet-1000toInf_TuneCUETP8M1_14TeV-pythia8/MINIAODSIM/noPU_93X_upgrade2023_realistic_v2-v1/150000/18370D18-A3AE-E711-8161-0CC47A78A3EE.root',
'/store/mc/PhaseIITDRFall17MiniAOD/QCD_Mdijet-1000toInf_TuneCUETP8M1_14TeV-pythia8/MINIAODSIM/noPU_93X_upgrade2023_realistic_v2-v1/150000/1840A8C8-F9B2-E711-B722-008CFAF7350E.root',
'/store/mc/PhaseIITDRFall17MiniAOD/QCD_Mdijet-1000toInf_TuneCUETP8M1_14TeV-pythia8/MINIAODSIM/noPU_93X_upgrade2023_realistic_v2-v1/150000/1E3964D9-33B2-E711-ABC6-5065F38152E1.root'
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
    )
)

process.bTaggingExerciseIIAK8Jets = cms.EDAnalyzer('BTaggingExerciseII',
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
        'pfCombinedMVAV2BJetTags',
        'pfDeepCSVJetTags:probudsg',        
        'pfDeepCSVJetTags:probb',           
        'pfDeepCSVJetTags:probc',           
        'pfDeepCSVJetTags:probbb',          
    )
)

process.bTaggingExerciseIISubJets = cms.EDAnalyzer('BTaggingExerciseII',
    jets = cms.InputTag('slimmedJetsAK8PFPuppiSoftDropPacked:SubJets'), # input jet collection name
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

process.task = cms.Task()
for mod in process.producers_().itervalues():
    process.task.add(mod)
for mod in process.filters_().itervalues():
    process.task.add(mod)

## Let it run
process.p = cms.Path(
    process.bTaggingExerciseIIAK4Jets
    * process.bTaggingExerciseIIAK8Jets
    * process.bTaggingExerciseIISubJets
    ,process.task ) 

open('dump.py', 'w').write(process.dumpPython())
