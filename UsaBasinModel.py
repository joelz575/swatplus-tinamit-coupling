from matplotlib import pyplot as plt
# EN:   Tinamït imports
# ES:   Importaciones de Tinamït
from tinamit.conect import Conectado
from tinamit.envolt.mds.pysd import ModeloPySD
from tinamit.tiempo import EspecTiempo
from tinamit.unids import agregar_trad

# EN:   Importing the wrapper class
# ES:   Importación de la clase contenedora
from SWATWrapper import ModeloSWATPlus

# EN:   Preparing for visualization of results
# ES:   Preparación para la visualización de los resultados
f, ((graph1, graph2), (graph3, graph4), (graph5, graph6)) = plt.subplots(3, 2)
line_styles = ["solid", "dashed", "dotted"]

# EN:   Specifying SWAT+ model executable to be used
# ES:   Especificación del ejecutable del modelo SWAT+ que se va a utilizar
ModeloSWATPlus.estab_conf('exe', '/home/joelz/PycharmProjects/swatplus/build/bin/swatplus_exe')

# EN:   Adding 'year' to the Tinamït dictionary since the Vensim model is in English
# ES:   Añadir 'año' al diccionario Tinamït ya que el modelo Vensim está en inglés
agregar_trad('año', 'year', leng_trad='en', leng_orig='es')

# EN:   Initializing vensim model wrappers for multiple scenarios
# ES:   Inicialización de contenedores de modelos vensim para varios escenarios
vensim = [ModeloPySD("BaseLineScenario.mdl"), ModeloPySD("45SubsidyScenario.mdl"),
          ModeloPySD("90HighSubsidyScenario.mdl")]

for counter in range(3):
    style = line_styles[counter]
    sdModel = vensim[counter]

    # EN:   Creating SWAT+ model instance and grouping landuses
    # *HINT*: users might first want to use print_landuse_types() to know which landuse the numerals refer to
    # ES:   Creación de instancias de modelo SWAT + y agrupación de usos terrestres
    # *SUGERENCIA*: es posible que los usuarios primero deseen usar print_landuse_types() para saber a qué uso de la
    # tierra se refieren los números
    swatPlus = ModeloSWATPlus('Usa_Basin_model', lte_hru=False, cha=False, sd_ch=True)
    swatPlus.agrupar_usos_del_suelo([2, 3, 7, 8, 9])

    # EN:   Coupled model creation and connecting variables
    # ES:   Creación de modelos acoplados y conexión de variables
    coupledModel = Conectado(swatPlus, sdModel)
    coupledModel.conectar('Agricultural Land', 'agrl_ha', True)
    coupledModel.conectar('"Banana Yields (SWAT+)"', '2_yield', False)
    coupledModel.conectar('"Corn Yields (SWAT+)"', '4_yield', False)
    coupledModel.conectar('Runnoff into channels', 'total_ch_out_y%flo', False)
    coupledModel.conectar('"Banana Cultivation Area (SWAT+)"', 'banana_land_use_area', False)
    coupledModel.conectar('"Corn Cultivation Area (SWAT+)"', 'corn_land_use_area', False)

    # EN:   Running the coupled model simulation
    # ES:   Ejecución de la simulación del modelo acoplado
    results = coupledModel.simular(EspecTiempo(10, '2006-1-1'))

    # EN:   Graphing the results
    # ES:   Graficación de los resultados
    graph1.plot(results['mds']['Agricultural Land'].vals, linestyle=style, linewidth=3)
    graph1.set_title('Agricultural Land (ha)')
    graph1.grid(True)

    graph2.plot(1000 * results['SWATPlus']['total_ch_out_y%no3'].vals / results['SWATPlus'][
        'total_ch_out_y%flo'].vals / 86400, linestyle=style, linewidth=3)
    graph2.set_title('Average Channel NO3-N Concentration (mg/L)')
    graph2.grid(True)

    graph3.plot(results['mds']['"Banana Yields (SWAT+)"'].vals, linestyle=style, linewidth=3)
    graph3.set_title('Banana Yield (t)')
    graph3.grid(True)

    graph4.plot(results['mds']['"Corn Yields (SWAT+)"'].vals, linestyle=style, linewidth=3)
    graph4.set_title('Corn Yield (t)')
    graph4.grid(True)

    graph5.plot(results['mds']['"Banana Cultivation Area (SWAT+)"'].vals, linestyle=style, linewidth=3)
    graph5.set_title('Banana Cultivation Area (ha)')
    graph5.set_xlabel('Years')
    graph5.grid(True)

    graph6.plot(results['mds']['"Corn Cultivation Area (SWAT+)"'].vals, linestyle=style, linewidth=3)
    graph6.set_title('Corn Cultivation Area (ha)')
    graph6.set_xlabel('Years')
    graph6.grid(True)
plt.subplot(3, 2, 1)
plt.legend(["No-Subsidy-Scenario", "45%-Subsidy-Scenario", "90%-Subsidy-Scenario"])
plt.show()
