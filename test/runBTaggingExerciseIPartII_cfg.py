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
options.register('outputFilename', 'run2_discr.root',
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    "Output file name"
)
options.register('wantSummary', False,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Print out trigger and timing summary"
)

## 'maxEvents' is already registered by the Framework, changing default value
options.setDefault('maxEvents', 50000)

options.parseArguments()

process = cms.Process("User")

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
        # /TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM
        #'/store/mc/RunIISummer17MiniAOD/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/MINIAODSIM/92X_upgrade2017_realistic_v10_ext1-v1/110000/004132F1-7785-E711-A143-008CFAFC53C6.root' 
       #'root://cmseos.fnal.gov//store/user/cmsdas/2017/short_exercises/BTagging/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/0806AB92-99BE-E611-9ECD-0025905A6138.root'
       #'file:/afs/cern.ch/work/l/lata/public/941021E6-1FCF-E511-969E-FA163E8CF0DE.root' 
       '/store/mc/RunIIFall15MiniAODv2/BulkGravTohhTohbbhbb_narrow_M-3000_13TeV-madgraph/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/10000/52AAADC4-16CF-E511-8808-842B2B765E01.root','/store/mc/RunIIFall15MiniAODv2/BulkGravTohhTohbbhbb_narrow_M-3000_13TeV-madgraph/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/10000/96020602-17CF-E511-BFDE-C45444922988.root'
  )
)

## Output file

process.TFileService = cms.Service("TFileService",
  fileName = cms.string(options.outputFilename)
  
)

process.out = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string('Output.root'),
    ## save only events passing the full path
    #SelectEvents = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    outputCommands = cms.untracked.vstring(
       
        'keep *_*_*_User' #keep only the slimmed jets
    )
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
]

from PhysicsTools.PatAlgos.tools.jetTools import *
## Update the slimmedJets in miniAOD: corrections from the chosen Global Tag are applied and the b-tag discriminators are re-evaluated
#getattr(process,'updatedPatJets').addTagInfos = cms.bool(True)
updateJetCollection(
    process,
    jetSource = cms.InputTag('slimmedJets'),
    jetCorrections = ('AK4PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'None'),
    btagDiscriminators = bTagDiscriminators
   )

#process.append('keep *_selectedUpdatedPatJets_*_*')
#from PhysicsTools.PatAlgos.tools.helpers import getPatAlgosToolsTask
#patAlgosToolsTask = getPatAlgosToolsTask(process)
#process.outpath = cms.EndPath(process.out, patAlgosToolsTask)

process.out.outputCommands.append('keep *_selectedUpdatedPatJets_*_*')




#################################################



################################################

## Initialize analyzer

process.bTaggingExerciseIPartII = cms.EDAnalyzer('BTaggingExerciseI',
    jets = cms.InputTag('selectedUpdatedPatJets'), # input jet collection name
    bDiscriminators = cms.vstring(          # list of b-tag discriminators to access
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



## Let it run
process.p = cms.Path(process.bTaggingExerciseIPartII)
open('pydump1.py','w').write(process.dumpPython())
