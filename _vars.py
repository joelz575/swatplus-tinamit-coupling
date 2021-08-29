import shutil
import subprocess
import tempfile
from distutils.dir_util import copy_tree

import numpy as np
from tinamit.mod import Variable
from tinamit_idm.puertos import IDMEnchufes


def gen_variables_swatp(archivo, exe, hru, cha, lte_hru, sd_ch) -> [Variable]:
    variables = []
    servidor = IDMEnchufes()
    direc_trabajo = tempfile.mkdtemp('_' + str(hash("init")))
    copy_tree(archivo, direc_trabajo)
    proc = subprocess.Popen(
        [exe, str(servidor.puerto), servidor.dirección],
        cwd=direc_trabajo
    )
    servidor.activar()
    for vr, info in _info_vars.items():
        if ((vr != 'agrl_ha' and vr != '2_yield' and vr != '4_yield' and vr != 'total_aqu_a%flo_cha') and
                ((info['type'] == 'hru' and hru) or (info['type'] == 'cha' and cha) or
                                  (info['type'] == 'lte_hru' and lte_hru) or (info['type'] == 'sd_ch' and sd_ch))):
            variables.append(Variable(
                nombre=vr, unid=info['unid'], ingr=info['ingr'], egr=info['egr'], inic=np.array(servidor.recibir(vr))
            ))
        elif (hru and (vr == 'agrl_ha' or vr == '2_yield' or vr == '4_yield' or vr == 'total_aqu_a%flo_cha')):
            variables.append(Variable(
                nombre=vr, unid=info['unid'], ingr=info['ingr'], egr=info['egr']))

    servidor.cerrar()
    proc.kill()
    shutil.rmtree(direc_trabajo, ignore_errors=True)
    return variables


