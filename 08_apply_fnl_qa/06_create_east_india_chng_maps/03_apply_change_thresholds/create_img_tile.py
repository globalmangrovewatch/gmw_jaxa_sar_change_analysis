from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib
import rsgislib.rastergis
import rsgislib.imagecalc
import rsgislib.imageutils

logger = logging.getLogger(__name__)

class CreateImageTile(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_img_tile.py', descript=None)

    def do_processing(self, **kwargs):
        if not os.path.exists(self.params['tmp_dir']):
            os.mkdir(self.params['tmp_dir'])

        if self.params['year'] == '1996':
            nmng_thres = -1215.430489
            mng_thres = -1511.171434
        elif self.params['year'] == '2007':
            nmng_thres = -2427.589548
            mng_thres = -2158.887011
        elif self.params['year'] == '2008':
            nmng_thres = -2434.407934
            mng_thres = -2173.061028
        elif self.params['year'] == '2009':
            nmng_thres = -2398.244403
            mng_thres = -2171.08455
        elif self.params['year'] == '2010':
            nmng_thres = -2374.124697
            mng_thres = -2122.784418
        elif self.params['year'] == '2015':
            nmng_thres = -2502.865236
            mng_thres = -2267.757672
        elif self.params['year'] == '2016':
            nmng_thres = -2508.187956
            mng_thres = -2267.300256
        elif self.params['year'] == '2017':
            nmng_thres = -2404.203915
            mng_thres = -2183.935853
        elif self.params['year'] == '2018':
            nmng_thres = -2445.103804
            mng_thres = -2161.883534
        elif self.params['year'] == '2019':
            nmng_thres = -2441.94874
            mng_thres = -2225.188312
        elif self.params['year'] == '2020':
            nmng_thres = -2489.658711
            mng_thres = -2242.837166
        else:
            raise Exception("Year error no thresholds.")

        sar_vld_img = os.path.join(self.params['tmp_dir'], "{}_sar_vld_msk.kea".format(self.params['tile']))
        rsgislib.imageutils.genValidMask(self.params['sar_img'], sar_vld_img, "KEA", nodata=32767)

        if self.params['year'] == '1996':
            band_defns = []
            band_defns.append(rsgislib.imagecalc.BandDefn('gmw', self.params['gmw_tile'], 1))
            band_defns.append(rsgislib.imagecalc.BandDefn('hh', self.params['sar_img'], 1))
            band_defns.append(rsgislib.imagecalc.BandDefn('pchng', self.params['pchng_img'], 1))
            band_defns.append(rsgislib.imagecalc.BandDefn('vld', sar_vld_img, 1))
            exp = '(vld==1)&&(pchng==1)&&(gmw==1)&&(hh<{})?0:(vld==1)&&(pchng==1)&&(gmw==0)&&(hh>{})?1:gmw'.format(mng_thres, nmng_thres)
            rsgislib.imagecalc.bandMath(self.params['out_img'], exp, 'KEA', rsgislib.TYPE_8UINT, band_defns)
        else:
            band_defns = []
            band_defns.append(rsgislib.imagecalc.BandDefn('gmw', self.params['gmw_tile'], 1))
            band_defns.append(rsgislib.imagecalc.BandDefn('hv', self.params['sar_img'], 2))
            band_defns.append(rsgislib.imagecalc.BandDefn('pchng', self.params['pchng_img'], 1))
            band_defns.append(rsgislib.imagecalc.BandDefn('vld', sar_vld_img, 1))
            exp = '(vld==1)&&(pchng==1)&&(gmw==1)&&(hv<{})?0:(vld==1)&&(pchng==1)&&(gmw==0)&&(hv>{})?1:gmw'.format(mng_thres, nmng_thres)
            rsgislib.imagecalc.bandMath(self.params['out_img'], exp, 'KEA', rsgislib.TYPE_8UINT, band_defns)
        rsgislib.rastergis.populateStats(self.params['out_img'], True, True, True)

        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])


    def required_fields(self, **kwargs):
        return ["tile", "gmw_tile", "sar_img", "pchng_img", "year", "out_img", "tmp_dir"]


    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_img']] = 'gdal_image'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_img']):
            os.remove(self.params['out_img'])

        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])

if __name__ == "__main__":
    CreateImageTile().std_run()


