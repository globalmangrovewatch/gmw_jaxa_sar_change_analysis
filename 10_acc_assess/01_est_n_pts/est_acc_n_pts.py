from classaccuracymetrics import create_modelled_acc_pts, calc_sampled_acc_metrics



cls_lst = ["Mangroves", "Not Mangroves", "Mangroves to Not Mangroves", "Not Mangroves to Mangroves"]

cls_clrs = dict()
cls_clrs["Mangroves"] = [0.0, 1.0, 0.0]
cls_clrs["Not Mangroves"] = [0.8, 0.8, 0.8]
cls_clrs["Mangroves to Not Mangroves"] = [1.0, 0.0, 0.0]
cls_clrs["Not Mangroves to Mangroves"] = [0.0, 0.0, 1.0]


err_mtx_unit_area = [[0.378, 0.02,  0.002, 0.0  ],
                     [0.02,  0.478, 0.0,   0.002],
                     [0.02, 0.0,   0.03, 0.0],
                     [0.0,   0.02, 0.0,   0.03]]


ref_samples, pred_samples = create_modelled_acc_pts(err_mtx_unit_area, cls_lst, 1600)



calc_sampled_acc_metrics(ref_samples, pred_samples, cls_lst, [400, 500, 600, 700, 800, 900, 1000, 1500], out_metrics_file="out_stats.json", out_usr_metrics_plot="out_usrs_plot.png", out_prod_metrics_plot="out_prod_plot.png", out_ref_usr_plot="ref_usr_plot.png", out_ref_prod_plot="ref_prod_plot.png", cls_colours=cls_clrs)



