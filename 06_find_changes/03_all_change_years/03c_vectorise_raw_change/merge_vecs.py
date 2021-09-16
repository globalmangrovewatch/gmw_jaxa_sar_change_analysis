import glob
import os
import rsgislib.vectorutils

all_years = ['1996', '2007', '2008', '2009', '2010', '2015', '2016', '2017', '2018', '2019', '2020']
years_l1 = ['1996', '2007', '2008', '2009', '2015', '2016', '2017', '2018', '2019', '2020']
for l1_year in years_l1:
    out_file = "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from{0}/gmw_raw_chngs_feats_304_{0}base_vecs.gpkg".format(l1_year)
    base_dir = '/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from{}'.format(l1_year)
    chng_years = all_years.copy()
    chng_years.remove(l1_year)
    first = True
    for chg_year in chng_years:
        if first:
            input_vecs = glob.glob(os.path.join(base_dir, 'gmw_{0}_{1}_chngs_vecs/*{1}_mng_chng_base{0}.kea'.format(l1_year, chg_year)))
            rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "{}_mng_{}_nmng".format(l1_year, chg_year), False)

            input_vecs = glob.glob(os.path.join(base_dir, 'gmw_{0}_{1}_chngs_vecs/*{1}_not_mng_chng_base{0}.kea'.format(l1_year, chg_year)))
            rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "{}_nmng_{}_mng".format(l1_year, chg_year), True)
            first = True
        else:
            input_vecs = glob.glob(os.path.join(base_dir, 'gmw_{0}_{1}_chngs_vecs/*{1}_mng_chng_base{0}.kea'.format(l1_year, chg_year)))
            rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "{}_mng_{}_nmng".format(l1_year, chg_year), True)

            input_vecs = glob.glob(os.path.join(base_dir, 'gmw_{0}_{1}_chngs_vecs/*{1}_not_mng_chng_base{0}.kea'.format(l1_year, chg_year)))
            rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "{}_nmng_{}_mng".format(l1_year, chg_year), True)




