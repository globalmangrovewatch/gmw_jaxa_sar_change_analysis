import os
import shutil
import rsgislib.tools.filetools

def create_data_arch(site_lst, pts_dir, img_dirs, out_arch_file, tmp_dir):
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)

    file_list = list()

    for site in site_lst:
        print(site)
        site_out_dir = os.path.join(tmp_dir, f"site_{site}")
        if not os.path.exists(site_out_dir):
            os.mkdir(site_out_dir)
        site_pts_file = rsgislib.tools.filetools.find_file(pts_dir, f"gmw_chng_site_{site}_*.geojson")
        site_pts_file_name = os.path.basename(site_pts_file)
        print(site_pts_file)
        out_pts_file = os.path.join(site_out_dir, site_pts_file_name)
        shutil.copy(site_pts_file, out_pts_file)
        file_list.append(out_pts_file)

        acc_pts_file_basename = rsgislib.tools.filetools.get_file_basename(site_pts_file)
        acc_pts_file_comps = acc_pts_file_basename.split("_")
        base_year = acc_pts_file_comps[4]
        end_year = acc_pts_file_comps[5]
        print(f"{base_year} -- {end_year}")
        ls_imgs_site_dir = os.path.join(img_dirs, f"gmw_ref_ls_comp_imgs_site_{site}")
        print(ls_imgs_site_dir)

        base_ls_img = rsgislib.tools.filetools.find_file(ls_imgs_site_dir, f"site_{site}_ls_*_{base_year}_img.tif")
        print(base_ls_img)
        ls_base_img_name = os.path.basename(base_ls_img)
        out_base_img = os.path.join(site_out_dir, ls_base_img_name)
        print(out_base_img)
        shutil.copy(base_ls_img, out_base_img)
        file_list.append(out_base_img)

        end_ls_img = rsgislib.tools.filetools.find_file(ls_imgs_site_dir, f"site_{site}_ls_*_{end_year}_img.tif")
        print(end_ls_img)
        ls_end_img_name = os.path.basename(end_ls_img)
        out_end_img = os.path.join(site_out_dir, ls_end_img_name)
        print(out_end_img)
        shutil.copy(end_ls_img, out_end_img)
        file_list.append(out_end_img)

    rsgislib.tools.filetools.create_targz_arch(out_arch_file, file_list, base_path=tmp_dir)

    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)


rl_sites = [3, 6,  29, 30, 31, 35]
ar_sites = [1, 2,  11, 13, 20, 25, 28, 32, 33, 36, 38]
lh_sites = [4, 7,  8,  9,  15, 18, 19, 21, 22, 26, 27]
nt_sites = [5, 10, 12, 14, 16, 17, 23, 24, 34, 37]

pts_dir = "acc_ref_pts_set_2"
ls_imgs_dir = "/Users/pete/Dropbox/University/Research/Analysis/GlobalMangroveWatch/gmw_v3_acc/landsat_band_sub"


create_data_arch(rl_sites, pts_dir, ls_imgs_dir, "richard_gmw_chng_sites_acc.tar.gz", "./tmp")
create_data_arch(ar_sites, pts_dir, ls_imgs_dir, "ake_gmw_chng_sites_acc.tar.gz", "./tmp")
create_data_arch(lh_sites, pts_dir, ls_imgs_dir, "lammert_gmw_chng_sites_acc.tar.gz", "./tmp")
create_data_arch(nt_sites, pts_dir, ls_imgs_dir, "nathan_gmw_chng_sites_acc.tar.gz", "./tmp")

