# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response,get_object_or_404
from django.db.models import Q
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings

#from DjVALD.vald.models import Transition,State,Source,Species
from DjCDMS.cdms.models import RadiativeTransitions,StatesMolecules,Sources #,Species

import sys
def LOG(s):
    print >> sys.stderr, s




RETURNABLES={\
'SourceID':'Sources.rId', #.id',
'SourceAuthorName':'Sources.authors', #.srcdescr',
'SourceCategory':'Sources.category',
'SourcePageBegin':'Sources.pageBegin',
'SourcePageEnd':'Sources.pageEnd',
'SourceName':'Sources.name',
'SourceTitle':'Sources.title',
'SourceURI':'Sources.uri',
'SourceVolume':'Sources.vol',
'SourceYear':'Sources.year',
'MethodID':'"MCALC"',
'MethodCategory':'"calculated"',
'MethodDescription':'',
'AtomStateID':'',
'AtomSymbol':'',
'AtomNuclearCharge':'',
'AtomCompositionComments':'',
'AtomConfigurationLabel':'',
'AtomCompositionComponentTerm':'',
'AtomIonizationEnergy':'',
'AtomLandeFactor':'',
'AtomStateEnergy':'',
'AtomStateDescription':'',
'AtomIonCharge':'',
'AtomMassNumber':'',
#'RadTransComments':'',
#'RadTransWavelengthAir':'',
#'RadTransWavelengthVac':'',
#'RadTransWavelengthAccuracyFlag':'',
#'RadTransWavelengthAccuracy':'',

'RadTransComments':'',

'RadTransFinalStateRef':'RadTran.finalstateref',
'RadTransInitialStateRef':'RadTran.initialstateref',

'RadTransWavenumberRitzComments':'',
'RadTransWavenumberRitzSourceRef':'',
'RadTransWavenumberRitzMethodRef':'',
'RadTransWavenumberRitzValue':'',
'RadTransWavenumberRitzUnits':'',
'RadTransWavenumberRitzAccuracy':'',
'RadTransWavenumberExperimentalComments':'',
'RadTransWavenumberExperimentalSourceRef':'',
'RadTransWavenumberExperimentalMethodRef':'',
'RadTransWavenumberExperimentalValue':'',
'RadTransWavenumberExperimentalUnits':'',
'RadTransWavenumberExperimentalAccuracy':'',
'RadTransWavenumberTheoreticalComments':'',
'RadTransWavenumberTheoreticalSourceRef':'',
'RadTransWavenumberTheoreticalMethodRef':'',
'RadTransWavenumberTheoreticalValue':'',
'RadTransWavenumberTheoreticalUnits':'',
'RadTransWavenumberTheoreticalAccuracy':'',
'RadTransWavelengthRitzComments':'',
'RadTransWavelengthRitzSourceRef':'',
'RadTransWavelengthRitzMethodRef':'',
'RadTransWavelengthRitzValue':'',
'RadTransWavelengthRitzUnits':'',
'RadTransWavelengthRitzAccuracy':'',
'RadTransWavelengthExperimentalComments':'',
'RadTransWavelengthExperimentalSourceRef':'',
'RadTransWavelengthExperimentalMethodRef':'',
'RadTransWavelengthExperimentalValue':'',
'RadTransWavelengthExperimentalUnits':'',
'RadTransWavelengthExperimentalAccuracy':'',
'RadTransWavelengthTheoreticalComments':'',
'RadTransWavelengthTheoreticalSourceRef':'',
'RadTransWavelengthTheoreticalMethodRef':'',
'RadTransWavelengthTheoreticalValue':'',
'RadTransWavelengthTheoreticalUnits':'',
'RadTransWavelengthTheoreticalAccuracy':'',
'RadTransEnergyRitzComments':'',
'RadTransEnergyRitzSourceRef':'',
'RadTransEnergyRitzMethodRef':'',
'RadTransEnergyRitzValue':'',
'RadTransEnergyRitzUnits':'',
'RadTransEnergyRitzAccuracy':'',
'RadTransEnergyExperimentalComments':'',
'RadTransEnergyExperimentalSourceRef':'',
'RadTransEnergyExperimentalMethodRef':'',
'RadTransEnergyExperimentalValue':'',
'RadTransEnergyExperimentalUnits':'',
'RadTransEnergyExperimentalAccuracy':'',
'RadTransEnergyTheoreticalComments':'',
'RadTransEnergyTheoreticalSourceRef':'',
'RadTransEnergyTheoreticalMethodRef':'',
'RadTransEnergyTheoreticalValue':'',
'RadTransEnergyTheoreticalUnits':'',
'RadTransEnergyTheoreticalAccuracy':'',
'RadTransFrequencyRitzComments':'',
'RadTransFrequencyRitzSourceRef':'',
'RadTransFrequencyRitzMethodRef':'',
'RadTransFrequencyRitzValue':'',
'RadTransFrequencyRitzUnits':'',
'RadTransFrequencyRitzAccuracy':'',
'RadTransFrequencyExperimentalComments':'',
'RadTransFrequencyExperimentalSourceRef':'',
'RadTransFrequencyExperimentalMethodRef':'',
'RadTransFrequencyExperimentalValue':'',
'RadTransFrequencyExperimentalUnits':'',
'RadTransFrequencyExperimentalAccuracy':'',
'RadTransFrequencyTheoreticalComments':'',
'RadTransFrequencyTheoreticalSourceRef':'',
'RadTransFrequencyTheoreticalMethodRef':'',
'RadTransFrequencyTheoreticalValue':'RadTran.frequencyvalue',
'RadTransFrequencyTheoreticalUnits':'RadTran.frequencyunit',
'RadTransFrequencyTheoreticalAccuracy':'RadTran.energywavelengthaccuracy',
'RadTransProbabilityTransitionProbabilityAComments ':'',
'RadTransProbabilityTransitionProbabilityASourceRef':'',
'RadTransProbabilityTransitionProbabilityAMethodRef':'',
'RadTransProbabilityTransitionProbabilityAValue':'',
'RadTransProbabilityTransitionProbabilityAUnits':'',
'RadTransProbabilityTransitionProbabilityAAccuracy':'',
'RadTransProbabilityOscillatorStrengthComments ':'',
'RadTransProbabilityOscillatorStrengthSourceRef':'',
'RadTransProbabilityOscillatorStrengthMethodRef':'',
'RadTransProbabilityOscillatorStrengthValue':'',
'RadTransProbabilityOscillatorStrengthUnits':'',
'RadTransProbabilityOscillatorStrengthAccuracy':'',
'RadTransProbabilityLineStrengthComments ':'',
'RadTransProbabilityLineStrengthSourceRef':'',
'RadTransProbabilityLineStrengthMethodRef':'',
'RadTransProbabilityLineStrengthValue':'',
'RadTransProbabilityLineStrengthUnits':'',
'RadTransProbabilityLineStrengthAccuracy':'',
'RadTransProbabilityWeightedOscillatorStrengthComments ':'',
'RadTransProbabilityWeightedOscillatorStrengthSourceRef':'',
'RadTransProbabilityWeightedOscillatorStrengthMethodRef':'',
'RadTransProbabilityWeightedOscillatorStrengthValue':'',
'RadTransProbabilityWeightedOscillatorStrengthUnits':'',
'RadTransProbabilityWeightedOscillatorStrengthAccuracy':'',
'RadTransProbabilityLog10WeightedOscillatorStrengthComments ':'',
'RadTransProbabilityLog10WeightedOscillatorStrengthSourceRef':'',
'RadTransProbabilityLog10WeightedOscillatorStrengthMethodRef':'',
'RadTransProbabilityLog10WeightedOscillatorStrengthValue':'RadTran.log10weightedoscillatorstrengthvalue',
'RadTransProbabilityLog10WeightedOscillatorStrengthUnits':'RadTran.log10weightedoscillatorstrengthunit',
'RadTransProbabilityLog10WeightedOscillatorStrengthAccuracy':'',
'RadTransProbabilityIdealisedIntensityComments ':'',
'RadTransProbabilityIdealisedIntensitySourceRef':'',
'RadTransProbabilityIdealisedIntensityMethodRef':'',
'RadTransProbabilityIdealisedIntensityValue':'',
'RadTransProbabilityIdealisedIntensityUnits':'',
'RadTransProbabilityIdealisedIntensityAccuracy':'',
'RadTransProbabilityProbability:MultipoleValue':'RadTran.multipole',


'CollisionComments':'',
'CollisionTabulatedData':'',
'CollisionProcessClassCode':'',
'CollisionProductsStateRef':'',
'CollisionReactantsStateRef':'',


# table for molecular states 
# (maybe molecular species should be a separate table)
    
'MolecularSpeciesChemicalName':'MolState.molecularchemicalspecies',
'MolecularSpeciesOrdinaryStructuralFormula':'',
'MolecularSpeciesStoichiometrcFormula':'MolState.isotopomer',
'MolecularSpeciesIonCharge':'',
'MolecularSpeciesIUPACName':'',
'MolecularSpeciesURLFigure':'',
'MolecularSpeciesInChl':'',
'MolecularSpeciesCASRegistryNumber':'',
'MolecularSpeciesCNPIGroup':'',
'MolecularSpeciesMoleculeNuclearSpins':'',
'MolecularSpeciesStableMolecularProperties':'',
'MolecularSpeciesMolecularWeight':'',
'MolecularSpeciesComment':'',
'MoleculeNuclearSpinsAtomArray':'',
'MoleculeNuclearSpinsBondArray':'',

'MolecularStateStateID':'MolState.stateid',
'MolecularStateDescription':'',
'MolecularStateEnergyComments':'',
'MolecularStateEnergySourceRef':'',
'MolecularStateEnergyMethodRef':'',
'MolecularStateEnergyValue':'MolState.stateenergyvalue',
'MolecularStateEnergyUnit':'MolState.stateenergyunit',
'MolecularStateEnergyAccuracy':'MolState.stateenergyaccuracy',
'MolecularStateEnergyOrigin':'',
'MolecularStateMixingCoefficient':'MolState.mixingcoefficient',

'MolecularStateCharacTotalStatisticalWeight':'',
'MolecularStateCharacNuclearStatisticalWeight':'MolState.statenuclearstatisticalweight',
'MolecularStateCharacNuclearSpinSymmetry':'',
'MolecularStateCharacLifeTime':'',
'MolecularStateCharacParameters':'',

# table for quantum numbers

'MolQnStateID':'StateQN.stateid',
'MolQnCase':'StateQN.case',  #(for case-by-case)
'MolQnLabel':'StateQN.label', #(for case-by-case) (should be labels suggested by Christian Hill)
'MolXPath':'',   #(for classical)
'MolTag':'',     #(for classical)
'MolQnValue':'StateQN.value',
'MolQnSpinRef':'StateQN.spinref',
'MolQnAttribute':'StateQN.attribute',
'MolQnComment':'StateQN.comment'

}

