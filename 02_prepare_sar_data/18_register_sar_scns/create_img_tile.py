from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib
import rsgislib.tools.filetools
import rsgislib.tools.utils
import rsgislib.imageutils
import rsgislib.imageregistration
import rsgislib.imagecalc

logger = logging.getLogger(__name__)


def msk_imgs(in_ref_img, in_flt_img, tmp_dir, sar_year):
    ref_img_base = rsgislib.tools.filetools.get_file_basename(in_ref_img)
    flt_img_base = rsgislib.tools.filetools.get_file_basename(in_flt_img)

    out_ref_img = os.path.join(tmp_dir, "{}_mskd.kea".format(ref_img_base))
    out_flt_img = os.path.join(tmp_dir, "{}_mskd.kea".format(flt_img_base))

    ref_msk_img = os.path.join(tmp_dir, "{}_msk.kea".format(ref_img_base))
    flt_msk_img = os.path.join(tmp_dir, "{}_msk.kea".format(flt_img_base))

    ref_msk_dist_img = os.path.join(tmp_dir, "{}_msk_dist.kea".format(ref_img_base))
    flt_msk_dist_img = os.path.join(tmp_dir, "{}_msk_dist.kea".format(flt_img_base))

    ref_msk_buf_img = os.path.join(tmp_dir, "{}_msk_buf.kea".format(ref_img_base))
    flt_msk_buf_img = os.path.join(tmp_dir, "{}_msk_buf.kea".format(flt_img_base))

    msk_img = os.path.join(tmp_dir, "{}_{}_msk.kea".format(ref_img_base, flt_img_base))

    if sar_year == '1996':
        rsgislib.imagecalc.imageBandMath(in_ref_img, ref_msk_img, '(b1>-1500)&&(b1<500)?1:0', 'KEA', rsgislib.TYPE_8UINT)
        rsgislib.imagecalc.imageBandMath(in_flt_img, flt_msk_img, '(b1>-1500)&&(b1<500)?1:0', 'KEA', rsgislib.TYPE_8UINT)
    else:
        rsgislib.imagecalc.imageBandMath(in_ref_img, ref_msk_img, '(b2>-2000)&&(b2<500)?1:0', 'KEA', rsgislib.TYPE_8UINT)
        rsgislib.imagecalc.imageBandMath(in_flt_img, flt_msk_img, '(b2>-2000)&&(b2<500)?1:0', 'KEA', rsgislib.TYPE_8UINT)

    n_ref_pxls = rsgislib.imagecalc.countPxlsOfVal(ref_msk_img, [0,1])
    n_flt_pxls = rsgislib.imagecalc.countPxlsOfVal(flt_msk_img, [0,1])

    tot_ref_pxls = n_ref_pxls[0] + n_ref_pxls[1]
    tot_flt_pxls = n_flt_pxls[0] + n_flt_pxls[1]

    prop_ref_pxls = n_ref_pxls[1] / tot_ref_pxls
    prop_flt_pxls = n_flt_pxls[1] / tot_flt_pxls

    print("prop_ref_pxls: {}".format(prop_ref_pxls))
    print("prop_flt_pxls: {}".format(prop_flt_pxls))

    if (prop_ref_pxls > 0.0001) and (prop_flt_pxls > 0.0001):
        rsgislib.imagecalc.calcDist2ImgVals(ref_msk_img, ref_msk_dist_img, 1, 1, 'KEA', 100, 32767, False)
        rsgislib.imagecalc.calcDist2ImgVals(flt_msk_img, flt_msk_dist_img, 1, 1, 'KEA', 100, 32767, False)

        rsgislib.imagecalc.imageBandMath(ref_msk_dist_img, ref_msk_buf_img, 'b1<50?1:0', 'KEA', rsgislib.TYPE_8UINT)
        rsgislib.imagecalc.imageBandMath(flt_msk_dist_img, flt_msk_buf_img, 'b1<50?1:0', 'KEA', rsgislib.TYPE_8UINT)

        band_defs = []
        band_defs.append(rsgislib.imagecalc.BandDefn('ref', ref_msk_buf_img, 1))
        band_defs.append(rsgislib.imagecalc.BandDefn('flt', flt_msk_buf_img, 1))
        rsgislib.imagecalc.bandMath(msk_img, '(ref==1)||(flt==1)?1:0', 'KEA', rsgislib.TYPE_8UINT, band_defs)

        rsgislib.imageutils.includeImagesIndImgIntersect(flt_msk_buf_img, [msk_img])

        rsgislib.imageutils.maskImage(in_ref_img, msk_img, out_ref_img, 'KEA', rsgislib.TYPE_16INT, 32767, 0)
        rsgislib.imageutils.maskImage(in_flt_img, flt_msk_buf_img, out_flt_img, 'KEA', rsgislib.TYPE_16INT, 32767, 0)

        rsgislib.imageutils.popImageStats(out_ref_img, True, 32767, True)
        rsgislib.imageutils.popImageStats(out_flt_img, True, 32767, True)
    else:
        out_ref_img = None
        out_flt_img = None

    return out_ref_img, out_flt_img


