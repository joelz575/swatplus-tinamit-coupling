import os
import numpy as np
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

# EN:   Number of years of simulation
simulation_years = 10
model_runs = 3


# EN:   Preparing for visualization of results
# ES:   Preparación para la visualización de los resultados
f, ((graph1, graph2), (graph3, graph4), (graph5, graph6)) = plt.subplots(3, 2)
line_styles = ["solid", "dashed", "dotted"]
line_color = ["purple", "green", "red"]
fill_color = ["violet", "springgreen", "salmon"]
fill_styles = ['/', '|', 'X']

# EN:   Specifying SWAT+ model executable to be used
# ES:   Especificación del ejecutable del modelo SWAT+ que se va a utilizar
BASE_DIR = os.path.split(os.path.split(__file__)[0])[0]
swat_exe = os.path.join(BASE_DIR, "swatplus/build/bin/swatplus_exe")
ModeloSWATPlus.estab_conf('exe', swat_exe)

# EN:   Adding 'year' to the Tinamït dictionary since the Vensim model is in English
# ES:   Añadir 'año' al diccionario Tinamït ya que el modelo Vensim está en inglés
agregar_trad('año', 'year', leng_trad='en', leng_orig='es', guardar=True)

# EN:   Initializing vensim model wrappers for multiple scenarios
# ES:   Inicialización de contenedores de modelos vensim para varios escenarios
vensim = [ModeloPySD("BaseLineScenario.mdl"), ModeloPySD("45SubsidyScenario.mdl"),
          ModeloPySD("90HighSubsidyScenario.mdl")]

