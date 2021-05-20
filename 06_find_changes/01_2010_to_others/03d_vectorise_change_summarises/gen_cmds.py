from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import logging
import os
import glob

logger = logging.getLogger(__name__)

class GenCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        if not os.path.exists(kwargs['out_dir']):
            os.mkdir(kwargs['out_dir'])

        img_tiles = glob.glob(kwargs['img_srch'])
        for img_tile in img_tiles:
            basename = self.get_file_basename(img_tile)

            out_vec = os.path.join(kwargs['out_dir'], '{}.gpkg'.format(basename))
            out_cmp_file = os.path.join(kwargs['out_dir'], '{}.txt'.format(basename))

            if not os.path.exists(out_cmp_file):
                c_dict = dict()
                c_dict['img_tile'] = img_tile
                c_dict['out_vec'] = out_vec
                c_dict['out_lyr_name'] = kwargs['out_lyr_name']
                c_dict['out_cmp_file'] = out_cmp_file
                self.params.append(c_dict)


    def run_gen_commands(self):
        self.gen_command_info(
            img_srch='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_pre_2010_chngs/*_sum_not_mng_chng.kea',
            out_lyr_name='pre_2010_mng_loss',
            out_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_pre_2010_chngs_vecs')

        self.gen_command_info(
            img_srch='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_pre_2010_chngs/*_sum_mng_chng.kea',
            out_lyr_name='pre_2010_mng_gain',
            out_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_pre_2010_chngs_vecs')

        self.gen_command_info(
                img_srch='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_post_2010_chngs/*_sum_not_mng_chng.kea',
                out_lyr_name='pre_2010_mng_gain',
                out_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_post_2010_chngs_vecs')

        self.gen_command_info(
                img_srch='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_post_2010_chngs/*_sum_mng_chng.kea',
                out_lyr_name='pre_2010_mng_loss',
                out_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_post_2010_chngs_vecs')

        self.pop_params_db()
        self.create_slurm_sub_sh("gmw_vec_chng_sum", 16448, '/scratch/a.pfb/gmw_v3_change/logs',
                                 run_script='run_exe_analysis.sh', job_dir="job_scripts",
                                 db_info_file=None, account_name='scw1376', n_cores_per_job=10, n_jobs=10,
                                 job_time_limit='2-23:59',
                                 module_load='module load parallel singularity\n\nexport http_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\nexport https_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\n')

if __name__ == "__main__":
    py_script = os.path.abspath("create_vec_tile.py")
    script_cmd = "singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python {}".format(py_script)

    process_tools_mod = 'create_vec_tile'
    process_tools_cls = 'CreateVectorTile'

    create_tools = GenCmds(cmd=script_cmd, db_conn_file="/home/a.pfb/gmw_gap_fill_db/pbpt_db_conn.txt",
                                         lock_file_path="./gmw_gapfill_lock_file.txt",
                                         process_tools_mod=process_tools_mod, process_tools_cls=process_tools_cls)
    create_tools.parse_cmds()