class CreateImageTile(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_img_tile.py', descript=None)

    def do_processing(self, **kwargs):
        if not os.path.exists(self.params['tmpdir']):
            os.mkdir(self.params['tmpdir'])

        in_ref_img_mskd, in_flt_img_mskd = msk_imgs(self.params['sar_ref_img'], self.params['sar_flt_buf_img'], self.params['tmpdir'], self.params['sar_year'])

        if (in_ref_img_mskd is not None) and (in_flt_img_mskd is not None):
            if self.params['sar_year'] == '1996':
                offsets = rsgislib.imageregistration.findImageOffset(in_ref_img_mskd, in_flt_img_mskd, [1], [1], rsgislib.imageregistration.METRIC_CORELATION, 5, 5, 10)
            else:
                offsets = rsgislib.imageregistration.findImageOffset(in_ref_img_mskd, in_flt_img_mskd, [2], [2], rsgislib.imageregistration.METRIC_CORELATION, 5, 5, 10)

            img_res_x, img_res_y = rsgislib.imageutils.getImageRes(self.params['sar_flt_buf_img'], abs_vals=True)

            sp_off_x = offsets[0] * img_res_x
            sp_off_y = offsets[1] * img_res_y

            rsgislib.imageregistration.applyOffset2Image(self.params['sar_flt_buf_img'], self.params['out_flt_buf_img'], 'KEA', rsgislib.TYPE_16INT, sp_off_x, sp_off_y)

            rsgislib.imageutils.resampleImage2Match(self.params['sar_ref_img'], self.params['out_flt_buf_img'], self.params['out_rsmpld_img'], 'KEA', 'cubic', rsgislib.TYPE_16INT, 32767)
            rsgislib.imageutils.popImageStats(self.params['out_rsmpld_img'], True, 32767, True)
        else:
            offsets = [0, 0]
            sp_off_x = 0.0
            sp_off_y = 0.0

        out_offs = dict()
        out_offs['tile'] = self.params['tile']
        out_offs['x_pxl_off'] = float(offsets[0])
        out_offs['y_pxl_off'] = float(offsets[1])
        out_offs['x_spl_off'] = float(sp_off_x)
        out_offs['y_spl_off'] = float(sp_off_y)
        rsgislib.tools.utils.writeDict2JSON(out_offs, self.params['out_off_json'])

        if os.path.exists(self.params['tmpdir']):
            shutil.rmtree(self.params['tmpdir'])


    def required_fields(self, **kwargs):
        return ["tile", "sar_ref_img", "sar_flt_buf_img", "out_flt_buf_img", "out_rsmpld_img", "out_off_json", "sar_year", "tmpdir"]


    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_flt_buf_img']] = 'gdal_image'
        files_dict[self.params['out_rsmpld_img']] = 'gdal_image'
        files_dict[self.params['out_off_json']] = 'file'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_flt_buf_img']):
            os.remove(self.params['out_flt_buf_img'])

        if os.path.exists(self.params['out_rsmpld_img']):
            os.remove(self.params['out_rsmpld_img'])

        if os.path.exists(self.params['out_off_json']):
            os.remove(self.params['out_off_json'])

        if os.path.exists(self.params['tmpdir']):
            shutil.rmtree(self.params['tmpdir'])
            os.mkdir(self.params['tmpdir'])

if __name__ == "__main__":
    CreateImageTile().std_run()


