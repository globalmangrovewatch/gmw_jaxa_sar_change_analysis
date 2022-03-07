import ee
import geemap
import os
import rsgislib
import rsgislib.tools.filetools
import rsgislib.imageutils


def downloadFile(url, remote_path, local_path, time_out=None, username=None, password=None):
    """
    :param url:
    :param remote_path:
    :param local_path:
    :param time_out: (default 300 seconds if None)
    :param username:
    :param password:
    :return:
    """
    import pycurl
    full_path_url = url+remote_path
    success = False
    try:
        if time_out is None:
            time_out = 300

        fp = open(local_path, "wb")
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, full_path_url)
        curl.setopt(pycurl.FOLLOWLOCATION, True)
        curl.setopt(pycurl.NOPROGRESS, 0)
        curl.setopt(pycurl.FOLLOWLOCATION, 1)
        curl.setopt(pycurl.MAXREDIRS, 5)
        curl.setopt(pycurl.CONNECTTIMEOUT, 50)
        curl.setopt(pycurl.TIMEOUT, time_out)
        curl.setopt(pycurl.FTP_RESPONSE_TIMEOUT, 600)
        curl.setopt(pycurl.NOSIGNAL, 1)
        if (not username is None) and (not password is None):
            curl.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_ANY)
            curl.setopt(pycurl.USERPWD, username + ':' + password)
        curl.setopt(pycurl.WRITEDATA, fp)
        print("Starting download of {}".format(full_path_url))
        curl.perform()
        print("Finished download in {0} of {1} bytes for {2}".format(curl.getinfo(curl.TOTAL_TIME), curl.getinfo(curl.SIZE_DOWNLOAD), full_path_url))
        success = True
    except:
        print("An error occurred when downloading {}.".format(os.path.join(url, remote_path)))
        success = False
    return success


def extract_data_gee(ls_row, ls_path, s_date, e_date, bbox, tmp_dir, out_img, landsat_col):
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)
    
    Map = geemap.Map()
    
    collection = ee.ImageCollection(landsat_col) \
      .filterDate(s_date, e_date) \
      .filter(ee.Filter.eq('WRS_PATH', ls_path)) \
      .filter(ee.Filter.eq('WRS_ROW', ls_row))
    
    # Compute the median in each band, each pixel.
    # Band names are B1_median, B2_median, etc.
    median = collection.reduce(ee.Reducer.median())
    
    # The output is an Image.  Add it to the map.
    #vis_param = {'bands': ['B4_median', 'B5_median', 'B3_median'], 'opacity': 1.0, 'gamma': 1.2}
    #Map.setCenter(-122.3355, 37.7924, 9)
    #Map.addLayer(median, vis_param, 'Median Image')
    
    bbox_str = '[[{0}, {3}], [{1}, {3}], [{1}, {2}], [{0}, {2}]]'.format(*bbox)
    print(bbox_str)
    
    url_path = median.getDownloadUrl({
        'scale': 30,
        'crs': 'EPSG:4326',
        'region': bbox_str
    })

    #'[[-122.2, 37.7], [-122.0, 37.7], [-122.0, 37.5], [-122.2, 37.5]]'
    
    print(url_path)
    
    dwnld_file = os.path.join(tmp_dir, "download.zip")
    downloadFile(url_path, "", local_path=dwnld_file)
    
        
    rsgislib.tools.filetools.unzip_file(dwnld_file, out_dir=tmp_dir, gen_arch_dir=False, verbose=True)
    
    
    #out_img = "r44_p34_2008_img.kea"
    input_imgs = list()
    input_imgs.append(rsgislib.tools.filetools.find_file_none(tmp_dir, "*B1*.tif"))
    input_imgs.append(rsgislib.tools.filetools.find_file_none(tmp_dir, "*B2*.tif"))
    input_imgs.append(rsgislib.tools.filetools.find_file_none(tmp_dir, "*B3*.tif"))
    input_imgs.append(rsgislib.tools.filetools.find_file_none(tmp_dir, "*B4*.tif"))
    input_imgs.append(rsgislib.tools.filetools.find_file_none(tmp_dir, "*B5*.tif"))
    #input_imgs.append(rsgislib.tools.filetools.find_file_none(tmp_dir, "*B6*.tif"))
    input_imgs.append(rsgislib.tools.filetools.find_file_none(tmp_dir, "*B7*.tif"))
    rsgislib.imageutils.stack_img_bands(input_imgs, None, out_img, 0, 0, "KEA", rsgislib.TYPE_32FLOAT)
    rsgislib.imageutils.pop_img_stats(out_img, use_no_data=True, no_data_val=0, calc_pyramids=True)



