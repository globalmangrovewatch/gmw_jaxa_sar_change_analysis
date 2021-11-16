from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import pathlib
import rsgislib.vectorutils
import rsgislib.imagecalc

import osgeo.gdal as gdal
import osgeo.osr as osr
import osgeo.ogr as ogr

logger = logging.getLogger(__name__)


def write_vec_column(
    out_vec_file: str,
    out_vec_lyr: str,
    att_column: str,
    att_col_datatype: int,
    att_col_data: list,
):
    """
    A function which will write a column to a vector file

    :param out_vec_file: The file / path to the vector data 'file'.
    :param out_vec_lyr: The layer to which the data is to be added.
    :param att_column: Name of the output column
    :param att_col_datatype: ogr data type for the output column
                            (e.g., ogr.OFTString, ogr.OFTInteger, ogr.OFTReal)
    :param att_col_data: A list of the same length as the number of features
                        in vector file.

    """
    gdal.UseExceptions()

    ds = gdal.OpenEx(out_vec_file, gdal.OF_UPDATE)
    if ds is None:
        raise Exception("Could not open '{}'".format(out_vec_file))

    lyr = ds.GetLayerByName(out_vec_lyr)
    if lyr is None:
        raise Exception("Could not find layer '{}'".format(out_vec_lyr))

    numFeats = lyr.GetFeatureCount()
    if not len(att_col_data) == numFeats:
        print("Number of Features: {}".format(numFeats))
        print("Length of Data: {}".format(len(att_col_data)))
        raise Exception(
            "The number of features and size of the input data is not equal."
        )

    colExists = False
    lyrDefn = lyr.GetLayerDefn()
    for i in range(lyrDefn.GetFieldCount()):
        if lyrDefn.GetFieldDefn(i).GetName().lower() == att_column.lower():
            colExists = True
            break

    if not colExists:
        field_defn = ogr.FieldDefn(att_column, att_col_datatype)
        if lyr.CreateField(field_defn) != 0:
            raise Exception(
                "Creating '{}' field failed; be careful with case, "
                "some drivers are case insensitive but column might "
                "not be found.".format(att_column)
            )

    lyr.ResetReading()
    # WORK AROUND AS SQLITE GETS STUCK IN LOOP ON FIRST FEATURE WHEN USE SETFEATURE.
    fids = []
    for feat in lyr:
        fids.append(feat.GetFID())

    openTransaction = False
    lyr.ResetReading()
    i = 0
    try:
        # WORK AROUND AS SQLITE GETS STUCK IN LOOP ON FIRST FEATURE WHEN USE SETFEATURE.
        for fid in fids:
            if not openTransaction:
                lyr.StartTransaction()
                openTransaction = True
            feat = lyr.GetFeature(fid)
            if feat is not None:
                feat.SetField(att_column, att_col_data[i])
                lyr.SetFeature(feat)
            if ((i % 20000) == 0) and openTransaction:
                lyr.CommitTransaction()
                openTransaction = False
            i = i + 1
        if openTransaction:
            lyr.CommitTransaction()
            openTransaction = False
        lyr.SyncToDisk()
        ds = None
    except Exception as e:
        if i < numFeats:
            print(
                "Data type of the value being "
                "written is '{}'".format(type(att_col_data[i]))
            )
        raise e


def read_vec_column(vec_file: str, vec_lyr: str, att_column: str):
    """
    A function which will reads a column from a vector file

    :param vec_file: The file / path to the vector data 'file'.
    :param vec_lyr: The layer to which the data is to be read from.
    :param att_column: Name of the input column

    """
    gdal.UseExceptions()

    ds = gdal.OpenEx(vec_file, gdal.OF_VECTOR)
    if ds is None:
        raise Exception("Could not open '{}'".format(vec_file))

    lyr = ds.GetLayerByName(vec_lyr)
    if lyr is None:
        raise Exception("Could not find layer '{}'".format(vec_lyr))

    colExists = False
    lyrDefn = lyr.GetLayerDefn()
    for i in range(lyrDefn.GetFieldCount()):
        if lyrDefn.GetFieldDefn(i).GetName() == att_column:
            colExists = True
            break

    if not colExists:
        ds = None
        raise Exception(
            "The specified column does not exist in the input layer; "
            "check case as some drivers are case sensitive."
        )

    outVal = list()
    lyr.ResetReading()
    for feat in lyr:
        outVal.append(feat.GetField(att_column))
    ds = None

    return outVal




