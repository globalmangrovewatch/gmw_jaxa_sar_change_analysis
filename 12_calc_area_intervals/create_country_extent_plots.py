import os
import pandas
import numpy
import matplotlib.pyplot as plt

mapped_areas_df = pandas.read_csv("gmw_mjr_v314_national_stats_mapped.csv", index_col="Unnamed: 0")
lower_areas_df = pandas.read_csv("gmw_mjr_v314_national_stats_lower.csv", index_col="Unnamed: 0")
upper_areas_df = pandas.read_csv("gmw_mjr_v314_national_stats_upper.csv", index_col="Unnamed: 0")

years = [1996, 2007, 2008, 2009, 2010, 2015, 2016, 2017, 2018, 2019, 2020]
"""
country_lst = mapped_areas_df["name"].values
rgn_code_lst = mapped_areas_df["region"].values
countries_lut = dict()
regions_lut = dict()
for cntry, rgn in zip(country_lst, rgn_code_lst):
    countries_lut[cntry] = rgn
    regions_lut[rgn] = cntry

for rgn in rgn_code_lst:
    print(f"Process: {rgn}")
    mapped_row = mapped_areas_df[mapped_areas_df['region'] == rgn]
    lower_row = lower_areas_df[lower_areas_df['region'] == rgn]
    upper_row = upper_areas_df[upper_areas_df['region'] == rgn]

    mapped_row = mapped_row.drop(columns=["name", "region"])
    lower_row = lower_row.drop(columns=["name", "region"])
    upper_row = upper_row.drop(columns=["name", "region"])

    mng_map_areas = mapped_row.values[0]
    mng_low_areas = lower_row.values[0]
    mng_upp_areas = upper_row.values[0]

    avg_mng_area = mng_map_areas.mean()
    print(avg_mng_area)
    x_lbl = "Area (Ha)"
    if avg_mng_area > 10000:
        x_lbl = "Area (km2)"
        mng_map_areas = mng_map_areas / 100
        mng_low_areas = mng_low_areas / 100
        mng_upp_areas = mng_upp_areas / 100
        
    max_area = numpy.max(mng_upp_areas) * 1.1

    fig, ax = plt.subplots(1, 1, figsize=(15, 5))
    ax.plot(years, mng_map_areas, color="black")
    ax.fill_between(years, mng_low_areas, mng_upp_areas, color=[0.9, 0.9, 0.9])
    ax.set_title(regions_lut[rgn])
    ax.set_xlabel("Years")
    ax.set_ylabel(x_lbl)
    ax.set_xlim(1995, 2020)
    ax.set_ylim(0, max_area)
    fig.tight_layout()
    out_plt_file = os.path.join("country_extent_plots", f"{rgn}_mng_extent.pdf")
    plt.savefig(out_plt_file)
"""
# Create Global Plot
mapped_areas_tmp_df = mapped_areas_df.drop(columns=["name", "region"])
lower_areas_tmp_df = lower_areas_df.drop(columns=["name", "region"])
upper_areas_tmp_df = upper_areas_df.drop(columns=["name", "region"])

glb_map_extent_df = mapped_areas_tmp_df.loc[:].sum(axis=0)
glb_low_extent_df = lower_areas_tmp_df.loc[:].sum(axis=0)
glb_upp_extent_df = upper_areas_tmp_df.loc[:].sum(axis=0)

mng_map_areas = glb_map_extent_df.values
mng_low_areas = glb_low_extent_df.values
mng_upp_areas = glb_upp_extent_df.values

x_lbl = "Area (km2)"
mng_map_areas = mng_map_areas / 100
mng_low_areas = mng_low_areas / 100
mng_upp_areas = mng_upp_areas / 100

fig, ax = plt.subplots(1, 1, figsize=(15, 5))
ax.plot(years, mng_map_areas, color="black")
ax.fill_between(years, mng_low_areas, mng_upp_areas, color=[0.9, 0.9, 0.9])
ax.set_title("Global")
ax.set_xlabel("Years")
ax.set_ylabel(x_lbl)
ax.set_xlim(1995, 2020)
ax.set_ylim(145000, 155000)
fig.tight_layout()
out_plt_file = "global_mng_extent_zoom_further.pdf"
plt.savefig(out_plt_file)