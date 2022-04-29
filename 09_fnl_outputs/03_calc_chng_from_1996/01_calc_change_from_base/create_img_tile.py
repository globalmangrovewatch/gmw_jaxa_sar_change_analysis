from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import rsgislib.imagecalc
import rsgislib.imageutils

logger = logging.getLogger(__name__)

class CreateImageTile(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_img_tile.py', descript=None)

    def do_processing(self, **kwargs):
        band_defns = list()
        band_defns.append(rsgislib.imagecalc.BandDefn('base', self.params['gmw_base_tile'], 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('chng', self.params['gmw_chg_img'], 1))
        rsgislib.imagecalc.band_math(self.params['out_img'], "(base==0)&&(chng==1)?1:(base==1)&&(chng==0)?2:0", 'KEA', rsgislib.TYPE_8UINT, band_defns)
        rsgislib.imageutils.pop_thmt_img_stats(self.params['out_img'])

        clr_lut = dict()
        clr_lut[1] = '#FF0000'
        clr_lut[2] = '#0000FF'
        rsgislib.imageutils.define_colour_table(self.params['out_img'], clr_lut)


    def required_fields(self, **kwargs):
        return ["gmw_base_tile", "gmw_chg_img", "out_img"]


    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_img']] = 'gdal_image'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_img']):
            os.remove(self.params['out_img'])

if __name__ == "__main__":
    CreateImageTile().std_run()


