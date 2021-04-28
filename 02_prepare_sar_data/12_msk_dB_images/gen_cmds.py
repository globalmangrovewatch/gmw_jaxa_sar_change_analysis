from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import logging
import os
import glob

logger = logging.getLogger(__name__)

class GenCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        input_imgs = glob.glob(kwargs['tiles_path'])
        for dB_img in input_imgs:
            basename = self.get_file_basename(dB_img, n_comps=2)
            tile_name = basename.split('_')[0]
            img_dir = os.path.dirname(dB_img)

            vmsk_img = os.path.join(img_dir, '{}_vmsk.kea'.format(basename))
            out_dB_img = os.path.join(img_dir, '{}_db_mskd.kea'.format(basename))

            if (not os.path.exists(out_dB_img)):
                c_dict = dict()
                c_dict['tile'] = tile_name
                c_dict['sar_img'] = dB_img
                c_dict['vmsk_img'] = vmsk_img
                c_dict['out_img'] = out_dB_img
                c_dict['tmp_dir'] = os.path.join(kwargs['tmp_dir'], "{}_msk_ard".format(tile_name))
                if not os.path.exists(c_dict['tmp_dir']):
                    os.mkdir(c_dict['tmp_dir'])
                self.params.append(c_dict)


    def run_gen_commands(self):
        self.gen_command_info(tiles_path='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/*/*/*_db.kea',
                              tmp_dir='/scratch/a.pfb/gmw_v2_gapfill/tmp')
        self.pop_params_db()
        self.create_slurm_sub_sh("mask_dB_images", 16448, '/scratch/a.pfb/gmw_v3_change/logs',
                                 run_script='run_exe_analysis.sh', job_dir="job_scripts",
                                 db_info_file=None, account_name='scw1376', n_cores_per_job=10, n_jobs=10,
                                 job_time_limit='2-23:59',
                                 module_load='module load parallel singularity\n\nexport http_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\nexport https_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\n')

if __name__ == "__main__":
    py_script = os.path.abspath("mask_dB_images.py")
    script_cmd = "singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python {}".format(py_script)

    process_tools_mod = 'mask_dB_images'
    process_tools_cls = 'MaskdBImages'

    create_tools = GenCmds(cmd=script_cmd, db_conn_file="/home/a.pfb/gmw_gap_fill_db/pbpt_db_conn.txt",
                                         lock_file_path="./gmw_gapfill_lock_file.txt",
                                         process_tools_mod=process_tools_mod, process_tools_cls=process_tools_cls)
    create_tools.parse_cmds()
