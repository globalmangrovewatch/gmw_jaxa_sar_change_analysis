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

def create_1996_mng_msk(gmw_tile, sar_img, sar_vld_img, threshold, out_img, out_uncertain_img, tmp_dir, thres_var=200, n_steps=10):

    step_intvl = thres_var / int(n_steps/2)
    threshold_steps = numpy.arange(1, int(n_steps/2)+1) * step_intvl
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

def create_1996_nmng_msk(chng_rgn_tile, sar_img, sar_vld_img, threshold, out_img, out_uncertain_img, tmp_dir, thres_var=200, n_steps=10):
    step_intvl = thres_var / int(n_steps / 2)
    threshold_steps = numpy.arange(1, int(n_steps / 2)+1) * step_intvl
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




def create_alos_mng_msk(gmw_tile, sar_img, sar_vld_img, threshold, out_img, out_uncertain_img, tmp_dir, thres_var=200, n_steps=10):
    step_intvl = thres_var / int(n_steps / 2)
    threshold_steps = numpy.arange(1, int(n_steps / 2)+1) * step_intvl
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



def create_alos_nmng_msk(chng_rgn_tile, sar_img, sar_vld_img, threshold, out_img, out_uncertain_img, tmp_dir, thres_var=200, n_steps=10):
    step_intvl = thres_var / int(n_steps / 2)
    threshold_steps = numpy.arange(1, int(n_steps / 2)+1) * step_intvl
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

        rsgis_utils = rsgislib.RSGISPyUtils()

        out_stats = dict()
        out_stats['gmw_pxls'] = 0
        out_stats['pochng_pxls'] = 0
        out_stats['gmw_pxls_gt'] = list()
        out_stats['pochng_pxls_gt'] = list()
        out_stats['thresholds_gt'] = list()
        out_stats['gmw_pxls_lt'] = list()
        out_stats['pochng_pxls_lt'] = list()
        out_stats['thresholds_lt'] = list()


        if self.params['band'] == 'HH':
            sar_band = 1
        elif self.params['band'] == 'HV':
            sar_band = 2
        else:
            raise Exception("Did not recognise the bands: {}".format(self.params['band']))

        if self.params['sar_img'] is not None:
            basename = rsgis_utils.get_file_basename(self.params['sar_img'])

            out_tmp_gmw_img = os.path.join(self.params['tmp_dir'], "{}_gmw_pxls.kea".format(basename))
            band_defns = []
            band_defns.append(rsgislib.imagecalc.BandDefn('gmw', self.params['gmw_tile'], 1))
            band_defns.append(rsgislib.imagecalc.BandDefn('vld', self.params['sar_vld_img'], 1))
            rsgislib.imagecalc.bandMath(out_tmp_gmw_img, '(vld==1)&&(gmw==1)?1:0', 'KEA', rsgislib.TYPE_8UINT, band_defns)
            out_stats['gmw_pxls'] = int(rsgislib.imagecalc.countPxlsOfVal(out_tmp_gmw_img, vals=[1])[0])

            out_tmp_pochng_img = os.path.join(self.params['tmp_dir'], "{}_pochng_pxls.kea".format(basename))
            band_defns = []
            band_defns.append(rsgislib.imagecalc.BandDefn('pochng', self.params['potent_chng_msk_img'], 1))
            band_defns.append(rsgislib.imagecalc.BandDefn('vld', self.params['sar_vld_img'], 1))
            rsgislib.imagecalc.bandMath(out_tmp_pochng_img, '(vld==1)&&(pochng==1)?1:0', 'KEA', rsgislib.TYPE_8UINT, band_defns)
            out_stats['pochng_pxls'] = int(rsgislib.imagecalc.countPxlsOfVal(out_tmp_pochng_img, vals=[1])[0])

            if (out_stats['gmw_pxls'] > 0) or (out_stats['pochng_pxls'] > 0):
                thresholds = numpy.arange(-3500, -450, 50)
                for threshold in thresholds:
                    # Greater than threshold
                    out_stats['thresholds_gt'].append(int(threshold))
                    out_tmp_img = os.path.join(self.params['tmp_dir'], "{}_gt_thres_{}.kea".format(basename, abs(threshold)))
                    band_defns = []
                    band_defns.append(rsgislib.imagecalc.BandDefn('sar', self.params['sar_img'], sar_band))
                    band_defns.append(rsgislib.imagecalc.BandDefn('vld', self.params['sar_vld_img'], 1))
                    exp = '(vld==1)&&(sar>{})?1:0'.format(threshold)
                    rsgislib.imagecalc.bandMath(out_tmp_img, exp, 'KEA', rsgislib.TYPE_8UINT, band_defns)

                    out_tmp_gmw_img = os.path.join(self.params['tmp_dir'], "{}_gt_thres_{}_GMW.kea".format(basename, abs(threshold)))
                    band_defns = []
                    band_defns.append(rsgislib.imagecalc.BandDefn('gmw', self.params['gmw_tile'], 1))
                    band_defns.append(rsgislib.imagecalc.BandDefn('msk', out_tmp_img, 1))
                    rsgislib.imagecalc.bandMath(out_tmp_gmw_img, '(msk==1)&&(gmw==1)?1:0', 'KEA', rsgislib.TYPE_8UINT, band_defns)
                    out_stats['gmw_pxls_gt'].append(int(rsgislib.imagecalc.countPxlsOfVal(out_tmp_gmw_img, vals=[1])[0]))

                    out_tmp_pochng_img = os.path.join(self.params['tmp_dir'], "{}_gt_thres_{}_pochng.kea".format(basename, abs(threshold)))
                    band_defns = []
                    band_defns.append(rsgislib.imagecalc.BandDefn('pochng', self.params['potent_chng_msk_img'], 1))
                    band_defns.append(rsgislib.imagecalc.BandDefn('msk', out_tmp_img, 1))
                    rsgislib.imagecalc.bandMath(out_tmp_pochng_img, '(msk==1)&&(pochng==1)?1:0', 'KEA', rsgislib.TYPE_8UINT, band_defns)
                    out_stats['pochng_pxls_gt'].append(int(rsgislib.imagecalc.countPxlsOfVal(out_tmp_pochng_img, vals=[1])[0]))

                    # Less than threshold
                    out_stats['thresholds_lt'].append(int(threshold))
                    out_tmp_img = os.path.join(self.params['tmp_dir'], "{}_lt_thres_{}.kea".format(basename, abs(threshold)))
                    band_defns = []
                    band_defns.append(rsgislib.imagecalc.BandDefn('sar', self.params['sar_img'], sar_band))
                    band_defns.append(rsgislib.imagecalc.BandDefn('vld', self.params['sar_vld_img'], 1))
                    exp = '(vld==1)&&(sar<{})?1:0'.format(threshold)
                    rsgislib.imagecalc.bandMath(out_tmp_img, exp, 'KEA', rsgislib.TYPE_8UINT, band_defns)

                    out_tmp_gmw_img = os.path.join(self.params['tmp_dir'], "{}_lt_thres_{}_GMW.kea".format(basename, abs(threshold)))
                    band_defns = []
                    band_defns.append(rsgislib.imagecalc.BandDefn('gmw', self.params['gmw_tile'], 1))
                    band_defns.append(rsgislib.imagecalc.BandDefn('msk', out_tmp_img, 1))
                    rsgislib.imagecalc.bandMath(out_tmp_gmw_img, '(msk==1)&&(gmw==1)?1:0', 'KEA', rsgislib.TYPE_8UINT, band_defns)
                    out_stats['gmw_pxls_lt'].append(int(rsgislib.imagecalc.countPxlsOfVal(out_tmp_gmw_img, vals=[1])[0]))

                    out_tmp_pochng_img = os.path.join(self.params['tmp_dir'], "{}_lt_thres_{}_pochng.kea".format(basename, abs(threshold)))
                    band_defns = []
                    band_defns.append(rsgislib.imagecalc.BandDefn('pochng', self.params['potent_chng_msk_img'], 1))
                    band_defns.append(rsgislib.imagecalc.BandDefn('msk', out_tmp_img, 1))
                    rsgislib.imagecalc.bandMath(out_tmp_pochng_img, '(msk==1)&&(pochng==1)?1:0', 'KEA', rsgislib.TYPE_8UINT, band_defns)
                    out_stats['pochng_pxls_lt'].append(int(rsgislib.imagecalc.countPxlsOfVal(out_tmp_pochng_img, vals=[1])[0]))

        pprint.pprint(out_stats)
        rsgis_utils.writeDict2JSON(out_stats, self.params['out_file'])

        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])


    def required_fields(self, **kwargs):
        return ["tile", "gmw_tile", "potent_chng_msk_img", "band", "sar_img", "sar_vld_img", "out_file", "tmp_dir"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_file']] = 'file'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_file']):
            os.remove(self.params['out_file'])

        # Reset the tmp dir
        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])
        os.mkdir(self.params['tmp_dir'])

if __name__ == "__main__":
    CreateImageTile().std_run()


