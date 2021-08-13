import os
import shutil
import socket
import subprocess

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
        return 'dias'

    def incrementar(símismo, rebanada):
        if símismo.connectar:
            # Mandar los valores nuevas a SWATPlus
            for var in rebanada.resultados:
                print("var: " + var)
                # check for special variable
                símismo.servidor.cambiar(var.var, var.var.obt_val())

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
        símismo.archivo_uso_de_tierra = open(símismo.direc_trabajo + '\\landuse.lum', 'r')
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
