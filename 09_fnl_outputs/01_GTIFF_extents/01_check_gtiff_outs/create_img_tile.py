from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import osgeo.gdal as gdal
import rsgislib
import rsgislib.imagecalc
import numpy

logger = logging.getLogger(__name__)


def write_dict_to_json(data_dict: dict, out_file: str):
    """
    Write some data to a JSON file. The data would commonly be structured as a dict
    but could also be a list.

    :param data_dict: The dict (or list) to be written to the output JSON file.
    :param out_file: The file path to the output file.

    """
    import json

    with open(out_file, "w") as fp:
        json.dump(
            data_dict,
            fp,
            sort_keys=True,
            indent=4,
            separators=(",", ": "),
            ensure_ascii=False,
        )


class CreateImageTile(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_img_tile.py', descript=None)

    def do_processing(self, **kwargs):

        if os.path.exists(self.params['tif_img']):
            kea_pxl_count = rsgislib.imagecalc.countPxlsOfVal(self.params['gmw_tile'], vals=[1])
            tif_pxl_count = rsgislib.imagecalc.countPxlsOfVal(self.params['tif_img'], vals=[1])

            if kea_pxl_count[0] != tif_pxl_count[0]:
                os.remove(self.params['tif_img'])
            else:
                pxl_vals = dict()
                pxl_vals['kea'] = int(kea_pxl_count[0])
                pxl_vals['tif'] = int(tif_pxl_count[0])
                write_dict_to_json(pxl_vals, self.params['out_file'])


    def required_fields(self, **kwargs):
        return ["gmw_tile", "tif_img", "out_file"]


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


