from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import pprint
import rsgislib
import rsgislib.rastergis
import rsgislib.imagecalc
import rsgislib.imageutils
import numpy

def create_1996_mng_msk(gmw_tile, sar_img, sar_vld_img, threshold, out_img, out_uncertain_img, tmp_dir, thres_var=2, n_steps=10):

    step_intvl = thres_var / int(n_steps/2)
    threshold_steps = numpy.arange(1, int(n_steps/2)) * step_intvl
    rsgis_utils = rsgislib.RSGISPyUtils()
    basename = rsgis_utils.get_file_basename(out_img)

    imgs = list()

    # Using threshold
    band_defns = []
    band_defns.append(rsgislib.imagecalc.BandDefn('gmw', gmw_tile, 1))
    band_defns.append(rsgislib.imagecalc.BandDefn('hh', sar_img, 1))
    band_defns.append(rsgislib.imagecalc.BandDefn('vld', sar_vld_img, 1))
    exp = '(vld==1)&&(gmw==1)&&(hh<{})?1:0'.format(threshold)
    rsgislib.imagecalc.bandMath(out_img, exp, 'KEA', rsgislib.TYPE_8UINT, band_defns)
    rsgislib.rastergis.populateStats(out_img, True, True, True)
    imgs.append(out_img)

    # Add intervals
    i = 1
    for step in threshold_steps:
        out_tmp_img = os.path.join(tmp_dir, "{}_img_{}.kea".format(basename, i))
        band_defns = []
        band_defns.append(rsgislib.imagecalc.BandDefn('gmw', gmw_tile, 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('hh', sar_img, 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('vld', sar_vld_img, 1))
        exp = '(vld==1)&&(gmw==1)&&(hh<{})?1:0'.format(threshold+step)
        rsgislib.imagecalc.bandMath(out_tmp_img, exp, 'KEA', rsgislib.TYPE_8UINT, band_defns)
        imgs.append(out_tmp_img)
        i += 1

    # Remove intervals
    for step in threshold_steps:
        out_tmp_img = os.path.join(tmp_dir, "{}_img_{}.kea".format(basename, i))
        band_defns = []
        band_defns.append(rsgislib.imagecalc.BandDefn('gmw', gmw_tile, 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('hh', sar_img, 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('vld', sar_vld_img, 1))
        exp = '(vld==1)&&(gmw==1)&&(hh<{})?1:0'.format(threshold-step)
        rsgislib.imagecalc.bandMath(out_tmp_img, exp, 'KEA', rsgislib.TYPE_8UINT, band_defns)
        imgs.append(out_tmp_img)
        i += 1

    rsgislib.imagecalc.calcMultiImgBandStats(imgs, out_uncertain_img, rsgislib.SUMTYPE_SUM, 'KEA', rsgislib.TYPE_8UINT, 0, False)
    rsgislib.imageutils.popImageStats(out_uncertain_img, usenodataval=True, nodataval=0, calcpyramids=True)

def create_1996_nmng_msk(chng_rgn_tile, sar_img, sar_vld_img, threshold, out_img, out_uncertain_img, tmp_dir, thres_var=2, n_steps=10):
    step_intvl = thres_var / int(n_steps / 2)
    threshold_steps = numpy.arange(1, int(n_steps / 2)) * step_intvl
    rsgis_utils = rsgislib.RSGISPyUtils()
    basename = rsgis_utils.get_file_basename(out_img)

    imgs = list()

    # Using threshold
    band_defns = []
    band_defns.append(rsgislib.imagecalc.BandDefn('chgmsk', chng_rgn_tile, 1))
    band_defns.append(rsgislib.imagecalc.BandDefn('hh', sar_img, 1))
    band_defns.append(rsgislib.imagecalc.BandDefn('vld', sar_vld_img, 1))
    exp = '(vld==1)&&(chgmsk==1)&&(hh>{})?1:0'.format(threshold)
    rsgislib.imagecalc.bandMath(out_img, exp, 'KEA', rsgislib.TYPE_8UINT, band_defns)
    rsgislib.rastergis.populateStats(out_img, True, True, True)
    imgs.append(out_img)

    # Add intervals
    i = 1
    for step in threshold_steps:
        out_tmp_img = os.path.join(tmp_dir, "{}_img_{}.kea".format(basename, i))
        band_defns = []
        band_defns.append(rsgislib.imagecalc.BandDefn('chgmsk', chng_rgn_tile, 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('hh', sar_img, 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('vld', sar_vld_img, 1))
        exp = '(vld==1)&&(chgmsk==1)&&(hh>{})?1:0'.format(threshold + step)
        rsgislib.imagecalc.bandMath(out_tmp_img, exp, 'KEA', rsgislib.TYPE_8UINT, band_defns)
        imgs.append(out_tmp_img)
        i += 1

    # Remove intervals
    for step in threshold_steps:
        out_tmp_img = os.path.join(tmp_dir, "{}_img_{}.kea".format(basename, i))
        band_defns = []
        band_defns.append(rsgislib.imagecalc.BandDefn('chgmsk', chng_rgn_tile, 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('hh', sar_img, 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('vld', sar_vld_img, 1))
        exp = '(vld==1)&&(chgmsk==1)&&(hh>{})?1:0'.format(threshold - step)
        rsgislib.imagecalc.bandMath(out_tmp_img, exp, 'KEA', rsgislib.TYPE_8UINT, band_defns)
        imgs.append(out_tmp_img)
        i += 1

    rsgislib.imagecalc.calcMultiImgBandStats(imgs, out_uncertain_img, rsgislib.SUMTYPE_SUM, 'KEA', rsgislib.TYPE_8UINT, 0, False)
    rsgislib.imageutils.popImageStats(out_uncertain_img, usenodataval=True, nodataval=0, calcpyramids=True)




def create_alos_mng_msk(gmw_tile, sar_img, sar_vld_img, threshold, out_img, out_uncertain_img, tmp_dir, thres_var=2, n_steps=10):
    step_intvl = thres_var / int(n_steps / 2)
    threshold_steps = numpy.arange(1, int(n_steps / 2)) * step_intvl
    rsgis_utils = rsgislib.RSGISPyUtils()
    basename = rsgis_utils.get_file_basename(out_img)

    imgs = list()

    # Using threshold
    band_defns = []
    band_defns.append(rsgislib.imagecalc.BandDefn('gmw', gmw_tile, 1))
    band_defns.append(rsgislib.imagecalc.BandDefn('hv', sar_img, 2))
    band_defns.append(rsgislib.imagecalc.BandDefn('vld', sar_vld_img, 1))
    exp = '(vld==1)&&(gmw==1)&&(hv<{})?1:0'.format(threshold)
    rsgislib.imagecalc.bandMath(out_img, exp, 'KEA', rsgislib.TYPE_8UINT, band_defns)
    rsgislib.rastergis.populateStats(out_img, True, True, True)
    imgs.append(out_img)

    # Add intervals
    i = 1
    for step in threshold_steps:
        out_tmp_img = os.path.join(tmp_dir, "{}_img_{}.kea".format(basename, i))
        band_defns = []
        band_defns.append(rsgislib.imagecalc.BandDefn('gmw', gmw_tile, 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('hv', sar_img, 2))
        band_defns.append(rsgislib.imagecalc.BandDefn('vld', sar_vld_img, 1))
        exp = '(vld==1)&&(gmw==1)&&(hv<{})?1:0'.format(threshold + step)
        rsgislib.imagecalc.bandMath(out_tmp_img, exp, 'KEA', rsgislib.TYPE_8UINT, band_defns)
        imgs.append(out_tmp_img)
        i += 1

    # Remove intervals
    for step in threshold_steps:
        out_tmp_img = os.path.join(tmp_dir, "{}_img_{}.kea".format(basename, i))
        band_defns = []
        band_defns.append(rsgislib.imagecalc.BandDefn('gmw', gmw_tile, 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('hv', sar_img, 2))
        band_defns.append(rsgislib.imagecalc.BandDefn('vld', sar_vld_img, 1))
        exp = '(vld==1)&&(gmw==1)&&(hv<{})?1:0'.format(threshold - step)
        rsgislib.imagecalc.bandMath(out_tmp_img, exp, 'KEA', rsgislib.TYPE_8UINT, band_defns)
        imgs.append(out_tmp_img)
        i += 1

    rsgislib.imagecalc.calcMultiImgBandStats(imgs, out_uncertain_img, rsgislib.SUMTYPE_SUM, 'KEA', rsgislib.TYPE_8UINT, 0, False)
    rsgislib.imageutils.popImageStats(out_uncertain_img, usenodataval=True, nodataval=0, calcpyramids=True)



def create_alos_nmng_msk(chng_rgn_tile, sar_img, sar_vld_img, threshold, out_img, out_uncertain_img, tmp_dir, thres_var=2, n_steps=10):
    step_intvl = thres_var / int(n_steps / 2)
    threshold_steps = numpy.arange(1, int(n_steps / 2)) * step_intvl
    rsgis_utils = rsgislib.RSGISPyUtils()
    basename = rsgis_utils.get_file_basename(out_img)

    imgs = list()

    # Using threshold
    band_defns = []
    band_defns.append(rsgislib.imagecalc.BandDefn('chgmsk', chng_rgn_tile, 1))
    band_defns.append(rsgislib.imagecalc.BandDefn('hv', sar_img, 2))
    band_defns.append(rsgislib.imagecalc.BandDefn('vld', sar_vld_img, 1))
    exp = '(vld==1)&&(chgmsk==1)&&(hv>{})?1:0'.format(threshold)
    rsgislib.imagecalc.bandMath(out_img, exp, 'KEA', rsgislib.TYPE_8UINT, band_defns)
    rsgislib.rastergis.populateStats(out_img, True, True, True)
    imgs.append(out_img)

    # Add intervals
    i = 1
    for step in threshold_steps:
        out_tmp_img = os.path.join(tmp_dir, "{}_img_{}.kea".format(basename, i))
        band_defns = []
        band_defns.append(rsgislib.imagecalc.BandDefn('chgmsk', chng_rgn_tile, 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('hv', sar_img, 2))
        band_defns.append(rsgislib.imagecalc.BandDefn('vld', sar_vld_img, 1))
        exp = '(vld==1)&&(chgmsk==1)&&(hv>{})?1:0'.format(threshold + step)
        rsgislib.imagecalc.bandMath(out_tmp_img, exp, 'KEA', rsgislib.TYPE_8UINT, band_defns)
        imgs.append(out_tmp_img)
        i += 1

    # Remove intervals
    for step in threshold_steps:
        out_tmp_img = os.path.join(tmp_dir, "{}_img_{}.kea".format(basename, i))
        band_defns = []
        band_defns.append(rsgislib.imagecalc.BandDefn('chgmsk', chng_rgn_tile, 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('hv', sar_img, 2))
        band_defns.append(rsgislib.imagecalc.BandDefn('vld', sar_vld_img, 1))
        exp = '(vld==1)&&(chgmsk==1)&&(hv>{})?1:0'.format(threshold - step)
        rsgislib.imagecalc.bandMath(out_tmp_img, exp, 'KEA', rsgislib.TYPE_8UINT, band_defns)
        imgs.append(out_tmp_img)
        i += 1

    rsgislib.imagecalc.calcMultiImgBandStats(imgs, out_uncertain_img, rsgislib.SUMTYPE_SUM, 'KEA', rsgislib.TYPE_8UINT, 0, False)
    rsgislib.imageutils.popImageStats(out_uncertain_img, usenodataval=True, nodataval=0, calcpyramids=True)

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
                mng_hh_thres = thres_lut['yen_mng_hh']
                if thres_lut['his_mng_hh'] > thres_lut['yen_mng_hh']:
                    mng_hh_thres = thres_lut['his_mng_hh']
                create_1996_mng_msk(self.params['gmw_tile'], self.params['sar_img'], self.params['sar_vld_img'], mng_hh_thres, self.params['out_mng_chng'], self.params['out_mng_chng_uncertain'], self.params['tmp_dir'])

                nmng_hh_thres = thres_lut['yen_nmng_hh']
                if thres_lut['his_nmng_hh'] < thres_lut['yen_nmng_hh']:
                    nmng_hh_thres = thres_lut['his_nmng_hh']
                create_1996_nmng_msk(self.params['potent_chng_msk_img'], self.params['sar_img'], self.params['sar_vld_img'], nmng_hh_thres, self.params['out_nmng_chng'], self.params['out_nmng_chng_uncertain'], self.params['tmp_dir'])

            else:
                mng_hv_thres = thres_lut['yen_mng_hv']
                if thres_lut['his_mng_hv'] > thres_lut['yen_mng_hv']:
                    mng_hv_thres = thres_lut['his_mng_hv']
                create_alos_mng_msk(self.params['gmw_tile'], self.params['sar_img'], self.params['sar_vld_img'], mng_hv_thres, self.params['out_mng_chng'], self.params['out_mng_chng_uncertain'], self.params['tmp_dir'])

                nmng_hv_thres = thres_lut['yen_nmng_hv']
                if thres_lut['his_nmng_hv'] < thres_lut['yen_nmng_hv']:
                    nmng_hv_thres = thres_lut['his_nmng_hv']
                create_alos_nmng_msk(self.params['potent_chng_msk_img'], self.params['sar_img'], self.params['sar_vld_img'], nmng_hv_thres, self.params['out_nmng_chng'], self.params['out_nmng_chng_uncertain'], self.params['tmp_dir'])
        else:
            rsgislib.imagecalc.imageMath(self.params['gmw_tile'], self.params['out_mng_chng'], '0', 'KEA', rsgislib.TYPE_8UINT)
            rsgislib.imagecalc.imageMath(self.params['gmw_tile'], self.params['out_mng_chng_uncertain'], '0', 'KEA', rsgislib.TYPE_8UINT)
            rsgislib.imagecalc.imageMath(self.params['gmw_tile'], self.params['out_nmng_chng'], '0', 'KEA', rsgislib.TYPE_8UINT)
            rsgislib.imagecalc.imageMath(self.params['gmw_tile'], self.params['out_nmng_chng_uncertain'], '0', 'KEA', rsgislib.TYPE_8UINT)

        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])


    def required_fields(self, **kwargs):
        return ["tile", "gmw_tile", "sar_year", "potent_chng_msk_img", "sar_img", "sar_vld_img", "gmw_proj_thres_lmit_file", "gmw_proj_thres_file", "out_mng_chng", "out_nmng_chng", "out_mng_chng_uncertain", "out_nmng_chng_uncertain"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_mng_chng']] = 'gdal_image'
        files_dict[self.params['out_nmng_chng']] = 'gdal_image'
        files_dict[self.params['out_mng_chng_uncertain']] = 'gdal_image'
        files_dict[self.params['out_nmng_chng_uncertain']] = 'gdal_image'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_mng_chng']):
            os.remove(self.params['out_mng_chng'])

        if os.path.exists(self.params['out_nmng_chng']):
            os.remove(self.params['out_nmng_chng'])

        if os.path.exists(self.params['out_mng_chng_uncertain']):
            os.remove(self.params['out_mng_chng_uncertain'])

        if os.path.exists(self.params['out_nmng_chng_uncertain']):
            os.remove(self.params['out_nmng_chng_uncertain'])

        # Reset the tmp dir
        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])
        os.mkdir(self.params['tmp_dir'])

if __name__ == "__main__":
    CreateImageTile().std_run()


