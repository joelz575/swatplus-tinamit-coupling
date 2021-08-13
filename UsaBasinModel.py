from tinamit.conect import Conectado
from tinamit.envolt.mds.pysd import ModeloPySD
from tinamit.tiempo import EspecTiempo
from tinamit.unids import agregar_trad

from SWATWrapper import ModeloSWATPlus

ModeloSWATPlus.estab_conf('exe', '../swatplus/build/bin/swatplus_exe.exe')
agregar_trad('año', 'year', leng_trad='en', leng_orig='es')
swatPlus = ModeloSWATPlus('Usa-Basin-Model')
vensim = ModeloPySD("C:/Users/Joel/Documents/Prof Adamowski/SWAT+ Test Model/vensim usa model.mdl")
modelo = Conectado(swatPlus, vensim)

modelo.conectar('Agricultural Land', 'agrl_km2', True)
modelo.conectar("Non-Agricultural Land", "nagrl_km2", True)

modelo.simular(EspecTiempo())
