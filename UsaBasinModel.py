from tinamit.conect import Conectado
from tinamit.envolt.mds.pysd import ModeloPySD
from tinamit.tiempo import EspecTiempo
from tinamit.unids import agregar_trad, nueva_unidad, agregar_sinónimos

from SWATWrapper import ModeloSWATPlus

ModeloSWATPlus.estab_conf('exe', '/home/joelz/PycharmProjects/swatplus/build/bin/swatplus_exe')
#nueva_unidad(unid='year', ref='years', conv=1)
agregar_sinónimos('año', "años", leng='es')
agregar_trad('años', 'year', leng_trad='en', leng_orig='es')
swatPlus = ModeloSWATPlus('Usa-Basin-Model', lte_hru=False, cha=False, sd_ch=True)
vensim = ModeloPySD("vensim usa model.mdl")
modelo = Conectado(swatPlus, vensim)

modelo.conectar('Agricultural Land', 'agrl_ha', True)
modelo.conectar('"Banana Yields (SWAT+)"', '2_yield', False)
modelo.conectar('"Corn Yields (SWAT+)"', '4_yield', False)
modelo.conectar('Runnoff into channels', 'total_aqu_a%flo_cha', False)
swatPlus.deter_uso_de_tierra()
swatPlus.add_luses([2,3,5,6,7,8,9,10,11])
modelo.simular(EspecTiempo(10, '2006-1-1'))
