# -*- coding: utf-8 -*-

from vamdctap.caselessdict import CaselessDict

RETURNABLES = CaselessDict({\
'SourceID':'Source.id',
'SourceAuthorName':'Source.publications.all()[0].author',
'SourceCategory':'Source.publications.all()[0].category',
'SourcePageBegin':'Source.publications.all()[0].pages',
'SourcePageEnd':'Source.publications.all()[0].pages',
'SourceName':'Source.publications.all()[0].journal',
'SourceTitle':'Source.publications.all()[0].title',
'SourceURI':'Source.publications.all()[0].url',
'SourceVolume':'Source.publications.all()[0].volume',
'SourceYear':'Source.publications.all()[0].year',
'MethodID':'"MOBS"',
'MethodCategory':'"observed"',
'MethodDescription':'',
'AtomStateID':'AtomState.id',
'AtomSymbol':'AtomState.species.name',
'AtomNuclearCharge':'AtomState.species.atomic',
'AtomConfigurationLabel':'AtomState.charid',
'AtomCompositionComponentTerm':'AtomState.term',
'AtomIonizationEnergy':'AtomState.species.ionen',
'AtomStateLandeFactor':'AtomState.lande',
'AtomStateLandeFactorRef':'AtomState.lande_ref',
'AtomStateEnergy':'AtomState.energy',
'AtomStateEnergyRef':'AtomState.energy_ref',
'AtomStateEnergyUnits':'1/cm',
'AtomStateDescription':'',
'AtomIonCharge':'AtomState.species.ion',
'AtomMassNumber':'AtomState.species.massno',
'RadTransComments':'Wavelength is for vacuum.',
'RadTransWavelengthExperimentalValue':'RadTran.vacwave',
'RadTransWavelengthExperimentalUnits':u'\xc5',
'RadTransProbabilityLog10WeightedOscillatorStrengthAccuracy':'RadTran.accur',
'RadTransWavelengthExperimentalSourceRef':'RadTran.wave_ref',
'RadTransFinalStateRef':'RadTran.lostate.id',
'RadTransInitialStateRef':'RadTran.upstate.id',
'RadTransLogGF':'RadTran.loggf',
'RadTransMethodRef':'OBS',
'RadTransProbabilityLog10WeightedOscillatorStrengthSourceRef':'RadTran.loggf_ref',
'RadTransProbabilityLog10WeightedOscillatorStrengthValue':'RadTran.loggf',
'RadTransBroadRadGammaLog':'RadTran.gammarad',
'RadTransBroadRadRef':'RadTran.gammarad_ref',
'RadTransBroadStarkGammaLog':'RadTran.gammastark',
'RadTransBroadStarkRef':'RadTran.gammastark_ref',
'RadTransBroadWaalsGammaLog':'RadTran.gammawaals',
'RadTransBroadWaalsAlpha':'RadTran.alphawaals',
'RadTransBroadWaalsSigma':'RadTran.sigmawaals',
'RadTransBroadWaalsRef':'RadTran.waals_ref',
'RadTransEffLande':'RadTran.landeff',
'RadTransEffLandeRef':'RadTran.lande_ref',
})

RESTRICTABLES = CaselessDict({\
'AtomSymbol':'species__name',
'AtomNuclearCharge':'species__atomic',
'AtomStateEnergy':'upstate__energy',
'RadTransWavelengthExperimentalValue':'vacwave',
'RadTransLogGF':'loggf',
'AtomIonCharge':'species__ion',
})
