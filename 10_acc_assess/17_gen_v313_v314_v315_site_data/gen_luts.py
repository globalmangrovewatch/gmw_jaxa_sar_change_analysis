import os
import glob

import rsgislib.imageutils.imagelut

years = ["1996", "2007", "2008", "2009", "2010", "2015", "2016", "2017", "2018", "2019", "2020"]
versions = ["313", "314", "315"]

base_path = "/bigdata/globalmangrovewatch/gmw_v{}_extent"
scns_rel_path = "KEA/gmw_v3_fnl_mjr_{}_v{}"
for version in versions:
    print(f"v{version}")
    ver_base_path = base_path.format(version)
    lut_vec_file = os.path.join(ver_base_path, "gmw_scns_lut_v{}.gpkg".format(version))
    if os.path.exists(lut_vec_file):
        os.remove(lut_vec_file)
    for year in years:
        print(f"\t{year}")
        srch_path = os.path.join(ver_base_path, scns_rel_path.format(year, version), "*.kea")
        input_imgs = glob.glob(srch_path)
        lut_vec_lyr = "{}_mng_v{}".format(year, version)
        rsgislib.imageutils.imagelut.create_img_extent_lut(input_imgs, lut_vec_file, lut_vec_lyr, out_format="GPKG", ignore_none_imgs=False, out_proj_wgs84=False, overwrite_lut_file=False)

