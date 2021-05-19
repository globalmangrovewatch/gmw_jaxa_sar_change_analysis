from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import logging
import os
import glob

logger = logging.getLogger(__name__)


class GenCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        if not os.path.exists(kwargs['out_dir']):
            os.mkdir(kwargs['out_dir'])

        img_tiles = glob.glob(kwargs['gmw_tiles'])
        for gmw_tile in img_tiles:
            basename = self.get_file_basename(gmw_tile)
            tile_basename = self.get_file_basename(gmw_tile, n_comps=2)

            mng_chng_img = os.path.join(kwargs['chng_img_dir'], '{}_{}_mng_chng.kea'.format(tile_basename, kwargs['sar_year']))
            nmng_chng_img = os.path.join(kwargs['chng_img_dir'], '{}_{}_not_mng_chng.kea'.format(tile_basename, kwargs['sar_year']))

            v2_chng_rgn_img = os.path.join(kwargs['out_dir'], '{}_v2_chng_from_2010.kea'.format(tile_basename))

            out_mng_chng_fnl_img = os.path.join(kwargs['out_dir'], '{}_{}_mng_chng.kea'.format(tile_basename, kwargs['sar_year']))
            out_nmng_chng_fnl_img = os.path.join(kwargs['out_dir'], '{}_{}_not_mng_chng.kea'.format(tile_basename, kwargs['sar_year']))

            if not os.path.exists(out_mng_chng_fnl_img):
                print("rm {}".format(mng_chng_img))
                c_dict = dict()
                c_dict['tile'] = tile_basename
                c_dict['chng_img'] = mng_chng_img
                c_dict['v2_chng_rgn_img'] = v2_chng_rgn_img
                c_dict['qa_chng_rgns_file'] = kwargs['qa_chng_rgns_file']
                c_dict['qa_chng_rgns_lyr'] = kwargs['qa_chng_rgns_lyr']
                c_dict['out_img'] = out_mng_chng_fnl_img
                c_dict['tmp_dir'] = os.path.join(kwargs['tmp_dir'], "{}_{}_fnl_pre2010_mng_chng".format(tile_basename, kwargs['sar_year']))
                if not os.path.exists(c_dict['tmp_dir']):
                    os.mkdir(c_dict['tmp_dir'])
                self.params.append(c_dict)

            if not os.path.exists(out_nmng_chng_fnl_img):
                print("rm {}".format(nmng_chng_img))
                c_dict = dict()
                c_dict['tile'] = tile_basename
                c_dict['chng_img'] = nmng_chng_img
                c_dict['v2_chng_rgn_img'] = v2_chng_rgn_img
                c_dict['qa_chng_rgns_file'] = kwargs['qa_chng_rgns_file']
                c_dict['qa_chng_rgns_lyr'] = kwargs['qa_chng_rgns_lyr']
                c_dict['out_img'] = out_nmng_chng_fnl_img
                c_dict['tmp_dir'] = os.path.join(kwargs['tmp_dir'], "{}_{}_fnl_pre2010_not_mng_chng".format(tile_basename, kwargs['sar_year']))
                if not os.path.exists(c_dict['tmp_dir']):
                    os.mkdir(c_dict['tmp_dir'])
                self.params.append(c_dict)

    def run_gen_commands(self):

        for year in ['1996', '2007', '2008', '2009']:
            self.gen_command_info(gmw_tiles='/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_2010_v3/*.kea',
                                  chng_img_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_{}_chngs_rmsml'.format(year),
                                  sar_year=year,
                                  v2_chng_rgns='/scratch/a.pfb/gmw_v3_change/data/other_base_data/gmw_v2_chng_from_2010',
                                  qa_chng_rgns_file='/scratch/a.pfb/gmw_v3_change/scripts/06_find_changes/01_2010_to_others/03e_define_pre2010_change_regions/add_chng_rgns.gpkg',
                                  qa_chng_rgns_lyr='add_chng_rgns',
                                  out_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_{}_chngs_rmsml_fnl'.format(year),
                                  tmp_dir='/scratch/a.pfb/gmw_v3_change/tmp')

        self.pop_params_db()
        self.create_slurm_sub_sh("gmw_fnl_pre_2010_chng_rgns", 16448, '/scratch/a.pfb/gmw_v3_change/logs',
                                 run_script='run_exe_analysis.sh', job_dir="job_scripts",
                                 db_info_file=None, account_name='scw1376', n_cores_per_job=10, n_jobs=10,
                                 n_xtr_cmds=20, job_time_limit='2-23:59',
                                 module_load='module load parallel singularity\n\nexport http_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\nexport https_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\n')


if __name__ == "__main__":
    py_script = os.path.abspath("create_img_tile.py")
    script_cmd = "singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python {}".format(
        py_script)

    process_tools_mod = 'create_img_tile'
    process_tools_cls = 'CreateImageTile'

    create_tools = GenCmds(cmd=script_cmd, db_conn_file="/home/a.pfb/gmw_gap_fill_db/pbpt_db_conn.txt",
                           lock_file_path="./gmw_gapfill_lock_file.txt",
                           process_tools_mod=process_tools_mod, process_tools_cls=process_tools_cls)
    create_tools.parse_cmds()
