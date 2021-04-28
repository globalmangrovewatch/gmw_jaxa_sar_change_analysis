from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib
import rsgislib.imagecalc
import rsgislib.imageutils
import rsgislib.rastergis


logger = logging.getLogger(__name__)

class MaskdBImages(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='mask_dB_images.py', descript=None)

    def do_processing(self, **kwargs):
        if not os.path.exists(self.params['tmp_dir']):
            os.mkdir(self.params['tmp_dir'])

        msk_file = os.path.join(self.params['tmp_dir'], '{}_invalid_msk.kea'.format(self.params['tile']))
        rsgislib.imagecalc.imageMath(self.params['vmsk_img'], msk_file, "(b1==0)||(b1==100)||(b1==150)?1:0", "KEA", rsgislib.TYPE_8UINT)

        rsgislib.imageutils.maskImage(self.params['sar_img'], msk_file, self.params['out_img'], "KEA", rsgislib.TYPE_16INT, 32767, 1)
        rsgislib.imageutils.popImageStats(self.params['out_img'], usenodataval=True, nodataval=32767, calcpyramids=True)

        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])


    def required_fields(self, **kwargs):
        return ["tile", "sar_img", "vmsk_img", "out_img", "tmp_dir"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_img']] = 'gdal_image'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_img']):
            os.remove(self.params['out_img'])

        # Reset the tmp dir
        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])
        os.mkdir(self.params['tmp_dir'])


if __name__ == "__main__":
    MaskdBImages().std_run()