for counter in range(3):
    # tracking which model is used in simulation and which line-style will be used in graphing
    style = line_styles[counter]
    sdModel = vensim[counter]

    # initializing result and graphing
    agricultural_land = np.zeros((model_runs, simulation_years+1, 1))
    no3_concentration = np.zeros((model_runs, simulation_years+1, 1))
    banana_production = np.zeros((model_runs, simulation_years+1, 1))
    corn_production = np.zeros((model_runs, simulation_years+1, 1))
    banana_area = np.zeros((model_runs, simulation_years+1, 1))
    corn_area = np.zeros((model_runs, simulation_years+1, 1))
    agricultural_land_mean = np.zeros(simulation_years+1)
    agricultural_land_std = np.zeros(simulation_years+1)
    no3_concentration_mean = np.zeros(simulation_years+1)
    no3_concentration_std = np.zeros(simulation_years+1)
    banana_production_mean = np.zeros(simulation_years+1)
    banana_production_std = np.zeros(simulation_years+1)
    corn_production_mean = np.zeros(simulation_years+1)
    corn_production_std = np.zeros(simulation_years+1)
    banana_area_mean = np.zeros(simulation_years+1)
    banana_area_std = np.zeros(simulation_years+1)
    corn_area_mean = np.zeros(simulation_years+1)
    corn_area_std = np.zeros(simulation_years+1)

    for run in range(model_runs):

        # EN:   Creating SWAT+ model instance and grouping landuses
        # *HINT*: users might first want to use imprimir_usos_de_tierra() to know which landuse the numerals refer to
        # ES:   Creación de instancias de modelo SWAT + y agrupación de usos terrestres
        # *SUGERENCIA*: es posible que los usuarios primero deseen usar imprimir_usos_de_tierra() para saber a qué uso
        # de la tierra se refieren los números
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
        results = coupledModel.simular(EspecTiempo(simulation_years, '2006-1-1'))
        agricultural_land[run] = results['mds']['Agricultural Land'].vals
        no3_concentration[run] = (1000 * results['SWATPlus']['total_ch_out_y%no3'].vals /
                             results['SWATPlus']['total_ch_out_y%flo'].vals / 86400)
        banana_production[run] = results['mds']['"Banana Yields (SWAT+)"'].vals
        corn_production[run] = results['mds']['"Corn Yields (SWAT+)"'].vals
        banana_area[run] = results['mds']['"Banana Cultivation Area (SWAT+)"'].vals
        corn_area[run] = results['mds']['"Corn Cultivation Area (SWAT+)"'].vals

        if run is model_runs-1:
            year = 0
            while year <= simulation_years:
                agricultural_land_mean[year] = sum(agricultural_land[i][year] for i in range(model_runs))/model_runs
                agricultural_land_std[year] = np.std([run[year] for run in agricultural_land])
                no3_concentration_mean[year] = sum(no3_concentration[i][year] for i in range(model_runs))/model_runs
                no3_concentration_std[year] = np.std([run[year] for run in no3_concentration])
                banana_production_mean[year] = sum(banana_production[i][year] for i in range(model_runs))/model_runs
                banana_production_std[year] = np.std([run[year] for run in banana_production])
                corn_production_mean[year] = sum(corn_production[i][year] for i in range(model_runs))/model_runs
                corn_production_std[year] = np.std([run[year] for run in corn_production])
                banana_area_mean[year] = sum(banana_area[i][year] for i in range(model_runs))/model_runs
                banana_area_std[year] = np.std([run[year] for run in banana_area])
                corn_area_mean[year] = sum(corn_area[i][year] for i in range(model_runs))/model_runs
                corn_area_std[year] = np.std([run[year] for run in corn_area])
                year += 1

    # EN:   Graphing the results
    # ES:   Graficación de los resultados
    graph1.fill_between(range(simulation_years+1), agricultural_land_mean + agricultural_land_std,
                        agricultural_land_mean - agricultural_land_std, hatch=fill_styles[counter],
                        color=fill_color[counter], alpha=0.3)
    graph1.plot(agricultural_land_mean, linestyle=style, linewidth=3, color=line_color[counter])
    graph1.set_title('Agricultural Land', fontweight='bold')
    graph1.set_ylabel('Area (ha)', fontweight='bold')
    graph1.grid(True)

    graph2.fill_between(range(simulation_years+1), no3_concentration_mean + no3_concentration_std,
                        no3_concentration_mean - no3_concentration_std, hatch=fill_styles[counter],
                        color=fill_color[counter], alpha=0.3)
    graph2.plot(no3_concentration_mean, linestyle=style, linewidth=3, color=line_color[counter])
    graph2.set_title('Channel Nitrate-Nitrogen', fontweight='bold')
    graph2.set_ylabel('Average Concentration (mg/L)', fontweight='bold')
    graph2.grid(True)

    graph3.fill_between(range(simulation_years+1), banana_production_mean + banana_production_std,
                        banana_production_mean - banana_production_std, hatch=fill_styles[counter],
                        color=fill_color[counter], alpha=0.3)
    graph3.plot(banana_production_mean, linestyle=style, linewidth=3, color=line_color[counter])
    graph3.set_title('Banana',fontsize=13, fontweight='bold')
    graph3.set_ylabel('Yield (t)', fontweight='bold')
    graph3.grid(True)

    graph4.fill_between(range(simulation_years+1), corn_production_mean + corn_production_std,
                        corn_production_mean - corn_production_std, hatch=fill_styles[counter],
                        color=fill_color[counter], alpha=0.3)
    graph4.plot(corn_production_mean, linestyle=style, linewidth=3, color=line_color[counter])
    graph4.set_title('Corn',fontsize=13, fontweight='bold')
    graph4.set_ylabel('Yield (t)', fontweight='bold')
    graph4.grid(True)

    graph5.fill_between(range(simulation_years+1), banana_area_mean + banana_area_std,
                        banana_area_mean - banana_area_std, hatch=fill_styles[counter], color=fill_color[counter],
                        alpha=0.3)
    graph5.plot(banana_area_mean, linestyle=style, linewidth=3, color=line_color[counter])
    graph5.set_ylabel('Cultivation Area (ha)', fontweight='bold')
    graph5.set_xlabel('Years', fontweight='bold')
    graph5.grid(True)

    graph6.fill_between(range(simulation_years+1), corn_area_mean + corn_area_std,
                        corn_area_mean - corn_area_std, hatch=fill_styles[counter], color=fill_color[counter],
                        alpha=0.3)
    graph6.plot(corn_area_mean, linestyle=style, linewidth=3, color=line_color[counter])
    graph6.set_ylabel('Cultivation Area (ha)', fontweight='bold')
    graph6.set_xlabel('Years', fontweight='bold')
    graph6.grid(True)
plt.subplot(3, 2, 1)
plt.legend(["No-Subsidy-Scenario", "45%-Subsidy-Scenario", "90%-Subsidy-Scenario"])
plt.show()
