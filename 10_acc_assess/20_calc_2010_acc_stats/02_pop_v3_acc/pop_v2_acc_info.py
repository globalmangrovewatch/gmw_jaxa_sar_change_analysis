import os
import rsgislib.classification


def pop_acc_pts(input_img, vec_file, vec_lyr):
    rsgislib.classification.pop_class_info_accuracy_pts(input_img, vec_file, vec_lyr, "cls_name", "gmw_v3_cls")



pts_dir = "../00_datasets/acc_pts/"
imgs_dir = "../00_datasets/roi_v314_cls_imgs"
for i in range(60):
    vec_acc_pts_file = os.path.join(pts_dir, "gmw_v25_set_{}_acc_pts.geojson".format(i+1))
    vec_acc_pts_lyr = "gmw_v25_set_{}_acc_pts".format(i+1)
    
    img = os.path.join(imgs_dir, "gmw_acc_roi_{}_cls.kea".format(i+1))
    if os.path.exists(vec_acc_pts_file):
        pop_acc_pts(img, vec_acc_pts_file, vec_acc_pts_lyr)
    else:
        raise Exception("Could not find input file: {}".format(vec_acc_pts_file))
