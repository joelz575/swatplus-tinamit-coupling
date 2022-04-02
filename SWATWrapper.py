import os
import shutil
import socket
import subprocess
import tempfile
import numpy as np

from distutils.dir_util import copy_tree
from tinamit.config import _ as ERR
from tinamit.envolt.bf import ModeloBF
from tinamit.mod import VariablesMod
from tinamit_idm.puertos import IDMEnchufes

from _vars import gen_variables_swatp


class ModeloSWATPlus(ModeloBF):
    def __init__(símismo, archivo, nombre='SWATPlus', connectar=True, hru=True, cha=True, lte_hru=False, sd_ch=False):
        # EN:   Initializing wrapper variables
        # ES:   Inicialización de variables contenedoras
        símismo.archivo = archivo
        símismo.proc = None
        símismo.área_de_hrus = []
        símismo.direc_trabajo = None

        # EN:   Confirming that the location of the SWAT+ executable has been specified
        # ES:   Confirmar la ubicación del modelo SWAT+
        símismo.exe_SWATPlus = símismo.obt_conf(
            'exe',
            cond=os.path.isfile,
            mnsj_err=ERR(
                '\nDebes especificar la ubicación del ejecutable SWATPlus, p. ej.'
                '\n\tModeloSWATPlus.estab_conf("exe", "C:\\Camino\\hacia\\mi\\SWATPlus.exe")'
                '\npara poder hacer simulaciones con modelos SWATPlus.'
                '\nSi no instalaste SWATPlus, lo puedes conseguir para Linux, Mac o Windows de '
                'https://github.com/joelz575/swatplus.'
            ))

        # EN:   Initializing variables necessary for coupling
        # ES:   Inicialización de variables necesarias para el acoplamiento
        símismo.HUÉSPED = socket.gethostbyname(socket.gethostname())
        símismo.connectar = connectar
        if connectar:
            símismo.servidor = IDMEnchufes()

        # EN:   Getting the initial values of SWAT+ model variables and passing them to the superclass constructor
        # ES:   Obtener los valores iniciales de las variables del modelo SWAT+ y pasarlos al constructor de superclase
        símismo.variables = gen_variables_swatp(símismo.archivo, símismo.obt_conf("exe"), hru, cha, lte_hru, sd_ch)
        variables_modelo = VariablesMod(variables=símismo.variables)
        super().__init__(nombre=nombre, variables=variables_modelo)

    def iniciar_modelo(símismo, corrida):
        if símismo.connectar:
            símismo.direc_trabajo = tempfile.mkdtemp('_' + str(hash(corrida)))
            copy_tree(símismo.archivo, símismo.direc_trabajo)

            if corrida.t.f_inic is None:
                raise ValueError('A start date is necessary when using SWAT+')
            super().iniciar_modelo(corrida=corrida)

            # EN:   Starting the SWAT+ model
            # ES:   Inicio del modelo SWAT+
            símismo.proc = subprocess.Popen(
                [símismo.obt_conf('exe'), str(símismo.servidor.puerto), símismo.servidor.dirección],
                cwd=símismo.direc_trabajo
            )
            símismo.servidor.activar()

            # EN:   More variable inicialization
            # ES:   Mas de inicialización de variables
            símismo.deter_área()

        # EN:   Without connection
        # ES:   Sin acoplamiento
        else:
            símismo.direc_trabajo = shutil.copytree(símismo.archivo, '_' + str(hash(corrida)))
            símismo.proc = subprocess.Popen(
                [símismo.obt_conf('exe')],
                cwd=símismo.direc_trabajo
            )

    def unidad_tiempo(símismo):
        return 'day'

    def incrementar(símismo, rebanada):
        if símismo.connectar:
            # EN:   Getting the newest values from SWAT+
            # ES:   Mandar los valores nuevas a SWAT+
            for var in rebanada.resultados:
                print("var: " + str(var))
                if var.var.ingr:
                    if str(var) == 'agrl_ha':
                        usos_de_tierra = np.array(símismo.servidor.recibir("luse"), dtype=int)
                        agrl_indexes = np.where(np.isin(usos_de_tierra, símismo.agrl_usos), 1, 0)
                        nagrl_indexes = np.where(agrl_indexes == 1, 0, 1)
                        nagrl_areas = nagrl_indexes * símismo.área_de_hrus
                        agrl_areas = agrl_indexes * símismo.área_de_hrus
                        agrl_area = np.sum(agrl_areas)
                        change_index = np.full(usos_de_tierra.shape, False)
                        diff = agrl_area - var.var.obt_val()
                        matrix_to_change = agrl_areas if diff > 0 else nagrl_areas
                        min_area = np.min(matrix_to_change[matrix_to_change > 0])
                        abs_diff = abs(diff)
                        while abs_diff > min_area:
                            diff_hru = np.abs(matrix_to_change - abs_diff)
                            min_difference_index = np.argmin(diff_hru)
                            abs_diff -= matrix_to_change[min_difference_index]
                            if not change_index[min_difference_index]:
                                change_index[min_difference_index] = True
                            else:
                                break
                        choices, frq = np.unique(usos_de_tierra[nagrl_indexes == 1 if diff > 0 else agrl_indexes == 1],
                                                 return_counts=True)
                        choice = np.random.choice(choices, np.sum(change_index), p=frq / np.sum(frq))
                        usos_de_tierra[change_index] = choice
                        símismo.servidor.cambiar('luse', usos_de_tierra)
                    else:
                        símismo.servidor.cambiar(str(var), var.var.obt_val())

            # EN:   Running a time-step of the simulation
            # ES:   Correr un paso de simulaccion
            símismo.servidor.incrementar(rebanada.n_pasos)

            # EN:   Getting the current variable values for this time-step of simulation
            # ES:   Obtiene los valores de eso paso de la simulaccion
            for var in rebanada.resultados:
                if var.var.egr and str(var) not in ['2_yield', '4_yield', 'banana_land_use_area', 'corn_land_use_area']:
                    resultados = símismo.servidor.recibir(str(var))
                    símismo.variables[str(var)].poner_val(resultados)
                elif var.var.egr and str(var) in ['2_yield', '4_yield']:
                    resultados = símismo.servidor.recibir('bsn_crop_yld')[int(str(var)[0]) - 1]
                    símismo.variables[str(var)].poner_val(resultados)
                elif var.var.egr and str(var) == 'banana_land_use_area':
                    resultados = np.sum(símismo.área_de_hrus * np.where(np.isin(usos_de_tierra, [2, 3]), 1, 0))
                    símismo.variables[str(var)].poner_val(resultados)
                elif var.var.egr and str(var) == 'corn_land_use_area':
                    resultados = np.sum(símismo.área_de_hrus * np.where(np.isin(usos_de_tierra, [3, 7, 8]), 1, 0))
                    símismo.variables[str(var)].poner_val(resultados)

            super().incrementar(rebanada=rebanada)
            print("DONE INCREMENTAR")

    def paralelizable(símismo):
        return True

    # EN:   Closing the model
    # ES:   Cerrar el modelo
    def cerrar(símismo):
        shutil.rmtree(símismo.direc_trabajo, ignore_errors=True)
        if símismo.connectar:
            símismo.servidor.cerrar()
            símismo.proc.kill()

    def cambiar_vals(símismo, valores):
        super().cambiar_vals(valores)

    def _correr_hasta_final(símismo):
        if símismo.connectar:
            símismo.servidor.finalizar()
        return None

    def instalado(cls):
        return cls.obt_conf('exe') is not None

