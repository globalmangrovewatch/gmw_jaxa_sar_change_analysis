from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import math
import pprint
import rsgislib
import rsgislib.rastergis
import rsgislib.imagecalc
import rsgislib.imageutils

def create_1996_mng_msk(gmw_tile, sar_img, sar_vld_img, threshold, threshold_se, out_img, out_lower_img, out_upper_img, calc_intervals=True):
    # 95th intervals
    threshold_upper = threshold + (threshold_se * 1.96)
    threshold_lower = threshold - (threshold_se * 1.96)

    # Using threshold
    band_defns = []
    band_defns.append(rsgislib.imagecalc.BandDefn('gmw', gmw_tile, 1))
    band_defns.append(rsgislib.imagecalc.BandDefn('hh', sar_img, 1))
    band_defns.append(rsgislib.imagecalc.BandDefn('vld', sar_vld_img, 1))
    exp = '(vld==1)&&(gmw==1)&&(hh<{})?1:0'.format(threshold)
    rsgislib.imagecalc.bandMath(out_img, exp, 'KEA', rsgislib.TYPE_8UINT, band_defns)
    rsgislib.rastergis.populateStats(out_img, True, True, True)

    if calc_intervals:
        # Using upper threshold
        band_defns = []
        band_defns.append(rsgislib.imagecalc.BandDefn('gmw', gmw_tile, 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('hh', sar_img, 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('vld', sar_vld_img, 1))
        exp = '(vld==1)&&(gmw==1)&&(hh<{})?1:0'.format(threshold_upper)
        rsgislib.imagecalc.bandMath(out_upper_img, exp, 'KEA', rsgislib.TYPE_8UINT, band_defns)
        rsgislib.rastergis.populateStats(out_upper_img, True, True, True)

        # Using lower threshold
        band_defns = []
        band_defns.append(rsgislib.imagecalc.BandDefn('gmw', gmw_tile, 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('hh', sar_img, 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('vld', sar_vld_img, 1))
        exp = '(vld==1)&&(gmw==1)&&(hh<{})?1:0'.format(threshold_lower)
        rsgislib.imagecalc.bandMath(out_lower_img, exp, 'KEA', rsgislib.TYPE_8UINT, band_defns)
        rsgislib.rastergis.populateStats(out_lower_img, True, True, True)


def create_1996_nmng_msk(chng_rgn_tile, sar_img, sar_vld_img, threshold, threshold_se, out_img, out_lower_img, out_upper_img, calc_intervals=True):
    # 95th intervals
    threshold_upper = threshold + (threshold_se * 1.96)
    threshold_lower = threshold - (threshold_se * 1.96)

    # Using threshold
    band_defns = []
    band_defns.append(rsgislib.imagecalc.BandDefn('chgmsk', chng_rgn_tile, 1))
    band_defns.append(rsgislib.imagecalc.BandDefn('hh', sar_img, 1))
    band_defns.append(rsgislib.imagecalc.BandDefn('vld', sar_vld_img, 1))
    exp = '(vld==1)&&(chgmsk==1)&&(hh>{})?1:0'.format(threshold)
    rsgislib.imagecalc.bandMath(out_img, exp, 'KEA', rsgislib.TYPE_8UINT, band_defns)
    rsgislib.rastergis.populateStats(out_img, True, True, True)

    if calc_intervals:
        # Using upper threshold
        band_defns = []
        band_defns.append(rsgislib.imagecalc.BandDefn('chgmsk', chng_rgn_tile, 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('hh', sar_img, 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('vld', sar_vld_img, 1))
        exp = '(vld==1)&&(chgmsk==1)&&(hh>{})?1:0'.format(threshold_upper)
        rsgislib.imagecalc.bandMath(out_upper_img, exp, 'KEA', rsgislib.TYPE_8UINT, band_defns)
        rsgislib.rastergis.populateStats(out_upper_img, True, True, True)

        # Using lower threshold
        band_defns = []
        band_defns.append(rsgislib.imagecalc.BandDefn('chgmsk', chng_rgn_tile, 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('hh', sar_img, 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('vld', sar_vld_img, 1))
        exp = '(vld==1)&&(chgmsk==1)&&(hh>{})?1:0'.format(threshold_lower)
        rsgislib.imagecalc.bandMath(out_lower_img, exp, 'KEA', rsgislib.TYPE_8UINT, band_defns)
        rsgislib.rastergis.populateStats(out_lower_img, True, True, True)




def create_alos_mng_msk(gmw_tile, sar_img, sar_vld_img, threshold, threshold_se, out_img, out_lower_img, out_upper_img, calc_intervals=True):
    # 95th intervals
    threshold_upper = threshold + (threshold_se * 1.96)
    threshold_lower = threshold - (threshold_se * 1.96)

    # Using threshold
    band_defns = []
    band_defns.append(rsgislib.imagecalc.BandDefn('gmw', gmw_tile, 1))
    band_defns.append(rsgislib.imagecalc.BandDefn('hv', sar_img, 2))
    band_defns.append(rsgislib.imagecalc.BandDefn('vld', sar_vld_img, 1))
    exp = '(vld==1)&&(gmw==1)&&(hv<{})?1:0'.format(threshold)
    rsgislib.imagecalc.bandMath(out_img, exp, 'KEA', rsgislib.TYPE_8UINT, band_defns)
    rsgislib.rastergis.populateStats(out_img, True, True, True)

    if calc_intervals:
        # Using upper threshold
        band_defns = []
        band_defns.append(rsgislib.imagecalc.BandDefn('gmw', gmw_tile, 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('hv', sar_img, 2))
        band_defns.append(rsgislib.imagecalc.BandDefn('vld', sar_vld_img, 1))
        exp = '(vld==1)&&(gmw==1)&&(hv<{})?1:0'.format(threshold_upper)
        rsgislib.imagecalc.bandMath(out_upper_img, exp, 'KEA', rsgislib.TYPE_8UINT, band_defns)
        rsgislib.rastergis.populateStats(out_upper_img, True, True, True)

        # Using lower threshold
        band_defns = []
        band_defns.append(rsgislib.imagecalc.BandDefn('gmw', gmw_tile, 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('hv', sar_img, 2))
        band_defns.append(rsgislib.imagecalc.BandDefn('vld', sar_vld_img, 1))
        exp = '(vld==1)&&(gmw==1)&&(hv<{})?1:0'.format(threshold_lower)
        rsgislib.imagecalc.bandMath(out_lower_img, exp, 'KEA', rsgislib.TYPE_8UINT, band_defns)
        rsgislib.rastergis.populateStats(out_lower_img, True, True, True)



def create_alos_nmng_msk(chng_rgn_tile, sar_img, sar_vld_img, threshold, threshold_se, out_img, out_lower_img, out_upper_img, calc_intervals=True):
    # 95th intervals
    threshold_upper = threshold + (threshold_se * 1.96)
    threshold_lower = threshold - (threshold_se * 1.96)

    # Using threshold
    band_defns = []
    band_defns.append(rsgislib.imagecalc.BandDefn('chgmsk', chng_rgn_tile, 1))
    band_defns.append(rsgislib.imagecalc.BandDefn('hv', sar_img, 2))
    band_defns.append(rsgislib.imagecalc.BandDefn('vld', sar_vld_img, 1))
    exp = '(vld==1)&&(chgmsk==1)&&(hv>{})?1:0'.format(threshold)
    rsgislib.imagecalc.bandMath(out_img, exp, 'KEA', rsgislib.TYPE_8UINT, band_defns)
    rsgislib.rastergis.populateStats(out_img, True, True, True)

    if calc_intervals:
        # Using upper threshold
        band_defns = []
        band_defns.append(rsgislib.imagecalc.BandDefn('chgmsk', chng_rgn_tile, 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('hv', sar_img, 2))
        band_defns.append(rsgislib.imagecalc.BandDefn('vld', sar_vld_img, 1))
        exp = '(vld==1)&&(chgmsk==1)&&(hv>{})?1:0'.format(threshold_upper)
        rsgislib.imagecalc.bandMath(out_upper_img, exp, 'KEA', rsgislib.TYPE_8UINT, band_defns)
        rsgislib.rastergis.populateStats(out_upper_img, True, True, True)

        # Using lower threshold
        band_defns = []
        band_defns.append(rsgislib.imagecalc.BandDefn('chgmsk', chng_rgn_tile, 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('hv', sar_img, 2))
        band_defns.append(rsgislib.imagecalc.BandDefn('vld', sar_vld_img, 1))
        exp = '(vld==1)&&(chgmsk==1)&&(hv>{})?1:0'.format(threshold_lower)
        rsgislib.imagecalc.bandMath(out_lower_img, exp, 'KEA', rsgislib.TYPE_8UINT, band_defns)
        rsgislib.rastergis.populateStats(out_lower_img, True, True, True)

logger = logging.getLogger(__name__)

class CreateImageTile(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_img_tile.py', descript=None)

    def do_processing(self, **kwargs):
        if not os.path.exists(self.params['tmp_dir']):
            os.mkdir(self.params['tmp_dir'])

        if self.params['sar_img'] is not None:
            rsgis_utils = rsgislib.RSGISPyUtils()
            thres_lut = rsgis_utils.readJSON2Dict(self.params['gmw_proj_thres_file'])
            pprint.pprint(thres_lut)

            if self.params['sar_year'] == '1996':
                mng_hh_thres = thres_lut[self.params['sar_year']]['mng_hh']
                mng_hh_thres_se = thres_lut[self.params['sar_year']]['mng_hh_se']
                if math.isnan(mng_hh_thres_se):
                    mng_hh_thres_se = 0.0
                create_1996_mng_msk(self.params['gmw_tile'], self.params['sar_img'], self.params['sar_vld_img'], mng_hh_thres, mng_hh_thres_se, self.params['out_mng_chng'], self.params['out_mng_chng_lower'], self.params['out_mng_chng_upper'], self.params['calc_intervals'])

                nmng_hh_thres = thres_lut[self.params['sar_year']]['nmng_hh']
                nmng_hh_thres_se = thres_lut[self.params['sar_year']]['nmng_hh_se']
                if math.isnan(nmng_hh_thres_se):
                    nmng_hh_thres_se = 0.0
                create_1996_nmng_msk(self.params['potent_chng_msk_img'], self.params['sar_img'], self.params['sar_vld_img'], nmng_hh_thres, nmng_hh_thres_se, self.params['out_nmng_chng'], self.params['out_nmng_chng_lower'], self.params['out_nmng_chng_upper'], self.params['calc_intervals'])

            else:
                mng_hv_thres = thres_lut[self.params['sar_year']]['mng_hv']
                mng_hv_thres_se = thres_lut[self.params['sar_year']]['mng_hv_se']
                if math.isnan(mng_hv_thres_se):
                    mng_hv_thres_se = 0.0
                create_alos_mng_msk(self.params['gmw_tile'], self.params['sar_img'], self.params['sar_vld_img'], mng_hv_thres, mng_hv_thres_se, self.params['out_mng_chng'], self.params['out_mng_chng_lower'], self.params['out_mng_chng_upper'], self.params['calc_intervals'])

                nmng_hv_thres = thres_lut[self.params['sar_year']]['nmng_hv']
                nmng_hv_thres_se = thres_lut[self.params['sar_year']]['nmng_hv_se']
                if math.isnan(nmng_hv_thres_se):
                    nmng_hv_thres_se = 0.0
                create_alos_nmng_msk(self.params['potent_chng_msk_img'], self.params['sar_img'], self.params['sar_vld_img'], nmng_hv_thres, nmng_hv_thres_se, self.params['out_nmng_chng'], self.params['out_nmng_chng_lower'], self.params['out_nmng_chng_upper'], self.params['calc_intervals'])
        else:
            rsgislib.imagecalc.imageMath(self.params['gmw_tile'], self.params['out_mng_chng'], '0', 'KEA', rsgislib.TYPE_8UINT)
            rsgislib.imagecalc.imageMath(self.params['gmw_tile'], self.params['out_nmng_chng'], '0', 'KEA', rsgislib.TYPE_8UINT)
            if self.params['calc_intervals']:
                rsgislib.imagecalc.imageMath(self.params['gmw_tile'], self.params['out_mng_chng_lower'], '0', 'KEA', rsgislib.TYPE_8UINT)
                rsgislib.imagecalc.imageMath(self.params['gmw_tile'], self.params['out_nmng_chng_lower'], '0', 'KEA', rsgislib.TYPE_8UINT)
                rsgislib.imagecalc.imageMath(self.params['gmw_tile'], self.params['out_mng_chng_upper'], '0', 'KEA', rsgislib.TYPE_8UINT)
                rsgislib.imagecalc.imageMath(self.params['gmw_tile'], self.params['out_nmng_chng_upper'], '0', 'KEA', rsgislib.TYPE_8UINT)

        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])


    def required_fields(self, **kwargs):
        return ["tile", "gmw_tile", "sar_year", "potent_chng_msk_img", "sar_img", "sar_vld_img",
                "gmw_proj_thres_file", "out_mng_chng", "out_nmng_chng", "out_mng_chng_upper",
                "out_nmng_chng_upper", "out_mng_chng_lower", "out_nmng_chng_lower", "calc_intervals"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_mng_chng']] = 'gdal_image'
        files_dict[self.params['out_nmng_chng']] = 'gdal_image'
        if self.params['calc_intervals']:
            files_dict[self.params['out_mng_chng_upper']] = 'gdal_image'
            files_dict[self.params['out_nmng_chng_upper']] = 'gdal_image'
            files_dict[self.params['out_mng_chng_lower']] = 'gdal_image'
            files_dict[self.params['out_nmng_chng_lower']] = 'gdal_image'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_mng_chng']):
            os.remove(self.params['out_mng_chng'])

        if os.path.exists(self.params['out_nmng_chng']):
            os.remove(self.params['out_nmng_chng'])

        if self.params['calc_intervals']:
            if os.path.exists(self.params['out_mng_chng_upper']):
                os.remove(self.params['out_mng_chng_upper'])

            if os.path.exists(self.params['out_nmng_chng_upper']):
                os.remove(self.params['out_nmng_chng_upper'])

            if os.path.exists(self.params['out_mng_chng_lower']):
                os.remove(self.params['out_mng_chng_lower'])

            if os.path.exists(self.params['out_nmng_chng_lower']):
                os.remove(self.params['out_nmng_chng_lower'])

        # Reset the tmp dir
        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])
        os.mkdir(self.params['tmp_dir'])

if __name__ == "__main__":
    CreateImageTile().std_run()


