import pandas

def calc_upper_lower_chng_intervals(chng_file, out_map_file, out_low_file, out_up_file):
    chngs_stats_df = pandas.read_feather(chng_file)
    cols = chngs_stats_df.columns
    cols_rm = list()
    cols_gain_area = list()
    cols_loss_area = list()
    for col in cols:
        if "count" in col:
            cols_rm.append(col)
        elif ("area" in col) and ("gain" in col):
            cols_gain_area.append(col)
        elif ("area" in col) and ("loss" in col):
            cols_loss_area.append(col)
    print(cols_rm)
    print(cols_gain_area)
    print(cols_loss_area)

    chngs_stats_df = chngs_stats_df.drop(columns=cols_rm)

    # Update the Users and Producers Accuracies is Accuracy Assessment Changes!
    mng_to_nmng_com = (100 - 46.24930555555556) / 100
    mng_to_nmng_om = (100 - 68.56030058651027) / 100
    nmng_to_mng_com = (100 - 43.66152423012652) / 100
    nmng_to_mng_om = (100 - 63.21779214559387) / 100

    print("mng_to_nmng_om = {}".format(mng_to_nmng_om))
    print("mng_to_nmng_com = {}".format(mng_to_nmng_com))
    print("nmng_to_mng_om = {}".format(nmng_to_mng_om))
    print("nmng_to_mng_com = {}".format(nmng_to_mng_com))

    low_chngs_stats_df = chngs_stats_df.copy(deep=True)
    up_chngs_stats_df = chngs_stats_df.copy(deep=True)

    for col in cols_gain_area:
        low_chngs_stats_df[col] = low_chngs_stats_df[col] - (low_chngs_stats_df[col] * nmng_to_mng_com)
        up_chngs_stats_df[col] = up_chngs_stats_df[col] + (up_chngs_stats_df[col] * nmng_to_mng_om)

    for col in cols_loss_area:
        low_chngs_stats_df[col] = low_chngs_stats_df[col] - (low_chngs_stats_df[col] * mng_to_nmng_com)
        up_chngs_stats_df[col] = up_chngs_stats_df[col] + (up_chngs_stats_df[col] * mng_to_nmng_om)

    low_chngs_stats_df.to_csv(out_low_file)
    up_chngs_stats_df.to_csv(out_up_file)
    chngs_stats_df.to_csv(out_map_file)

def calc_upper_lower_extent_intervals(extent_file, out_map_file, out_low_file, out_up_file):
    extent_stats_df = pandas.read_feather(extent_file)
    cols = extent_stats_df.columns
    cols_rm = list()
    cols_area = list()
    for col in cols:
        if "count" in col:
            cols_rm.append(col)
        elif ("area" in col):
            cols_area.append(col)
    print(cols_rm)
    print(cols_area)

    extent_stats_df = extent_stats_df.drop(columns=cols_rm)

    # Update the Users and Producers Accuracies is Accuracy Assessment Changes!
    mng_com = (100 - 87.80591096578111) / 100
    mng_om = (100 - 84.07280953261808) / 100

    print("mng_com = {}".format(mng_com))
    print("mng_om = {}".format(mng_om))

    low_extent_stats_df = extent_stats_df.copy(deep=True)
    up_extent_stats_df = extent_stats_df.copy(deep=True)

    for col in cols_area:
        low_extent_stats_df[col] = low_extent_stats_df[col] - (low_extent_stats_df[col] * mng_com)
        up_extent_stats_df[col] = up_extent_stats_df[col] + (up_extent_stats_df[col] * mng_om)

    low_extent_stats_df.to_csv(out_low_file)
    up_extent_stats_df.to_csv(out_up_file)
    extent_stats_df.to_csv(out_map_file)



chngs_annual_file = "base_area_stats/gmw_v314_annual_chngs_national_stats.feather"
chngs_annual_low_file = "gmw_v314_annual_chngs_national_stats_lower.csv"
chngs_annual_map_file = "gmw_v314_annual_chngs_national_stats_mapped.csv"
chngs_annual_up_file = "gmw_v314_annual_chngs_national_stats_upper.csv"
calc_upper_lower_chng_intervals(chngs_annual_file, chngs_annual_map_file, chngs_annual_low_file, chngs_annual_up_file)

chngs_base96_file = "base_area_stats/gmw_v314_chng_f1996_national_stats.feather"
chngs_base96_low_file = "gmw_v314_chng_f1996_national_stats_lower.csv"
chngs_base96_map_file = "gmw_v314_chng_f1996_national_stats_mapped.csv"
chngs_base96_up_file = "gmw_v314_chng_f1996_national_stats_upper.csv"
calc_upper_lower_chng_intervals(chngs_base96_file, chngs_base96_map_file, chngs_base96_low_file, chngs_base96_up_file)

gmw_area_extents_file = "base_area_stats/gmw_mjr_v314_national_stats.feather"
gmw_area_extents_low_file = "gmw_mjr_v314_national_stats_lower.csv"
gmw_area_extents_map_file = "gmw_mjr_v314_national_stats_mapped.csv"
gmw_area_extents_up_file = "gmw_mjr_v314_national_stats_upper.csv"
calc_upper_lower_extent_intervals(gmw_area_extents_file, gmw_area_extents_map_file, gmw_area_extents_low_file, gmw_area_extents_up_file)
