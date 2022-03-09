import os

def create_data_arch(site_lst, pts_dir, img_dirs, out_arch_file, tmp_dir):
    print("Hello World")
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)

    for site in site_lst:
        print(site)

rl_sites = []
ar_sites = []
lh_sites = []
nt_sites = []

pts_dir = "acc_ref_pts_set_2"
ls_imgs_dir = "/Users/pete/Dropbox/University/Research/Analysis/GlobalMangroveWatch/gmw_v3_acc/landsat_band_sub"


create_data_arch(rl_sites, pts_dir, ls_imgs_dir, "richard_gmw_chng_sites_acc.tar.gz", "./tmp")
create_data_arch(rl_sites, pts_dir, ar_sites, "ake_gmw_chng_sites_acc.tar.gz", "./tmp")
create_data_arch(rl_sites, pts_dir, lh_sites, "lammert_gmw_chng_sites_acc.tar.gz", "./tmp")
create_data_arch(rl_sites, pts_dir, nt_sites, "nathan_gmw_chng_sites_acc.tar.gz", "./tmp")

