import os
import shutil
import socket
import subprocess
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

            símismo.direc_trabajo = shutil.copytree(símismo.archivo, '_' + str(hash(corrida)))

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
                if (str(var) == 'agrl_km2'):
                    símismo.deter_área()
                    land_use = np.array(símismo.servidor.recibir(("luse")))
                    agrl_indexes = np.where(np.isin(land_use, símismo.agrl_uses), 1, 0)
                    nagrl_indexes = np.where(agrl_indexes, 0, 1)
                    agrl_area = np.sum(agrl_indexes * símismo.área_de_tierra)
                    change_index = []
                    if agrl_area - var.var.obt_val() > 0:
                        agrl_areas = [agrl_indexes[i] * [int(f) for f in símismo.área_de_tierra][i] for i in
                                      range(len(agrl_indexes))]

                        for i in range(len(agrl_areas)):
                            #trying with changing only one hru
                            if agrl_areas[i] > (agrl_area - var.var.obt_val())/2 and agrl_areas[i] < (agrl_area - var.var.obt_val())*1.5:
                                change_index.append(i)
                                break
                            #trying with changing multiple hru's
                            elif agrl_areas[i] < agrl_area - var.var.obt_val():
                                change_index.append(i)
                                agrl_area += agrl_areas[i]

                    for i in change_index:
                        closest = 0
                        for f in range(len(land_use)):
                            if (land_use[f] not in símismo.agrl_uses) and abs(i-f) < abs(i-closest):
                                closest = f

                        land_use[i] = land_use[closest]
                    símismo.servidor.cambiar('luse', land_use)
                else:
                    símismo.servidor.cambiar(str(var), var.var.obt_val())

            # Correr un paso de simulaccion
            símismo.servidor.incrementar(rebanada.n_pasos)

            # Obtiene los valores de eso paso de la simulaccion
            for var in rebanada.resultados:
                símismo.variables[str(var)].poner_val(símismo.servidor.recibir(var.var))

            super().incrementar(rebanada=rebanada)
            print("DONE INCREMENTAR")

    def paralelizable(símismo):
        return True

    def deter_uso_de_tierra(símismo):
        símismo.archivo_uso_de_tierra = open(símismo.archivo + '/landuse.lum', 'r')
        símismo.uso_de_tierra = []
        counter = 0
        for line in símismo.archivo_uso_de_tierra:
            if 1 < counter:
                split_line = line.split(' ')
                uso_de_tierra = split_line[0]
                símismo.uso_de_tierra.append(uso_de_tierra)
                print("Landuse: " + uso_de_tierra + "\tNumber: " + str(counter - 1))
            counter += 1
        símismo.archivo_uso_de_tierra.close()

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
        if símismo.connectar:
            símismo.servidor.cerrar()
            símismo.proc.kill()
            shutil.rmtree(símismo.direc_trabajo, ignore_errors=True)

    def cambiar_vals(símismo, valores):
        super().cambiar_vals(valores)

    def _correr_hasta_final(símismo):
        if símismo.connectar:
            símismo.servidor.finalizar()
        return None

    def instalado(cls):
        return cls.obt_conf('exe') is not None
