import glob
import os
import rsgislib.vectorutils

all_years = ['1996', '2007', '2008', '2009', '2010', '2015', '2016', '2017', '2018', '2019', '2020']
years_l1 = ['1996', '2007', '2008', '2009', '2015', '2016', '2017', '2018', '2019', '2020']
for l1_year in years_l1:
    out_file = "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from{0}/gmw_mng_ext_304_{0}base_vecs.gpkg".format(l1_year)
    base_dir = '/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from{}'.format(l1_year)
    chng_years = all_years.copy()
    chng_years.remove(l1_year)
    first = True
    for chg_year in chng_years:
        if first:
            input_vecs = glob.glob(os.path.join(base_dir,'gmw_base{}_{}_mng_ext_vecs/*.gpkg'.format(l1_year, chg_year)))
            rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "mng_{}_base{}".format(chg_year, l1_year), False)
            first = True
        else:
            input_vecs = glob.glob(os.path.join(base_dir, 'gmw_base{}_{}_mng_ext_vecs/*.gpkg'.format(l1_year, chg_year)))
            rsgislib.vectorutils.mergeVectors2GPKG(input_vecs, out_file, "mng_{}_base{}".format(chg_year, l1_year), True)






