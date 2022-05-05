import os
import pandas
import matplotlib.pyplot as plt


def create_country_change_plots(mapped_file, lower_file, upper_file, out_dir, plt_base_name, glb_plt_file):
    mapped_areas_df = pandas.read_csv(mapped_file, index_col="Unnamed: 0")
    lower_areas_df = pandas.read_csv(lower_file, index_col="Unnamed: 0")
    upper_areas_df = pandas.read_csv(upper_file, index_col="Unnamed: 0")

    years = [2007, 2008, 2009, 2010, 2015, 2016, 2017, 2018, 2019, 2020]

    country_lst = mapped_areas_df["name"].values
    rgn_code_lst = mapped_areas_df["region"].values
    countries_lut = dict()
    regions_lut = dict()
    for cntry, rgn in zip(country_lst, rgn_code_lst):
        countries_lut[cntry] = rgn
        regions_lut[rgn] = cntry

    cols = mapped_areas_df.columns
    cols_gain_area = list()
    cols_loss_area = list()
    for col in cols:
        if ("area" in col) and ("gain" in col):
            cols_gain_area.append(col)
        elif ("area" in col) and ("loss" in col):
            cols_loss_area.append(col)
    print(cols_gain_area)
    print(cols_loss_area)

    mapped_areas_loss_df = mapped_areas_df.drop(columns=cols_gain_area)
    mapped_areas_gain_df = mapped_areas_df.drop(columns=cols_loss_area)

    lower_areas_loss_df = lower_areas_df.drop(columns=cols_gain_area)
    lower_areas_gain_df = lower_areas_df.drop(columns=cols_loss_area)

    upper_areas_loss_df = upper_areas_df.drop(columns=cols_gain_area)
    upper_areas_gain_df = upper_areas_df.drop(columns=cols_loss_area)

    drop_cols = ["name", "region", "index"]

    for rgn in rgn_code_lst:
        print(f"Process: {rgn}")

        # Loss
        mapped_loss_row = mapped_areas_loss_df[mapped_areas_loss_df['region'] == rgn]
        lower_loss_row = lower_areas_loss_df[lower_areas_loss_df['region'] == rgn]
        upper_loss_row = upper_areas_loss_df[upper_areas_loss_df['region'] == rgn]
        # Gain
        mapped_gain_row = mapped_areas_gain_df[mapped_areas_gain_df['region'] == rgn]
        lower_gain_row = lower_areas_gain_df[lower_areas_gain_df['region'] == rgn]
        upper_gain_row = upper_areas_gain_df[upper_areas_gain_df['region'] == rgn]

        # Loss
        mapped_loss_row = mapped_loss_row.drop(columns=drop_cols)
        lower_loss_row = lower_loss_row.drop(columns=drop_cols)
        upper_loss_row = upper_loss_row.drop(columns=drop_cols)
        # Gain
        mapped_gain_row = mapped_gain_row.drop(columns=drop_cols)
        lower_gain_row = lower_gain_row.drop(columns=drop_cols)
        upper_gain_row = upper_gain_row.drop(columns=drop_cols)

        # Loss
        mng_loss_map_areas = mapped_loss_row.values[0]
        mng_loss_low_areas = lower_loss_row.values[0]
        mng_loss_upp_areas = upper_loss_row.values[0]
        # Gain
        mng_gain_map_areas = mapped_gain_row.values[0]
        mng_gain_low_areas = lower_gain_row.values[0]
        mng_gain_upp_areas = upper_gain_row.values[0]

        min_loss_area = mng_loss_low_areas.min()
        min_gain_area = mng_gain_low_areas.min()
        min_area = min_loss_area
        if min_gain_area < min_loss_area:
            min_area = min_gain_area

        max_loss_area = mng_loss_upp_areas.max()
        max_gain_area = mng_gain_upp_areas.max()
        max_area = max_loss_area
        if max_gain_area > max_loss_area:
            max_area = max_gain_area

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))

        ax1.plot(years, mng_loss_map_areas, color="black")
        ax1.fill_between(years, mng_loss_low_areas, mng_loss_upp_areas, color=[0.9, 0.9, 0.9])
        ax1.set_title("{} Loss".format(regions_lut[rgn]))
        ax1.set_xlabel("Years")
        ax1.set_ylabel("Area (Ha)")
        ax1.set_xlim(2005, 2020)
        ax1.set_ylim(min_area, max_area)

        ax2.plot(years, mng_gain_map_areas, color="black")
        ax2.fill_between(years, mng_gain_low_areas, mng_gain_upp_areas, color=[0.9, 0.9, 0.9])
        ax2.set_title("{} Gain".format(regions_lut[rgn]))
        ax2.set_xlabel("Years")
        ax2.set_ylabel("Area (Ha)")
        ax2.set_xlim(2005, 2020)
        ax2.set_ylim(min_area, max_area)

        fig.tight_layout()

        out_plt_file = os.path.join(out_dir, f"{rgn}_mng_changes_{plt_base_name}_extent.pdf")
        plt.savefig(out_plt_file)

    mapped_areas_loss_tmp_df = mapped_areas_loss_df.drop(columns=drop_cols)
    mapped_areas_gain_tmp_df = mapped_areas_gain_df.drop(columns=drop_cols)

    lower_areas_loss_tmp_df = lower_areas_loss_df.drop(columns=drop_cols)
    lower_areas_gain_tmp_df = lower_areas_gain_df.drop(columns=drop_cols)

    upper_areas_loss_tmp_df = upper_areas_loss_df.drop(columns=drop_cols)
    upper_areas_gain_tmp_df = upper_areas_gain_df.drop(columns=drop_cols)

    glb_map_loss_df = mapped_areas_loss_tmp_df.loc[:].sum(axis=0)
    glb_map_gain_df = mapped_areas_gain_tmp_df.loc[:].sum(axis=0)

    glb_low_loss_df = lower_areas_loss_tmp_df.loc[:].sum(axis=0)
    glb_low_gain_df = lower_areas_gain_tmp_df.loc[:].sum(axis=0)

    glb_upp_loss_df = upper_areas_loss_tmp_df.loc[:].sum(axis=0)
    glb_upp_gain_df = upper_areas_gain_tmp_df.loc[:].sum(axis=0)

    # Loss
    mng_loss_map_areas = glb_map_loss_df.values
    mng_loss_low_areas = glb_low_loss_df.values
    mng_loss_upp_areas = glb_upp_loss_df.values
    # Gain
    mng_gain_map_areas = glb_map_gain_df.values
    mng_gain_low_areas = glb_low_gain_df.values
    mng_gain_upp_areas = glb_upp_gain_df.values

    min_loss_area = mng_loss_low_areas.min()
    min_gain_area = mng_gain_low_areas.min()
    min_area = min_loss_area
    if min_gain_area < min_loss_area:
        min_area = min_gain_area

    max_loss_area = mng_loss_upp_areas.max()
    max_gain_area = mng_gain_upp_areas.max()
    max_area = max_loss_area
    if max_gain_area > max_loss_area:
        max_area = max_gain_area

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))

    ax1.plot(years, mng_loss_map_areas, color="black")
    ax1.fill_between(years, mng_loss_low_areas, mng_loss_upp_areas, color=[0.9, 0.9,
                                                                           0.9])
    ax1.set_title("Global Loss")
    ax1.set_xlabel("Years")
    ax1.set_ylabel("Area (Ha)")
    ax1.set_xlim(2005, 2020)
    ax1.set_ylim(min_area, max_area)

    ax2.plot(years, mng_gain_map_areas, color="black")
    ax2.fill_between(years, mng_gain_low_areas, mng_gain_upp_areas, color=[0.9, 0.9,
                                                                           0.9])
    ax2.set_title("Global Gain")
    ax2.set_xlabel("Years")
    ax2.set_ylabel("Area (Ha)")
    ax2.set_xlim(2005, 2020)
    ax2.set_ylim(min_area, max_area)

    fig.tight_layout()

    plt.savefig(glb_plt_file)


create_country_change_plots("gmw_v314_chng_f1996_national_stats_mapped.csv", "gmw_v314_chng_f1996_national_stats_lower.csv", "gmw_v314_chng_f1996_national_stats_upper.csv", "country_change_plots_base1996", "b1996", "global_mng_chng_b1996.pdf")
create_country_change_plots("gmw_v314_annual_chngs_national_stats_mapped.csv", "gmw_v314_annual_chngs_national_stats_lower.csv", "gmw_v314_annual_chngs_national_stats_upper.csv", "country_change_plots_obs2obs", "obs2obs", "global_mng_chng_obs2obs.pdf")