def polygoniseRaster2VecLyr(out_vec_file: str, out_vec_lyr: str, out_format: str, input_img: str, img_band: int =1,
                            mask_img: str =None, mask_band: int =1, replace_file: bool =True, replace_lyr: bool =True,
                            pxl_val_fieldname: str ='PXLVAL', use_8_conn: bool =False):
    """
A utility to polygonise a raster to a OGR vector layer. Recommended that you output with 8 connectedness
otherwise the resulting vector can be invalid and cause problems for further processing in GIS applications.

Where:

:param out_vec_file: is a string specifying the output vector file path. If it exists it will be deleted and overwritten.
:param out_vec_lyr: is a string with the name of the vector layer.
:param out_format: is a string with the driver
:param input_img: is a string specifying the input image file to be polygonised
:param img_band: is an int specifying the image band to be polygonised. (default = 1)
:param mask_img: is an optional string mask file specifying a no data mask (default = None)
:param mask_band: is an int specifying the image band to be used the mask (default = 1)
:param replace_file: is a boolean specifying whether the vector file should be replaced (i.e., overwritten). Default=True.
:param replace_lyr: is a boolean specifying whether the vector layer should be replaced (i.e., overwritten). Default=True.
:param pxl_val_fieldname: is a string to specify the name of the output column representing the pixel value within the input image.
:param use_8_conn: is a bool specifying whether 8 connectedness or 4 connectedness should be used (8 is RSGISLib default but 4 is GDAL default)

"""
    gdal.UseExceptions()

    gdalImgDS = gdal.Open(input_img)
    imgBand = gdalImgDS.GetRasterBand(img_band)
    imgsrs = osr.SpatialReference()
    imgsrs.ImportFromWkt(gdalImgDS.GetProjectionRef())

    gdalImgMaskDS = None
    imgMaskBand = None
    if mask_img is not None:
        gdalImgMaskDS = gdal.Open(mask_img)
        imgMaskBand = gdalImgMaskDS.GetRasterBand(mask_band)

    if os.path.exists(out_vec_file) and (not replace_file):
        vecDS = gdal.OpenEx(out_vec_file, gdal.GA_Update)
    else:
        outdriver = ogr.GetDriverByName(out_format)
        if os.path.exists(out_vec_file):
            outdriver.DeleteDataSource(out_format)
        vecDS = outdriver.CreateDataSource(out_vec_file)

    if vecDS is None:
        raise Exception("Could not open or create '{}'".format(out_vec_file))

    lcl_options = []
    if replace_lyr:
        lcl_options = ['OVERWRITE=YES']

    out_lyr_obj = vecDS.CreateLayer(out_vec_lyr, srs=imgsrs, options=lcl_options)
    if out_lyr_obj is None:
        raise Exception("Could not create layer: {}".format(out_vec_lyr))

    newField = ogr.FieldDefn(pxl_val_fieldname, ogr.OFTInteger)
    out_lyr_obj.CreateField(newField)
    dstFieldIdx = out_lyr_obj.GetLayerDefn().GetFieldIndex(pxl_val_fieldname)

    try:
        import tqdm
        pbar = tqdm.tqdm(total=100)
        callback = lambda *args, **kw: pbar.update()
    except:
        callback = gdal.TermProgress

    options = list()
    if use_8_conn:
        options.append('8CONNECTED=8')

    print("Polygonising...")
    gdal.Polygonize(imgBand, imgMaskBand, out_lyr_obj, dstFieldIdx, options, callback=callback )
    print("Completed")
    out_lyr_obj.SyncToDisk()
    vecDS = None
    gdalImgDS = None
    if mask_img is not None:
        gdalImgMaskDS = None



class CreateVectorTile(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_vec_tile.py', descript=None)

    def do_processing(self, **kwargs):
        pxl_count = rsgislib.imagecalc.countPxlsOfVal(self.params['img_tile'], vals=[1, 2])
        tot_pxl_count = pxl_count[0] + pxl_count[1]
        print("N Pixels: ", tot_pxl_count)

        if tot_pxl_count > 0:
            polygoniseRaster2VecLyr(self.params['out_vec'], self.params['out_lyr_name'], 'GPKG',
                                    self.params['img_tile'], img_band=1,
                                    mask_img=self.params['img_tile'],
                                    mask_band=1, replace_file=True, replace_lyr=True,
                                    pxl_val_fieldname='chng_type_id', use_8_conn=False)

            pxl_val_col = read_vec_column(self.params['out_vec'], self.params['out_lyr_name'], "chng_type_id")
            out_vals = list()
            for val in pxl_val_col:
                if val == 1:
                    out_vals.append("gain")
                elif val == 2:
                    out_vals.append("loss")
                else:
                    out_vals.append("")

            write_vec_column(self.params['out_vec'], self.params['out_lyr_name'], "chng_type", ogr.OFTString, out_vals)

        pathlib.Path(self.params['out_cmp_file']).touch()

    def required_fields(self, **kwargs):
        return ["img_tile", "out_vec", "out_lyr_name", "out_cmp_file"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_vec']] = 'gdal_vector'
        files_dict[self.params['out_cmp_file']] = 'file'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_vec']):
            os.remove(self.params['out_vec'])

        if os.path.exists(self.params['out_cmp_file']):
            os.remove(self.params['out_cmp_file'])

if __name__ == "__main__":
    CreateVectorTile().std_run()


