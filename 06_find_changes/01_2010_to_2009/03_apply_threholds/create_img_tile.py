from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import rsgislib
import rsgislib.rastergis
import rsgislib.imagecalc

logger = logging.getLogger(__name__)

class CreateImageTile(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_img_tile.py', descript=None)

    def do_processing(self, **kwargs):
        if self.params['sar_img'] is not None:
            rsgis_utils = rsgislib.RSGISPyUtils()
            thres_lut = rsgis_utils.readJSON2Dict(self.params['gmw_proj_thres_file'])

            # Threshold the mangrove regions (Mangroves > Not Mangroves)
            if (thres_lut['mng_hh'] < 0.0) and (thres_lut['mng_hv'] < 0.0):
                band_defns = []
                band_defns.append(rsgislib.imagecalc.BandDefn('gmw', self.params['gmw_tile'], 1))
                band_defns.append(rsgislib.imagecalc.BandDefn('hh', self.params['sar_img'], 1))
                band_defns.append(rsgislib.imagecalc.BandDefn('hv', self.params['sar_img'], 2))
                band_defns.append(rsgislib.imagecalc.BandDefn('vld', self.params['sar_vld_img'], 1))
                exp = '(vld==1)&&(gmw==1)&&(hh<{})&&(hv<{})?1:0'.format(thres_lut['mng_hh'], thres_lut['mng_hv'])
                rsgislib.imagecalc.bandMath(self.params['out_mng_chng'], exp, 'KEA', rsgislib.TYPE_8UINT, band_defns)
            elif thres_lut['mng_hh'] < 0.0:
                band_defns = []
                band_defns.append(rsgislib.imagecalc.BandDefn('gmw', self.params['gmw_tile'], 1))
                band_defns.append(rsgislib.imagecalc.BandDefn('hh', self.params['sar_img'], 1))
                band_defns.append(rsgislib.imagecalc.BandDefn('vld', self.params['sar_vld_img'], 1))
                exp = '(vld==1)&&(gmw==1)&&(hh<{})?1:0'.format(thres_lut['mng_hh'])
                rsgislib.imagecalc.bandMath(self.params['out_mng_chng'], exp, 'KEA', rsgislib.TYPE_8UINT, band_defns)
            else:
                rsgislib.imagecalc.imageMath(self.params['gmw_tile'], self.params['out_mng_chng'], '0', 'KEA', rsgislib.TYPE_8UINT)


            # Threshold the potential change features (Not Mangrove > Mangroves)
            if (thres_lut['nmng_hh'] < 0.0) and (thres_lut['nmng_hv'] < 0.0):
                band_defns = []
                band_defns.append(rsgislib.imagecalc.BandDefn('chgmsk', self.params['potent_chng_msk_img'], 1))
                band_defns.append(rsgislib.imagecalc.BandDefn('hh', self.params['sar_img'], 1))
                band_defns.append(rsgislib.imagecalc.BandDefn('hv', self.params['sar_img'], 2))
                band_defns.append(rsgislib.imagecalc.BandDefn('vld', self.params['sar_vld_img'], 1))
                exp = '(vld==1)&&(chgmsk==1)&&(hh>{})&&(hv>{})?1:0'.format(thres_lut['nmng_hh'], thres_lut['nmng_hv'])
                rsgislib.imagecalc.bandMath(self.params['out_nmng_chng'], exp, 'KEA', rsgislib.TYPE_8UINT, band_defns)
            elif thres_lut['nmng_hh'] < 0.0:
                band_defns = []
                band_defns.append(rsgislib.imagecalc.BandDefn('chgmsk', self.params['potent_chng_msk_img'], 1))
                band_defns.append(rsgislib.imagecalc.BandDefn('hh', self.params['sar_img'], 1))
                band_defns.append(rsgislib.imagecalc.BandDefn('vld', self.params['sar_vld_img'], 1))
                exp = '(vld==1)&&(chgmsk==1)&&(hh>{})?1:0'.format(thres_lut['nmng_hh'])
                rsgislib.imagecalc.bandMath(self.params['out_nmng_chng'], exp, 'KEA', rsgislib.TYPE_8UINT, band_defns)
            else:
                rsgislib.imagecalc.imageMath(self.params['gmw_tile'], self.params['out_nmng_chng'], '0', 'KEA', rsgislib.TYPE_8UINT)
        else:
            rsgislib.imagecalc.imageMath(self.params['gmw_tile'], self.params['out_mng_chng'], '0', 'KEA', rsgislib.TYPE_8UINT)
            rsgislib.imagecalc.imageMath(self.params['gmw_tile'], self.params['out_nmng_chng'], '0', 'KEA', rsgislib.TYPE_8UINT)

        rsgislib.rastergis.populateStats(self.params['out_mng_chng'], True, True, True)
        rsgislib.rastergis.populateStats(self.params['out_nmng_chng'], True, True, True)


    def required_fields(self, **kwargs):
        return ["tile", "gmw_tile", "potent_chng_msk_img", "sar_img", "sar_vld_img", "gmw_proj_thres_file", "out_mng_chng", "out_nmng_chng"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_mng_chng']] = 'gdal_image'
        files_dict[self.params['out_nmng_chng']] = 'gdal_image'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_mng_chng']):
            os.remove(self.params['out_mng_chng'])

        if os.path.exists(self.params['out_nmng_chng']):
            os.remove(self.params['out_nmng_chng'])

if __name__ == "__main__":
    CreateImageTile().std_run()


