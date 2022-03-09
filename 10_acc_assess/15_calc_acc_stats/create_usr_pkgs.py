import os
import rsgislib.tools.filetools

def create_data_arch(site_lst, pts_dir, img_dirs, out_arch_file, tmp_dir):
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)

    for site in site_lst:
        print(site)
        site_pts_file = rsgislib.tools.filetools.find_file(pts_dir, f"gmw_chng_site_{site}_*.geojson")
        print(site_pts_file)


rl_sites = [3, 6,  29, 30, 31, 35]
ar_sites = [1, 2,  11, 13, 20, 25, 28, 32, 33, 36, 38]
lh_sites = [4, 7,  8,  9,  15, 18, 19, 21, 22, 26, 27]
nt_sites = [5, 10, 12, 14, 16, 17, 23, 24, 34, 37]

pts_dir = "acc_ref_pts_set_2"
ls_imgs_dir = "/Users/pete/Dropbox/University/Research/Analysis/GlobalMangroveWatch/gmw_v3_acc/landsat_band_sub"


create_data_arch(rl_sites, pts_dir, ls_imgs_dir, "richard_gmw_chng_sites_acc.tar.gz", "./tmp")
#create_data_arch(rl_sites, pts_dir, ar_sites, "ake_gmw_chng_sites_acc.tar.gz", "./tmp")
#create_data_arch(rl_sites, pts_dir, lh_sites, "lammert_gmw_chng_sites_acc.tar.gz", "./tmp")
#create_data_arch(rl_sites, pts_dir, nt_sites, "nathan_gmw_chng_sites_acc.tar.gz", "./tmp")

