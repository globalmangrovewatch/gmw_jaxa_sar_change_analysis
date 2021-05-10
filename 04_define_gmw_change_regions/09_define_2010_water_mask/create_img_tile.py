from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib
import rsgislib.imagecalc
import rsgislib.imageutils
import rsgislib.rastergis

logger = logging.getLogger(__name__)


class CreateImageTile(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_img_tile.py', descript=None)

    def do_processing(self, **kwargs):
        if not os.path.exists(self.params['tmp_dir']):
            os.mkdir(self.params['tmp_dir'])

        if self.params['sar_img'] is None:
            rsgislib.imagecalc.imageMath(self.params['water_occur_img'], self.params['out_img'], '(b1>20)&&(b1<=100)?1:0', 'KEA', rsgislib.TYPE_8UINT)
            rsgislib.rastergis.populateStats(self.params['out_img'], addclrtab=True, calcpyramids=True, ignorezero=True)
        else:
            per_water_msk_img = os.path.join(self.params['tmp_dir'], '{}_perm_water.kea'.format(self.params['tile']))
            rsgislib.imagecalc.imageMath(self.params['water_occur_img'], per_water_msk_img, '(b1>90)&&(b1<=100)?1:0', 'KEA', rsgislib.TYPE_8UINT)
            rsgislib.rastergis.populateStats(per_water_msk_img, addclrtab=True, calcpyramids=False, ignorezero=True)

            n_pxl_vals = rsgislib.imagecalc.countPxlsOfVal(per_water_msk_img, vals=[1])
            if n_pxl_vals > 0:
                per_water_sar_img = os.path.join(self.params['tmp_dir'], '{}_perm_water_sar.kea'.format(self.params['tile']))
                rsgislib.imageutils.maskImage(self.params['sar_img'], per_water_msk_img, per_water_sar_img, 'KEA', rsgislib.TYPE_16INT, 30000, 0)

                sar_water_percent = rsgislib.imagecalc.bandPercentile(per_water_sar_img, 0.99, 30000)

                sar_hh_water_thres = sar_water_percent[0] - (sar_water_percent[0] * 0.15)
                sar_hv_water_thres = sar_water_percent[1] - (sar_water_percent[1] * 0.15)

            else:
                per_water_msk_img = os.path.join(self.params['tmp_dir'], '{}_perm_water.kea'.format(self.params['tile']))
                rsgislib.imagecalc.imageMath(self.params['water_occur_img'], per_water_msk_img, '(b1>70)&&(b1<=100)?1:0', 'KEA', rsgislib.TYPE_8UINT)
                rsgislib.rastergis.populateStats(per_water_msk_img, addclrtab=True, calcpyramids=False, ignorezero=True)

                n_pxl_vals = rsgislib.imagecalc.countPxlsOfVal(per_water_msk_img, vals=[1])
                if n_pxl_vals > 0:
                    per_water_sar_img = os.path.join(self.params['tmp_dir'], '{}_perm_water_sar.kea'.format(self.params['tile']))
                    rsgislib.imageutils.maskImage(self.params['sar_img'], per_water_msk_img, per_water_sar_img, 'KEA', rsgislib.TYPE_16INT, 30000, 0)

                    sar_water_percent = rsgislib.imagecalc.bandPercentile(per_water_sar_img, 0.99, 30000)

                    sar_hh_water_thres = sar_water_percent[0] - (sar_water_percent[0] * 0.15)
                    sar_hv_water_thres = sar_water_percent[1] - (sar_water_percent[1] * 0.15)
                else:
                    sar_hh_water_thres = -1600
                    sar_hv_water_thres = -1900

            print("sar_hh_water_thres = {}".format(sar_hh_water_thres))
            print("sar_hv_water_thres = {}".format(sar_hv_water_thres))

            band_defns = [rsgislib.imagecalc.BandDefn('woccur', self.params['water_occur_img'], 1),
                          rsgislib.imagecalc.BandDefn('hh', self.params['sar_img'], 1),
                          rsgislib.imagecalc.BandDefn('hv', self.params['sar_img'], 2)]
            exp = '(woccur > 5) && (hh < {}) && (hv < {})?1:0'.format(sar_hh_water_thres, sar_hv_water_thres)
            rsgislib.imagecalc.bandMath(self.params['out_img'], exp, 'KEA', rsgislib.TYPE_8UINT, band_defns)
            rsgislib.rastergis.populateStats(self.params['out_img'], addclrtab=True, calcpyramids=True, ignorezero=True)





        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])


    def required_fields(self, **kwargs):
        return ["tile", "water_occur_img", "sar_img", "out_img", "tmp_dir"]


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
    CreateImageTile().std_run()