# Un diccionario de variables SWAT+. Ver la documentación SWAT+ para más detalles.
_info_vars = {
    '2_yield':
        {'nombre': 'yield of plant 2 (banana in this example)', 'unid': 'tonne/ha', 'ingr': False,
         'egr': True, 'type': 'None'},
    '4_yield':
        {'nombre': 'yield of plant 4 (corn in this example)', 'unid': 'tonne/ha', 'ingr': False,
         'egr': True, 'type': 'None'},
    'bsn_crop_yld_aa':
        {'nombre': 'sum of yields by plants', 'unid': 'tonne/ha', 'ingr': False,
         'egr': True, 'type': 'hru'},
    'aqu_a%flo_cha':
        {'nombre': 'surface runoff flowing into channels', 'unid': 'm^3', 'ingr': False,
         'egr': True, 'type': 'hru'},
    'total_aqu_a%flo_cha':
        {'nombre': 'sum of surface runoff flowing into channels', 'unid': 'm^3', 'ingr': False,
         'egr': True, 'type': 'hru'},
    'agrl_ha':
        {'nombre': 'Area of Agricultural Land', 'unid': 'ha', 'ingr': True,
         'egr': False, 'type': 'None'},
    'sd_props':
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'sd_ch'},
    'sd_obj_no':
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'sd_ch'},
    'sd_aqu_link':
        {'nombre': "aquifer the channel is linked to", 'unid': '', 'ingr': False,
         'egr': True, 'type': 'sd_ch'},
    'sd_aqu_link_ch':
        {'nombre': 'sequential channel number in the aquifer', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'sd_ch'},
    'sd_chw':
        {'nombre': "channel width", 'unid': 'm', 'ingr': False,
         'egr': True, 'type': 'sd_ch'},
    'sd_chd':
        {'nombre': "channel depth", 'unid': 'm', 'ingr': False,
         'egr': True, 'type': 'sd_ch'},
    'sd_chs':
        {'nombre': "channel slope", 'unid': 'm/m', 'ingr': False,
         'egr': True, 'type': 'sd_ch'},
    'sd_chl':
        {'nombre': "channel length", 'unid': 'km', 'ingr': False,
         'egr': True, 'type': 'sd_ch'},
    'sd_chn':
        {'nombre': "channel Manning's n", 'unid': '', 'ingr': False,
         'egr': True, 'type': 'sd_ch'},
    'sd_cov':
        {'nombre': "channel cover factor", 'unid': '', 'ingr': False,
         'egr': True, 'type': 'sd_ch'},
    'sd_cherod':
        {'nombre': "channel erodibility", 'unid': '', 'ingr': False,
         'egr': True, 'type': 'sd_ch'},
    'sd_shear_bnk':
        {'nombre': "bank shear coefficient - fraction of bottom shear", 'unid': '', 'ingr': False,
         'egr': True, 'type': 'sd_ch'},
    'sd_hc_erod':
        {'nombre': "headcut erodibility", 'unid': '', 'ingr': False,
         'egr': True, 'type': 'sd_ch'},
    'sd_hc_co':
        {'nombre': "proportionality coefficient for head cut", 'unid': 'm/m', 'ingr': False,
         'egr': True, 'type': 'sd_ch'},
    'sd_hc_len':
        {'nombre': "length of head cut", 'unid': 'm', 'ingr': False,
         'egr': True, 'type': 'sd_ch'},
    'sd_hc_hgt':
        {'nombre': "headcut height", 'unid': 'm', 'ingr': False,
         'egr': True, 'type': 'sd_ch'},
    'sd_stor':
        {'nombre': "water stored in reach at end of the day", 'unid': 'm3', 'ingr': False,
         'egr': True, 'type': 'sd_ch'},
    'lte_props':
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    'lte_obj_no':
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    'lte_iplant':
        {'nombre': "plant number xwalked from hlt_db()%plant and plants.plt", 'unid': '',
         'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    'lte_km2':
        {'nombre': "drainage area", 'unid': 'km^2', 'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    'lte_cn2':
        {'nombre': "condition II curve number (used in calibration)", 'unid': '', 'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    'lte_cn3_swf':
        {'nombre': "soil water factor for cn3 (used in calibration)", 'unid': '', 'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    'lte_soildep':
        {'nombre': "soil profile depth", 'unid': 'mm', 'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    'lte_etco':
        {'nombre': "et coefficient - use with pet and aet (used in calibration)", 'unid': '',
         'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    'lte_revapc':
        {'nombre': "revap from aquifer (used in calibration)", 'unid': 'm/m', 'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    'lte_perco':
        {'nombre': "soil percolation coefficient (used in calibration)", 'unid': '',
         'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    'lte_tdrain':
        {'nombre': "design subsurface tile drain time (used in calibration)", 'unid': 'hr',
         'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    'lte_stress':
        {'nombre': "plant stress - pest, root restriction, soil quality, nutri", 'unid': 'frac',
         'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    'lte_uslefac':
        {'nombre': "USLE slope length factor", 'unid': '', 'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    'lte_wrt1':
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    'lte_wrt2':
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    'lte_smx':
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    'lte_hk':
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    'lte_yls':
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    'lte_ylc':
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    'lte_awc':
        {'nombre': "available water capacity of soil", 'unid': 'mm/mm', 'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    'lte_g':
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    'lte_hufh':
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    'lte_phu':
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    'lte_por':
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    'lte_sc':
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    'lte_sw':
        {'nombre': "initial soil water storage", 'unid': 'mm/mm', 'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    'lte_gw':
        {'nombre': "initial shallow aquifer storage", 'unid': 'mm', 'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    'lte_snow':
        {'nombre': "initial water content of snow", 'unid': 'mm', 'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    'lte_gwflow':
        {'nombre': "initial groundwater flow", 'unid': 'mm', 'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    'lte_dm':
        {'nombre': "plant biomass", 'unid': 't/ha', 'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    'lte_alai':
        {'nombre': "leaf area index", 'unid': '', 'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    'lte_yield':
        {'nombre': "plant yield", 'unid': 't/ha', 'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    'lte_npp':
        {'nombre': "net primary productivity", 'unid': 't/ha', 'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    'lte_lai_mx':
        {'nombre': "maximum leaf area index", 'unid': '', 'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    'lte_gwdeep':
        {'nombre': "deep aquifer storage", 'unid': 'mm', 'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    'lte_aet':
        {'nombre': "sum of actual et during growing season (for hi water stress)", 'unid': 'mm',
         'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    'lte_pet':
        {'nombre': "sum of potential et during growing season (for hi water stress)", 'unid': 'mm',
         'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    'lte_start':
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    'lte_end':
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'lte_hru'},
    "hru_land_use_mgt":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_land_use_mgt_c":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_lum_group":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_lum_group_c":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_region":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_plant_cov":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_mgt_ops":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_tiledrain":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_septic":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_fstrip":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_grassww":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_bmpuser":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_crop_reg":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_cur_op":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_strsa":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_luse%name":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_luse%cn_lu":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_luse%cons_prac":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_luse%usle_p":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_luse%urb_ro":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_luse%urb_lu":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_luse%ovn":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_dbs%name":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_dbs%topo":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_dbs%hyd":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_dbs%soil":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_dbs%land_use_mgt":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_dbs%soil_plant_in":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_dbs%surf_stor":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_dbs%snow":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_dbs%field":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_dbsc%name":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_dbsc%topo":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_dbsc%hyd":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_dbsc%soil":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_dbsc%land_use_mgt":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_dbsc%soil_plant_i":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_dbsc%surf_stor":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_dbsc%snow":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_dbsc%field":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_lumv%usle_p":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    # "hru_lumv%usle_ls":
    #    {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
    #     'egr': True, 'type': 'hru'},
    "hru_lumv%usle_mult":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_lumv%sdr_dep":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_lumv%ldrain":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_lumv%tile_ttime":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_lumv%vfsi":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_lumv%vfsratio":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_lumv%vfscon":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_lumv%vfsch":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_lumv%ngrwat":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_lumv%grwat_i":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_lumv%grwat_n":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_lumv%grwat_spcon":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_lumv%grwat_d":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_lumv%grwat_w":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_lumv%grwat_l":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_lumv%grwat_s":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_lumv%bmp_flag":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_lumv%bmp_sed":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_lumv%bmp_pp":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_lumv%bmp_sp":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_lumv%bmp_pn":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_lumv%bmp_sn":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_lumv%bmp_bac":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_obj_no":
        {'nombre': "object numbers of HRU's", 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_area_ha":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_km":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_surf_stor":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_sno_mm":
        {'nombre': "amount of water in snow on current day", 'unid': 'mm', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_water_fr":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_water_seep":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_water_evap":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    "hru_ich_flood":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'hru'},
    # "hru_cn_luse":
    #    {'nombre': "curve number of HRU based on landuse", 'unid': '', 'ingr': False,
    #     'egr': True, 'type': 'hru'},
    "luse":
        {'nombre': "HRU landuse variable (use this to change all dependent variables of landuse at once)",
         'unid': '', 'ingr': False, 'egr': True, 'type': 'hru'},
    "algae":
        {'nombre': "algal biomass concentration in reach", 'unid': 'mg/L', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "ammonian":
        {'nombre': "ammonia concentration in reach (mg N/L)", 'unid': 'mg/L', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "bankst":
        {'nombre': "bank storage", 'unid': 'm^3', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "li":
        {'nombre': "initial length of main channel", 'unid': 'km', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "orgn":
        {'nombre': "organic nitrogen contribution from channel erosion", 'unid': '', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "orgp":
        {'nombre': "organic phosphorus contribution from channel erosion", 'unid': '', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "si":
        {'nombre': "slope of main channel", 'unid': 'm/m', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "wi":
        {'nombre': "width of main channel at top of bank", 'unid': 'm', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "di":
        {'nombre': "depth of main channel from top of bank to bottom", 'unid': 'm', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "chlora":
        {'nombre': "chlorophyll-a concentration in reach", 'unid': 'mg/L', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "pst_conc":
        {'nombre': "initial pesticide concentration in reach", 'unid': 'mg/m^3', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "dep_chan":
        {'nombre': "average daily water depth in channel", 'unid': 'm', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "disolvp":
        {'nombre': "dissolved P concentration in reach", 'unid': 'mg/L', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "drift":
        {'nombre': "amount of pesticide drifting onto main channel in subbasin", 'unid': 'kg',
         'ingr': False,
         'egr': True, 'type': 'cha'},
    "flwin":
        {'nombre': "flow into reach on previous day", 'unid': 'm^3', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "flwout":
        {'nombre': "flow out of reach on previous day", 'unid': 'm^3', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "nitraten":
        {'nombre': "nitrate concentration in reach (mg N/L)", 'unid': 'mg/L', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "nitriten":
        {'nombre': "nitrite concentration in reach (mg N/L)", 'unid': 'mg/L', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "organicn":
        {'nombre': "organic nitrogen concentration in reach (mg N/L)", 'unid': 'mg/L', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "organicp":
        {'nombre': "organic phosphorus concentration in reach (mg P/L)", 'unid': 'mg/L', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "rch_bactlp":
        {'nombre': "less persistent bacteria stored in reach", 'unid': 'cfu/100ml', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "rch_bactp":
        {'nombre': "persistent bacteria stored in reach", 'unid': 'cfu/100ml', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "rch_cbod":
        {'nombre': "carbonaceous biochemical oxygen demand in reach (mg O2/L)", 'unid': 'mg/L', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "rch_dox":
        {'nombre': "dissolved oxygen concentration in reach (mg O2/L)", 'unid': 'mg/L', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "rchstor":
        {'nombre': "water stored in reach", 'unid': 'm^3', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "sedst":
        {'nombre': "amount of sediment stored in reach", 'unid': 't', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "vel_chan":
        {'nombre': "average flow velocity in channel", 'unid': 'm/s', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "bed_san":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "bed_sil":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "bed_cla":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "bed_gra":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "bnk_san":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "bnk_sil":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "bnk_cla":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "bnk_gra":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "depfp":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "depprfp":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "depsilfp":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "depclafp":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "depch":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "depprch":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "depsanch":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "depsilch":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "depclach":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "depsagch":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "deplagch":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "depgrach":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "sanst":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "silst":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "clast":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "sagst":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "lagst":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "grast":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "wattemp":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "bactp":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "chfloodvol":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'cha'},
    "bactlp":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True, 'type': 'cha'},
}
