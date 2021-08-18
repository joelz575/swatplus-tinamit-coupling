from typing import Dict

from tinamit.mod import Variable


def gen_variables_swatp() -> [Variable]:
    variables = []
    for vr, info in _info_vars.items():
        variables.append(Variable(
            nombre=vr, unid=info['unid'], ingr=info['ingr'], egr=info['egr']
        ))
    return variables


# Un diccionario de variables SWAT+. Ver la documentación SWAT+ para más detalles.
_info_vars = {
    'agrl_km2':
        {'nombre': 'Area of Agricultural Land', 'unid': 'km^2', 'ingr': True,
         'egr': False},
    'nagrl_km2':
        {'nombre': 'Area of Non-Agricultural Land', 'unid': 'km^2', 'ingr': True,
         'egr': False},
    'sd_props':
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    'sd_obj_no':
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    'sd_aqu_link':
        {'nombre': "aquifer the channel is linked to", 'unid': '', 'ingr': True,
         'egr': True},
    'sd_aqu_link_ch':
        {'nombre': 'sequential channel number in the aquifer', 'unid': '', 'ingr': True,
         'egr': True},
    'sd_chw':
        {'nombre': "channel width", 'unid': 'm', 'ingr': True,
         'egr': True},
    'sd_chd':
        {'nombre': "channel depth", 'unid': 'm', 'ingr': True,
         'egr': True},
    'sd_chs':
        {'nombre': "channel slope", 'unid': 'm/m', 'ingr': True,
         'egr': True},
    'sd_chl':
        {'nombre': "channel length", 'unid': 'km', 'ingr': True,
         'egr': True},
    'sd_chn':
        {'nombre': "channel Manning's n", 'unid': '', 'ingr': True,
         'egr': True},
    'sd_cov':
        {'nombre': "channel cover factor", 'unid': '', 'ingr': True,
         'egr': True},
    'sd_cherod':
        {'nombre': "channel erodibility", 'unid': '', 'ingr': True,
         'egr': True},
    'sd_shear_bnk':
        {'nombre': "bank shear coefficient - fraction of bottom shear", 'unid': '', 'ingr': True,
         'egr': True},
    'sd_hc_erod':
        {'nombre': "headcut erodibility", 'unid': '', 'ingr': True,
         'egr': True},
    'sd_hc_co':
        {'nombre': "proportionality coefficient for head cut", 'unid': 'm/m', 'ingr': True,
         'egr': True},
    'sd_hc_len':
        {'nombre': "length of head cut", 'unid': 'm', 'ingr': True,
         'egr': True},
    'sd_hc_hgt':
        {'nombre': "headcut height", 'unid': 'm', 'ingr': True,
         'egr': True},
    'sd_stor':
        {'nombre': "water stored in reach at end of the day", 'unid': 'm3', 'ingr': True,
         'egr': True},
    'lte_props':
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    'lte_obj_no':
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    'lte_iplant':
        {'nombre': "plant number xwalked from hlt_db()%plant and plants.plt", 'unid': '',
         'ingr': True,
         'egr': True},
    'lte_km2':
        {'nombre': "drainage area", 'unid': 'km^2', 'ingr': True,
         'egr': True},
    'lte_cn2':
        {'nombre': "condition II curve number (used in calibration)", 'unid': '', 'ingr': True,
         'egr': True},
    'lte_cn3_swf':
        {'nombre': "soil water factor for cn3 (used in calibration)", 'unid': '', 'ingr': True,
         'egr': True},
    'lte_soildep':
        {'nombre': "soil profile depth", 'unid': 'mm', 'ingr': True,
         'egr': True},
    'lte_etco':
        {'nombre': "et coefficient - use with pet and aet (used in calibration)", 'unid': '',
         'ingr': True,
         'egr': True},
    'lte_revapc':
        {'nombre': "revap from aquifer (used in calibration)", 'unid': 'm/m', 'ingr': True,
         'egr': True},
    'lte_perco':
        {'nombre': "soil percolation coefficient (used in calibration)", 'unid': '',
         'ingr': True,
         'egr': True},
    'lte_tdrain':
        {'nombre': "design subsurface tile drain time (used in calibration)", 'unid': 'hr',
         'ingr': True,
         'egr': True},
    'lte_stress':
        {'nombre': "plant stress - pest, root restriction, soil quality, nutri", 'unid': 'frac',
         'ingr': True,
         'egr': True},
    'lte_uslefac':
        {'nombre': "USLE slope length factor", 'unid': '', 'ingr': True,
         'egr': True},
    'lte_wrt1':
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    'lte_wrt2':
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    'lte_smx':
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    'lte_hk':
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    'lte_yls':
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    'lte_ylc':
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    'lte_awc':
        {'nombre': "available water capacity of soil", 'unid': 'mm/mm', 'ingr': True,
         'egr': True},
    'lte_g':
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    'lte_hufh':
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    'lte_phu':
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    'lte_por':
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    'lte_sc':
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    'lte_sw':
        {'nombre': "initial soil water storage", 'unid': 'mm/mm', 'ingr': True,
         'egr': True},
    'lte_gw':
        {'nombre': "initial shallow aquifer storage", 'unid': 'mm', 'ingr': True,
         'egr': True},
    'lte_snow':
        {'nombre': "initial water content of snow", 'unid': 'mm', 'ingr': True,
         'egr': True},
    'lte_gwflow':
        {'nombre': "initial groundwater flow", 'unid': 'mm', 'ingr': True,
         'egr': True},
    'lte_dm':
        {'nombre': "plant biomass", 'unid': 't/ha', 'ingr': True,
         'egr': True},
    'lte_alai':
        {'nombre': "leaf area index", 'unid': '', 'ingr': True,
         'egr': True},
    'lte_yield':
        {'nombre': "plant yield", 'unid': 't/ha', 'ingr': True,
         'egr': True},
    'lte_npp':
        {'nombre': "net primary productivity", 'unid': 't/ha', 'ingr': True,
         'egr': True},
    'lte_lai_mx':
        {'nombre': "maximum leaf area index", 'unid': '', 'ingr': True,
         'egr': True},
    'lte_gwdeep':
        {'nombre': "deep aquifer storage", 'unid': 'mm', 'ingr': True,
         'egr': True},
    'lte_aet':
        {'nombre': "sum of actual et during growing season (for hi water stress)", 'unid': 'mm',
         'ingr': True,
         'egr': True},
    'lte_pet':
        {'nombre': "sum of potential et during growing season (for hi water stress)", 'unid': 'mm',
         'ingr': True,
         'egr': True},
    'lte_start':
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    'lte_end':
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_land_use_mgt":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_land_use_mgt_c":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_lum_group":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_lum_group_c":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_region":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_plant_cov":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_mgt_ops":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_tiledrain":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_septic":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_fstrip":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_grassww":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_bmpuser":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_crop_reg":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_cur_op":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_strsa":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_luse%name":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_luse%cn_lu":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_luse%cons_prac":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_luse%usle_p":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_luse%urb_ro":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_luse%urb_lu":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_luse%ovn":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_dbs%name":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_dbs%topo":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_dbs%hyd":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_dbs%soil":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_dbs%land_use_mgt":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_dbs%soil_plant_in":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_dbs%surf_stor":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_dbs%snow":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_dbs%field":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_dbsc%name":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_dbsc%topo":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_dbsc%hyd":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_dbsc%soil":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_dbsc%land_use_mgt":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_dbsc%soil_plant_i":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_dbsc%surf_stor":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_dbsc%snow":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_dbsc%field":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_lumv%usle_p":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_lumv%usle_ls":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_lumv%usle_mult":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_lumv%sdr_dep":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_lumv%ldrain":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_lumv%tile_ttime":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_lumv%vfsi":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_lumv%vfsratio":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_lumv%vfscon":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_lumv%vfsch":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_lumv%ngrwat":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_lumv%grwat_i":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_lumv%grwat_n":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_lumv%grwat_spcon":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_lumv%grwat_d":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_lumv%grwat_w":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_lumv%grwat_l":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_lumv%grwat_s":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_lumv%bmp_flag":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_lumv%bmp_sed":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_lumv%bmp_pp":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_lumv%bmp_sp":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_lumv%bmp_pn":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_lumv%bmp_sn":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_lumv%bmp_bac":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_obj_no":
        {'nombre': "object numbers of HRU's", 'unid': '', 'ingr': False,
         'egr': True},
    "hru_area_ha":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': False,
         'egr': True},
    "hru_km":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_surf_stor":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_sno_mm":
        {'nombre': "amount of water in snow on current day", 'unid': 'mm', 'ingr': True,
         'egr': True},
    "hru_water_fr":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_water_seep":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_water_evap":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "hru_ich_flood":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "cn_luse":
        {'nombre': "curve number of HRU based on landuse", 'unid': '', 'ingr': True,
         'egr': True},
    "luse":
        {'nombre': "HRU landuse variable (use this to change all dependent variables of landuse at once)",
         'unid': '', 'ingr': True, 'egr': True},
    "algae":
        {'nombre': "algal biomass concentration in reach", 'unid': 'mg/L', 'ingr': True,
         'egr': True},
    "ammonian":
        {'nombre': "ammonia concentration in reach (mg N/L)", 'unid': 'mg/L', 'ingr': True,
         'egr': True},
    "bankst":
        {'nombre': "bank storage", 'unid': 'm^3', 'ingr': True,
         'egr': True},
    "li":
        {'nombre': "initial length of main channel", 'unid': 'km', 'ingr': True,
         'egr': True},
    "orgn":
        {'nombre': "organic nitrogen contribution from channel erosion", 'unid': '', 'ingr': True,
         'egr': True},
    "orgp":
        {'nombre': "organic phosphorus contribution from channel erosion", 'unid': '', 'ingr': True,
         'egr': True},
    "si":
        {'nombre': "slope of main channel", 'unid': 'm/m', 'ingr': True,
         'egr': True},
    "wi":
        {'nombre': "width of main channel at top of bank", 'unid': 'm', 'ingr': True,
         'egr': True},
    "di":
        {'nombre': "depth of main channel from top of bank to bottom", 'unid': 'm', 'ingr': True,
         'egr': True},
    "chlora":
        {'nombre': "chlorophyll-a concentration in reach", 'unid': 'mg/L', 'ingr': True,
         'egr': True},
    "pst_conc":
        {'nombre': "initial pesticide concentration in reach", 'unid': 'mg/m^3', 'ingr': True,
         'egr': True},
    "dep_chan":
        {'nombre': "average daily water depth in channel", 'unid': 'm', 'ingr': True,
         'egr': True},
    "disolvp":
        {'nombre': "dissolved P concentration in reach", 'unid': 'mg/L', 'ingr': True,
         'egr': True},
    "drift":
        {'nombre': "amount of pesticide drifting onto main channel in subbasin", 'unid': 'kg',
         'ingr': True,
         'egr': True},
    "flwin":
        {'nombre': "flow into reach on previous day", 'unid': 'm^3', 'ingr': True,
         'egr': True},
    "flwout":
        {'nombre': "flow out of reach on previous day", 'unid': 'm^3', 'ingr': True,
         'egr': True},
    "nitraten":
        {'nombre': "nitrate concentration in reach (mg N/L)", 'unid': 'mg/L', 'ingr': True,
         'egr': True},
    "nitriten":
        {'nombre': "nitrite concentration in reach (mg N/L)", 'unid': 'mg/L', 'ingr': True,
         'egr': True},
    "organicn":
        {'nombre': "organic nitrogen concentration in reach (mg N/L)", 'unid': 'mg/L', 'ingr': True,
         'egr': True},
    "organicp":
        {'nombre': "organic phosphorus concentration in reach (mg P/L)", 'unid': 'mg/L', 'ingr': True,
         'egr': True},
    "rch_bactlp":
        {'nombre': "less persistent bacteria stored in reach", 'unid': 'cfu/100ml', 'ingr': True,
         'egr': True},
    "rch_bactp":
        {'nombre': "persistent bacteria stored in reach", 'unid': 'cfu/100ml', 'ingr': True,
         'egr': True},
    "rch_cbod":
        {'nombre': "carbonaceous biochemical oxygen demand in reach (mg O2/L)", 'unid': 'mg/L', 'ingr': True,
         'egr': True},
    "rch_dox":
        {'nombre': "dissolved oxygen concentration in reach (mg O2/L)", 'unid': 'mg/L', 'ingr': True,
         'egr': True},
    "rchstor":
        {'nombre': "water stored in reach", 'unid': 'm^3', 'ingr': True,
         'egr': True},
    "sedst":
        {'nombre': "amount of sediment stored in reach", 'unid': 't', 'ingr': True,
         'egr': True},
    "vel_chan":
        {'nombre': "average flow velocity in channel", 'unid': 'm/s', 'ingr': True,
         'egr': True},
    "bed_san":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "bed_sil":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "bed_cla":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "bed_gra":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "bnk_san":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "bnk_sil":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "bnk_cla":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "bnk_gra":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "depfp":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "depprfp":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "depsilfp":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "depclafp":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "depch":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "depprch":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "depsanch":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "depsilch":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "depclach":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "depsagch":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "deplagch":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "depgrach":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "sanst":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "silst":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "clast":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "sagst":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "lagst":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "grast":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "wattemp":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "bactp":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "chfloodvol":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
    "bactlp":
        {'nombre': 'Name Not Available', 'unid': '', 'ingr': True,
         'egr': True},
}