def extract_data_gee_to_drive(ls_row, ls_path, s_date, e_date, bbox, out_img, out_folder, landsat_col):
    
    Map = geemap.Map()
    
    collection = ee.ImageCollection(landsat_col) \
      .filterDate(s_date, e_date) \
      .filter(ee.Filter.eq('WRS_PATH', ls_path)) \
      .filter(ee.Filter.eq('WRS_ROW', ls_row))
    
    # Compute the median in each band, each pixel.
    # Band names are B1_median, B2_median, etc.
    #median_img = collection.reduce(ee.Reducer.median())
    composite_img = ee.Algorithms.Landsat.simpleComposite(collection)

    
    geom = ee.Geometry.Polygon(
        [
            [
                [bbox[0], bbox[3]],
                [bbox[1], bbox[3]],
                [bbox[1], bbox[2]],
                [bbox[0], bbox[2]],
            ]
        ]
    )
    feature = ee.Feature(geom, {})
    roi = feature.geometry()
    
    
    geemap.ee_export_image_to_drive(composite_img, description=out_img, folder=out_folder, region=roi, scale=30)


#extract_data_gee(ls_row=34, ls_path=44, s_date='2008-01-01', e_date='2008-12-31', bbox=[-122.2, -122.0, 37.5, 37.7], tmp_dir="r44_p34_2008_tmp", out_img="r44_p34_2008_img.kea", landsat_col='LANDSAT/LT05/C01/T1')
#extract_data_gee_to_drive(ls_row=34, ls_path=44, s_date='2008-01-01', e_date='2008-12-31', bbox=[-122.2, -122.0, 37.5, 37.7], out_img="r44_p34_2008_img_c2", out_folder='export_gmw_ls', landsat_col='LANDSAT/LT05/C02/T1_L2')


years = [1996, 2007, 2008, 2009, 2010, 2015, 2016, 2017, 2018, 2019, 2020]

vec_file = "gmw_change_site_bboxs_ids_wrs2.geojson"
vec_lyr = "gmw_change_site_bboxs_ids_wrs2"


import rsgislib.vectorgeoms
import rsgislib.vectorattrs
import time


bboxes = rsgislib.vectorgeoms.get_geoms_as_bboxs(vec_file, vec_lyr)
site_info_lst = rsgislib.vectorattrs.read_vec_columns(vec_file, vec_lyr, ["roi_str_id", "PATH", "ROW"])

ls5 = 'LANDSAT/LT05/C01/T1'#C02/T1_L2'
ls8 = 'LANDSAT/LC08/C01/T1'#C02/T1_L2'

for bbox, site_info in zip(bboxes, site_info_lst):
    site = site_info['roi_str_id']
    row = site_info['ROW']
    path = site_info["PATH"]
    out_folder = f"gmw_ref_ls_comp_imgs_site_{site}"
    if site not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]:
        print(out_folder)
        for year in years:
            out_img_name = f"site_{site}_ls_r{row}_p{path}_{year}_img"
            ls_data = ls8
            if year < 2011:
                ls_data = ls5 
            extract_data_gee_to_drive(ls_row=row, ls_path=path, s_date=f'{year}-01-01', e_date=f'{year}-12-31', bbox=bbox, out_img=out_img_name, out_folder=out_folder, landsat_col=ls_data)
            
        time.sleep(600)



# Center the map and display the image.
#Map.centerObject(image, zoom=8)
#Map.addLayer(image, {}, 'Landsat')

#vis_params = {'bands': ['B5', 'B6', 'B4'], 'min': 0.0, 'max': 3000, 'opacity': 1.0, 'gamma': 1.2}
#Map.addLayer(image, vis_params, "Landsat Vis")

#Map
