from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import logging
import os
import glob
import rsgislib

logger = logging.getLogger(__name__)

class GenCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        rsgis_utils = rsgislib.RSGISPyUtils()
        tile_prj_lut = rsgis_utils.readJSON2Dict(kwargs['prjs_lut_file'])

        img_tiles = glob.glob(kwargs['gmw_tiles'])
        for gmw_tile in img_tiles:
            basename = self.get_file_basename(gmw_tile)
            tile_basename = self.get_file_basename(gmw_tile, n_comps=2)
            tile_name = tile_basename.split('_')[1]

            sar_scn_dir = os.path.join(kwargs['sar_tiles_dir'], tile_name)
            sar_img = os.path.join(sar_scn_dir, '{}_1996_db.kea'.format(tile_name))
            if os.path.exists(sar_img):
                gmw_prj = tile_prj_lut[tile_name]

                jers1_prj_dB_file = self.find_file(kwargs['v2_jers1_prjs_dir'], '{}*dB.kea'.format(gmw_prj))
                if jers1_prj_dB_file is not None:

                    out_sar_scn_dir = os.path.join(kwargs['out_dir'], tile_name)
                    if not os.path.exists(out_sar_scn_dir):
                        os.mkdir(out_sar_scn_dir)

                    out_img = os.path.join(out_sar_scn_dir, '{}_1996_db.kea'.format(tile_name))
                    out_cmp_file = os.path.join(kwargs['out_dir'], '{}_1996_sar.txt'.format(tile_name))

                    if (not os.path.exists(out_cmp_file)):
                        c_dict = dict()
                        c_dict['tile'] = tile_name
                        c_dict['gmw_tile'] = gmw_tile
                        c_dict['jers1_prj_dB_file'] = jers1_prj_dB_file
                        c_dict['sar_img'] = sar_img
                        c_dict['out_img'] = out_img
                        c_dict['out_cmp_file'] = out_cmp_file
                        c_dict['tmp_dir'] = os.path.join(kwargs['tmp_dir'], "{}_1996_reg_db".format(tile_basename))
                        if not os.path.exists(c_dict['tmp_dir']):
                            os.mkdir(c_dict['tmp_dir'])
                        self.params.append(c_dict)


    def run_gen_commands(self):
        self.gen_command_info(gmw_tiles='/scratch/a.pfb/gmw_v2_gapfill/data/gmw_tiles/gmw_init_v3_further_qa_part2/*.kea',
                              prjs_lut_file='/scratch/a.pfb/gmw_v3_change/scripts/03_prepare_datasets/09_create_project_tile_lut/gmw_tiles_luts.json',
                              sar_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/1996',
                              v2_jers1_prjs_dir='/scratch/a.pfb/gmw_v3_change/data/jaxa_dwnlds/gmw_v2_1996_reg_prj_files',
                              out_dir='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/1996_v2_reg',
                              tmp_dir='/scratch/a.pfb/gmw_v3_change/tmp')
        self.pop_params_db()
        self.create_slurm_sub_sh("gmw_2010_v3", 16448, '/scratch/a.pfb/gmw_v3_change/logs',
                                 run_script='run_exe_analysis.sh', job_dir="job_scripts",
                                 db_info_file=None, account_name='scw1376', n_cores_per_job=10, n_jobs=10,
                                 job_time_limit='2-23:59',
                                 module_load='module load parallel singularity\n\nexport http_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\nexport https_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\n')

if __name__ == "__main__":
    py_script = os.path.abspath("create_img_tile.py")
    script_cmd = "singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python {}".format(py_script)

    process_tools_mod = 'create_img_tile'
    process_tools_cls = 'CreateImageTile'

    create_tools = GenCmds(cmd=script_cmd, db_conn_file="/home/a.pfb/gmw_gap_fill_db/pbpt_db_conn.txt",
                                         lock_file_path="./gmw_gapfill_lock_file.txt",
                                         process_tools_mod=process_tools_mod, process_tools_cls=process_tools_cls)
    create_tools.parse_cmds()
