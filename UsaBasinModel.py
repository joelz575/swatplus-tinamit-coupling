from matplotlib import pyplot as plt
from tinamit.conect import Conectado
from tinamit.envolt.mds.pysd import ModeloPySD
from tinamit.tiempo import EspecTiempo
from tinamit.unids import agregar_trad, nueva_unidad, agregar_sinónimos

from SWATWrapper import ModeloSWATPlus

ModeloSWATPlus.estab_conf('exe', '/home/joelz/PycharmProjects/swatplus/build/bin/swatplus_exe')
#nueva_unidad(unid='year', ref='years', conv=1)
agregar_sinónimos('año', "años", leng='es')
agregar_trad('años', 'year', leng_trad='en', leng_orig='es')
swatPlus = ModeloSWATPlus('Usa_Basin_model', lte_hru=False, cha=False, sd_ch=True)
vensim = ModeloPySD("vensim usa model.mdl")
modelo = Conectado(swatPlus, vensim)

modelo.conectar('Agricultural Land', 'agrl_ha', True)
modelo.conectar('"Banana Yields (SWAT+)"', '2_yield', False)
modelo.conectar('"Corn Yields (SWAT+)"', '4_yield', False)
modelo.conectar('Runnoff into channels', 'total_ch_out_y%flo', False)
modelo.conectar('"Banana Cultivation Area (SWAT+)"', 'banana_land_use_area', False)
modelo.conectar('"Corn Cultivation Area (SWAT+)"', 'corn_land_use_area', False)
swatPlus.deter_uso_de_tierra()
swatPlus.add_luses([2,3,7,8,9])

res_conex =modelo.simular(EspecTiempo(10, '2006-1-1'))

# Visualizar
f, ((eje1, eje2), (eje3, eje4), (eje5, eje6)) = plt.subplots(3, 2)
eje1.plot(res_conex['mds']['Agricultural Land'].vals)
eje1.set_title('Agricultural Land (ha)')

eje2.plot(res_conex['SWATPlus']['total_ch_out_y%no3'].vals/res_conex['SWATPlus']['total_ch_out_y%flo'].vals)
eje2.set_title('Channel NO3-N Concentration Outflow (kg/m^3)')

eje3.plot(res_conex['mds']['"Banana Yields (SWAT+)"'].vals)
eje3.set_title('Banana Yield (t)')

eje4.plot(res_conex['mds']['"Corn Yields (SWAT+)"'].vals)
eje4.set_title('Corn Yield (t)')

eje5.plot(res_conex['mds']['"Banana Cultivation Area (SWAT+)"'].vals)
eje5.set_title('Banana Cultivation Area (ha)')
eje5.set_xlabel('Years')

eje6.plot(res_conex['mds']['"Corn Cultivation Area (SWAT+)"'].vals)
eje6.set_title('Corn Cultivation Area (ha)')
eje6.set_xlabel('Years')

#eje1.ticklabel_format(axis='y', style='sci', scilimits=(0,0))

plt.show()