# ----------------------------------------------------------------------------------------------------------------------
# EN:   Utility functions not required by Tinamït but likely useful in coupling of many SWAT+ models.
# ES:   Funciones de utilidad no requeridas por Tinamït, pero probablemente útiles en el acoplamiento de muchos
#       modelos SWAT+.

    # EN:   Prints landuse types and their corresponding numerical value
    # ES:   Imprime los tipos de uso de la tierra y su correspondiente valor numérico
    def deter_uso_de_tierra(símismo):
        with open(símismo.archivo + '/landuse.lum', 'r') as archivo_uso_de_tierra:
            index = 0
            for line in archivo_uso_de_tierra:
                if 1 < index:
                    split_line = line.split(' ')
                    uso_de_tierra = split_line[0]
                    print("Landuse: " + uso_de_tierra + "\tNumber: " + str(index - 1))
                index += 1

    # EN:   Reads SWAT+ input file "hru.con" to store the size of all the HRU's
    # ES:   Lee el archivo de entrada SWAT+ "hru.con" para almacenar el tamaño de todas las HRU
    def deter_área(símismo):
        with open(símismo.archivo + '/hru.con', 'r') as símismo.archivo_hru:
            index = 0
            for line in símismo.archivo_hru:
                if 1 < index:
                    split_line = line.split('    ')
                    area = split_line[6]
                    símismo.área_de_hrus.append(float(area))
                index += 1

    # EN:   Allows grouping of landuses into specific landuse types
    # ES:   Permite agrupar los landuses en tipos específicos de landuse
    def agrupar_usos_del_suelo(símismo, usos: [], clas='AGRL'):
        if clas == 'AGRL':
            símismo.agrl_usos = usos