RESTRICTABLES = {\
'MolecularChemicalSpecies':'molecularchemicalspecies',
'AtomSymbol':'species__name',
'AtomNuclearCharge':'species__atomic',
'AtomStateEnergy':'upstate__energy',
'RadTransWavelengthExperimentalValue':'frequencyvalue',
'RadTransLogGF':'loggf',
'AtomIonCharge':'species__ion',
'RadTransFrequencyTheoreticalValue':'RadiativeTransitions.frequencyvalue',
'RadTransFrequencyTheoreticalUnits':'RadiativeTransitions.frequencyunit',
'RadTransFrequencyTheoreticalAccuracy':'RadiativeTransitions.energywavelengthaccuracy',
}


from DjNode.tapservice.sqlparse import *

def getCDMSsources(transs):
    return # no sources yet for CDMS, afaik
    #return Source.objects.filter(pk__in=sids)

def getCDMSstates(transs):
#    q1,q2=Q(isupperstate_trans__in=transs),Q(islowerstate_trans__in=transs)
    q1,q2=Q(isinitialstate__in=transs),Q(isfinalstate__in=transs)
    return StatesMolecules.objects.filter(q1|q2).distinct()
    



def setupResults(sql):
#    LOG(sql)
    q=where2q(sql.where,RESTRICTABLES)
#    LOG(q)
    try: q=eval(q)
    except: return {}
#    q=RadiativeTransitions.molecularchemicalspecies__exact='NH3'
    transs = RadiativeTransitions.objects.select_related(depth=2).filter(q)
#    transs = RadiativeTransitions.objects.filter(molecularchemicalspecies__exact='NH3').filter(frequencyvalue__gt=29500).filter(frequencyvalue__lt=130000)
#    transs = RadiativeTransitions.objects.select_related(depth=2).filter(molecularchemicalspecies='CO') #, frequencyvalue>29500, frequencyvalue<130000)
#    LOG(transs)
    sources = getCDMSsources(transs)
    states = getCDMSstates(transs)

#    qn= states[0].molecularquantumnumbers_set.all()
    qn = states[0].quantumnumbers.all()
    return {'RadTrans':transs,
            'MoleStates':states,
            'Sources':sources,
            }


