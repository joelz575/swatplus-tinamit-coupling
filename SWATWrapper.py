import os
import shutil
import socket
import subprocess
import tempfile
import time
from distutils.dir_util import copy_tree

import numpy as np

from tinamit.config import _
from tinamit.envolt.bf import ModeloBF
from tinamit.mod import VariablesMod
from tinamit_idm.puertos import IDMEnchufes

from _vars import gen_variables_swatp


class ModeloSWATPlus(ModeloBF):
    def __init__(símismo, archivo, nombre='SWATPlus', connectar=True):
        # Buscar la ubicación del modelo SWATPlus.
        símismo.exe_SWATPlus = símismo.obt_conf(
            'exe',
            cond=os.path.isfile,
            mnsj_err=_(
                '\nDebes especificar la ubicación del ejecutable SWATPlus, p. ej.'
                '\n\tModeloSWATPlus.estab_conf("exe", "C:\\Camino\\hacia\\mi\\SWATPlus.exe")'
                '\npara poder hacer simulaciones con modelos SWATPlus.'
                '\nSi no instalaste SWATPlus, lo puedes conseguir para Linux, Mac o Windows de '
                'https://github.com/joelz575/swatplus.'
            ))

        símismo.HUÉSPED = socket.gethostbyname(socket.gethostname())
        símismo.archivo = archivo
        print(archivo)
        símismo.variables = gen_variables_swatp()
        variablesMod = VariablesMod(variables=símismo.variables)
        símismo.connectar = connectar

        if connectar:
            símismo.servidor = IDMEnchufes()

        super().__init__(nombre=nombre, variables=variablesMod)

    def iniciar_modelo(símismo, corrida):
        if símismo.connectar:
            símismo.direc_trabajo = tempfile.mkdtemp('_' + str(hash(corrida)))
            copy_tree(símismo.archivo, símismo.direc_trabajo)

            if corrida.t.f_inic is None:
                raise ValueError('A start date is necessary when using SWAT+')
            super().iniciar_modelo(corrida=corrida)

            # iniciate SWATPlus Model
            símismo.proc = subprocess.Popen(
                [símismo.obt_conf('exe'), str(símismo.servidor.puerto), símismo.servidor.dirección],
                cwd=símismo.direc_trabajo
            )
            símismo.servidor.activar()

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
            # Mandar los valores nuevas a SWATPlus
            for var in rebanada.resultados:
                print("var: " + str(var))
                if var.var.ingr:
                    if (str(var) == 'agrl_km2'):
                        símismo.deter_área()
                        land_use = np.array(símismo.servidor.recibir(("luse")), dtype=int)
                        agrl_indexes = np.where(np.isin(land_use, símismo.agrl_uses), 1, 0)
                        nagrl_indexes = np.where(agrl_indexes, 0, 1)
                        nagrl_areas = nagrl_indexes * símismo.área_de_tierra
                        agrl_areas = agrl_indexes * símismo.área_de_tierra
                        agrl_area = np.sum(agrl_areas)
                        change_index = np.full(land_use.shape, False)
                        diff = agrl_area - var.var.obt_val()
                        matrix_to_change = agrl_areas if diff > 0 else nagrl_areas
                        min_area = np.min(matrix_to_change[matrix_to_change > 0])
                        while diff > min_area:
                            diff_hru = np.abs(matrix_to_change - diff)
                            min_difference_index = np.argmin(diff_hru[~change_index])
                            diff -= matrix_to_change[min_difference_index]
                            change_index[min_difference_index] = True
                        choices, frq = np.unique(land_use[agrl_indexes if diff > 0 else nagrl_indexes], return_counts=True)
                        choice = np.random.choice(choices, np.sum(change_index), p=frq/np.sum(frq))
                        land_use[change_index] = choice
                        símismo.servidor.cambiar('luse', land_use)
                    else:
                        símismo.servidor.cambiar(str(var), var.var.obt_val())

            # Correr un paso de simulaccion
            símismo.servidor.incrementar(rebanada.n_pasos)
            # Obtiene los valores de eso paso de la simulaccion
            for var in rebanada.resultados:
                if var.var.egr:
                    resultados = símismo.servidor.recibir(str(var))
                    símismo.variables[str(var)].poner_val(resultados)

            super().incrementar(rebanada=rebanada)
            print("DONE INCREMENTAR")

    def paralelizable(símismo):
        return True

    def deter_uso_de_tierra(símismo):
        with open(símismo.archivo + '/landuse.lum', 'r') as archivo_uso_de_tierra:
            counter = 0
            for line in archivo_uso_de_tierra:
                if 1 < counter:
                    split_line = line.split(' ')
                    uso_de_tierra = split_line[0]
                    print("Landuse: " + uso_de_tierra + "\tNumber: " + str(counter - 1))
                counter += 1
 #ToDo: fix the naming please :( AND THE open() statement
    def deter_área(símismo):
        símismo.archivo_uso_de_tierra = open(símismo.archivo + '/hru.con', 'r')
        símismo.área_de_tierra = []
        counter = 0
        for line in símismo.archivo_uso_de_tierra:
            if 1 < counter:
                split_line = line.split('    ')
                area = split_line[6]
                símismo.área_de_tierra.append(float(area))
                print("Area: " + area + "\tHRU Number: " + str(counter))
            counter += 1
        símismo.archivo_uso_de_tierra.close()

    def add_luses(símismo, uses: [], classification='AGRL'):
        if classification == 'AGRL':
            símismo.agrl_uses = uses

    def cerrar(símismo):
        # close model
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
