from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import logging
import os
import glob
import pathlib
import rsgislib.imageutils.imagelut

logger = logging.getLogger(__name__)

class GenCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        img_tiles = glob.glob(kwargs['gmw_tiles'])

        for tile_name in ["N19E070", "N19E073", "N18E073", "N17E073", "N16E073",
                          "N16E074", "N15E074", "N14E074", "N13E074", "N13E075",
                          "N12E075", "N11E075", "N11E076", "N10E076", "N10E078",
                          "N10E079", "N10E080", "N09E076", "N09E077", "N09E078",
                          "N09E079", "N09E080"]:

        #for gmw_tile in img_tiles:
        #    basename = self.get_file_basename(gmw_tile)
        #    tile_basename = self.get_file_basename(gmw_tile, n_comps=2)
        #    tile_name = tile_basename.split('_')[1]

            sar_base_scn_dir = os.path.join(kwargs['sar_base_tiles_dir'], tile_name)
            sar_flt_scn_dir = os.path.join(kwargs['sar_tiles_dir'], tile_name)

            sar_base_img = os.path.join(sar_base_scn_dir, '{}_2010_db_mskd.kea'.format(tile_name))
            sar_flt_img = os.path.join(sar_flt_scn_dir, '{}_{}_db_mskd_bufd.kea'.format(tile_name, kwargs['sar_year']))
            if os.path.exists(sar_base_img) and os.path.exists(sar_flt_img):
                out_off_img = os.path.join(sar_flt_scn_dir, '{}_{}_db_mskd_bufd_offset.kea'.format(tile_name, kwargs['sar_year']))
                out_rsmp_img = os.path.join(sar_flt_scn_dir, '{}_{}_db_mskd_reg.kea'.format(tile_name, kwargs['sar_year']))
                out_off_json = os.path.join(sar_flt_scn_dir, '{}_{}_2010_offsets.json'.format(tile_name, kwargs['sar_year']))

                if not os.path.exists(out_off_json):
                    print("rm {}".format(sar_base_img))
                    c_dict = dict()
                    c_dict['tile'] = tile_name
                    c_dict['sar_ref_img'] = sar_base_img
                    c_dict['sar_flt_buf_img'] = sar_flt_img
                    c_dict['out_flt_buf_img'] = out_off_img
                    c_dict['out_rsmpld_img'] = out_rsmp_img
                    c_dict['out_off_json'] = out_off_json
                    c_dict['tmpdir'] = os.path.join(kwargs['tmpdir'], "{}_{}_reg_scn".format(tile_name, kwargs['sar_year']))
                    self.params.append(c_dict)


    def run_gen_commands(self):
        self.gen_command_info(
            gmw_tiles='/scratch/a.pfb/gmw_v2_gapfill/data/gmw_tiles/gmw_init_v3_further_qa_part2/*.kea',
            sar_base_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2010',
            sar_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/1996',
            sar_year='1996',
            tmpdir='/scratch/a.pfb/gmw_v3_change/tmp')
        self.gen_command_info(
            gmw_tiles='/scratch/a.pfb/gmw_v2_gapfill/data/gmw_tiles/gmw_init_v3_further_qa_part2/*.kea',
            sar_base_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2010',
            sar_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2007',
            sar_year='2007',
            tmpdir='/scratch/a.pfb/gmw_v3_change/tmp')
        self.gen_command_info(
            gmw_tiles='/scratch/a.pfb/gmw_v2_gapfill/data/gmw_tiles/gmw_init_v3_further_qa_part2/*.kea',
            sar_base_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2010',
            sar_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2008',
            sar_year='2008',
            tmpdir='/scratch/a.pfb/gmw_v3_change/tmp')
        self.gen_command_info(
            gmw_tiles='/scratch/a.pfb/gmw_v2_gapfill/data/gmw_tiles/gmw_init_v3_further_qa_part2/*.kea',
            sar_base_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2010',
            sar_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2009',
            sar_year='2009',
            tmpdir='/scratch/a.pfb/gmw_v3_change/tmp')
        self.gen_command_info(
            gmw_tiles='/scratch/a.pfb/gmw_v2_gapfill/data/gmw_tiles/gmw_init_v3_further_qa_part2/*.kea',
            sar_base_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2010',
            sar_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2015',
            sar_year='2015',
            tmpdir='/scratch/a.pfb/gmw_v3_change/tmp')
        self.gen_command_info(
            gmw_tiles='/scratch/a.pfb/gmw_v2_gapfill/data/gmw_tiles/gmw_init_v3_further_qa_part2/*.kea',
            sar_base_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2010',
            sar_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2016',
            sar_year='2016',
            tmpdir='/scratch/a.pfb/gmw_v3_change/tmp')
        self.gen_command_info(
            gmw_tiles='/scratch/a.pfb/gmw_v2_gapfill/data/gmw_tiles/gmw_init_v3_further_qa_part2/*.kea',
            sar_base_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2010',
            sar_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2017',
            sar_year='2017',
            tmpdir='/scratch/a.pfb/gmw_v3_change/tmp')
        self.gen_command_info(
            gmw_tiles='/scratch/a.pfb/gmw_v2_gapfill/data/gmw_tiles/gmw_init_v3_further_qa_part2/*.kea',
            sar_base_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2010',
            sar_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2018',
            sar_year='2018',
            tmpdir='/scratch/a.pfb/gmw_v3_change/tmp')
        self.gen_command_info(
            gmw_tiles='/scratch/a.pfb/gmw_v2_gapfill/data/gmw_tiles/gmw_init_v3_further_qa_part2/*.kea',
            sar_base_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2010',
            sar_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2019',
            sar_year='2019',
            tmpdir='/scratch/a.pfb/gmw_v3_change/tmp')
        self.gen_command_info(
            gmw_tiles='/scratch/a.pfb/gmw_v2_gapfill/data/gmw_tiles/gmw_init_v3_further_qa_part2/*.kea',
            sar_base_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2010',
            sar_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2020',
            sar_year='2020',
            tmpdir='/scratch/a.pfb/gmw_v3_change/tmp')

        self.pop_params_db()
        self.create_slurm_sub_sh("gmw_sar_reg_imgs", 16448, '/scratch/a.pfb/gmw_v3_change/logs',
                                 run_script='run_exe_analysis.sh', job_dir="job_scripts",
                                 db_info_file=None, account_name='scw1376', n_cores_per_job=10, n_jobs=10,
                                 job_time_limit='2-23:59',
                                 module_load='module load parallel singularity\n\nexport http_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\nexport https_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\n')

if __name__ == "__main__":
    py_script = os.path.abspath("create_img_tile.py")
    script_cmd = "singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-beta-dev.sif python {}".format(py_script)

    process_tools_mod = 'create_img_tile'
    process_tools_cls = 'CreateImageTile'

    create_tools = GenCmds(cmd=script_cmd, db_conn_file="/home/a.pfb/gmw_gap_fill_db/pbpt_db_conn.txt",
                                         lock_file_path="./gmw_gapfill_lock_file.txt",
                                         process_tools_mod=process_tools_mod, process_tools_cls=process_tools_cls)
    create_tools.parse_cmds()
