import numpy
import rsgislib.tools.utils

in_stats = rsgislib.tools.utils.read_json_to_dict("gmw_chng_acc_stats_pt_smpls_conf_int_iters.json")

culm_n_pts_lst_iters = in_stats["n_pts_iters"]
acc_stats_dict_iters = in_stats["acc_stats_iters"]

n_vec_files = len(culm_n_pts_lst_iters[0])
print(n_vec_files)

# Calculate the mean and 5th and 95th conf intervals
culm_n_pts_lst_iters_arr = numpy.array(culm_n_pts_lst_iters)
#print(culm_n_pts_lst_iters_arr)

f1_score_dict_iters = dict()
f1_score_dict_iters["Mangroves"] = list()
f1_score_dict_iters["Mangroves > Not Mangroves"] = list()
f1_score_dict_iters["Not Mangroves"] = list()
f1_score_dict_iters["Not Mangroves > Mangroves"] = list()

recall_dict_iters = dict()
recall_dict_iters["Mangroves"] = list()
recall_dict_iters["Mangroves > Not Mangroves"] = list()
recall_dict_iters["Not Mangroves"] = list()
recall_dict_iters["Not Mangroves > Mangroves"] = list()

precision_dict_iters = dict()
precision_dict_iters["Mangroves"] = list()
precision_dict_iters["Mangroves > Not Mangroves"] = list()
precision_dict_iters["Not Mangroves"] = list()
precision_dict_iters["Not Mangroves > Mangroves"] = list()

support_dict_iters = dict()
support_dict_iters["Mangroves"] = list()
support_dict_iters["Mangroves > Not Mangroves"] = list()
support_dict_iters["Not Mangroves"] = list()
support_dict_iters["Not Mangroves > Mangroves"] = list()

acc_stats_overall = acc_stats_dict_iters["Overall"]

for cls in acc_stats_dict_iters:
    if cls != "Overall":
        for i, item_lst in enumerate(acc_stats_dict_iters[cls]):
            f1_score_dict_iters[cls].append(list())
            recall_dict_iters[cls].append(list())
            precision_dict_iters[cls].append(list())
            support_dict_iters[cls].append(list())
            for val_dict in item_lst:
                f1_score_dict_iters[cls][i].append(val_dict["f1-score"])
                recall_dict_iters[cls][i].append(val_dict["recall"])
                precision_dict_iters[cls][i].append(val_dict["precision"])
                support_dict_iters[cls][i].append(val_dict["support"])


f1_score_dict_iters_arr = dict()
f1_score_dict_iters_arr["Mangroves"] = numpy.array(f1_score_dict_iters["Mangroves"])
f1_score_dict_iters_arr["Mangroves > Not Mangroves"] = numpy.array(f1_score_dict_iters["Mangroves > Not Mangroves"])
f1_score_dict_iters_arr["Not Mangroves"] = numpy.array(f1_score_dict_iters["Not Mangroves"])
f1_score_dict_iters_arr["Not Mangroves > Mangroves"] = numpy.array(f1_score_dict_iters["Not Mangroves > Mangroves"])

recall_dict_iters_arr = dict()
recall_dict_iters_arr["Mangroves"] = numpy.array(recall_dict_iters["Mangroves"])
recall_dict_iters_arr["Mangroves > Not Mangroves"] = numpy.array(recall_dict_iters["Mangroves > Not Mangroves"])
recall_dict_iters_arr["Not Mangroves"] = numpy.array(recall_dict_iters["Not Mangroves"])
recall_dict_iters_arr["Not Mangroves > Mangroves"] = numpy.array(recall_dict_iters["Not Mangroves > Mangroves"])

precision_dict_iters_arr = dict()
precision_dict_iters_arr["Mangroves"] = numpy.array(precision_dict_iters["Mangroves"])
precision_dict_iters_arr["Mangroves > Not Mangroves"] = numpy.array(precision_dict_iters["Mangroves > Not Mangroves"])
precision_dict_iters_arr["Not Mangroves"] = numpy.array(precision_dict_iters["Not Mangroves"])
precision_dict_iters_arr["Not Mangroves > Mangroves"] = numpy.array(precision_dict_iters["Not Mangroves > Mangroves"])

support_dict_iters_arr = dict()
support_dict_iters_arr["Mangroves"] = numpy.array(support_dict_iters["Mangroves"])
support_dict_iters_arr["Mangroves > Not Mangroves"] = numpy.array(support_dict_iters["Mangroves > Not Mangroves"])
support_dict_iters_arr["Not Mangroves"] = numpy.array(support_dict_iters["Not Mangroves"])
support_dict_iters_arr["Not Mangroves > Mangroves"] = numpy.array(support_dict_iters["Not Mangroves > Mangroves"])

acc_stats_overall_arr = numpy.array(acc_stats_overall)

culm_n_pts_low_lst = list()
culm_n_pts_median_lst = list()
culm_n_pts_up_lst = list()

overall_low_lst = list()
overall_median_lst = list()
overall_up_lst = list()

# F1-score
acc_stats_dict_f1_score_low = dict()
acc_stats_dict_f1_score_low["Mangroves"] = list()
acc_stats_dict_f1_score_low["Mangroves > Not Mangroves"] = list()
acc_stats_dict_f1_score_low["Not Mangroves"] = list()
acc_stats_dict_f1_score_low["Not Mangroves > Mangroves"] = list()

acc_stats_dict_f1_score_med = dict()
acc_stats_dict_f1_score_med["Mangroves"] = list()
acc_stats_dict_f1_score_med["Mangroves > Not Mangroves"] = list()
acc_stats_dict_f1_score_med["Not Mangroves"] = list()
acc_stats_dict_f1_score_med["Not Mangroves > Mangroves"] = list()

acc_stats_dict_f1_score_up = dict()
acc_stats_dict_f1_score_up["Mangroves"] = list()
acc_stats_dict_f1_score_up["Mangroves > Not Mangroves"] = list()
acc_stats_dict_f1_score_up["Not Mangroves"] = list()
acc_stats_dict_f1_score_up["Not Mangroves > Mangroves"] = list()

# recall
acc_stats_dict_recall_low = dict()
acc_stats_dict_recall_low["Mangroves"] = list()
acc_stats_dict_recall_low["Mangroves > Not Mangroves"] = list()
acc_stats_dict_recall_low["Not Mangroves"] = list()
acc_stats_dict_recall_low["Not Mangroves > Mangroves"] = list()

acc_stats_dict_recall_med = dict()
acc_stats_dict_recall_med["Mangroves"] = list()
acc_stats_dict_recall_med["Mangroves > Not Mangroves"] = list()
acc_stats_dict_recall_med["Not Mangroves"] = list()
acc_stats_dict_recall_med["Not Mangroves > Mangroves"] = list()

acc_stats_dict_recall_up = dict()
acc_stats_dict_recall_up["Mangroves"] = list()
acc_stats_dict_recall_up["Mangroves > Not Mangroves"] = list()
acc_stats_dict_recall_up["Not Mangroves"] = list()
acc_stats_dict_recall_up["Not Mangroves > Mangroves"] = list()

# precision
acc_stats_dict_precision_low = dict()
acc_stats_dict_precision_low["Mangroves"] = list()
acc_stats_dict_precision_low["Mangroves > Not Mangroves"] = list()
acc_stats_dict_precision_low["Not Mangroves"] = list()
acc_stats_dict_precision_low["Not Mangroves > Mangroves"] = list()

acc_stats_dict_precision_med = dict()
acc_stats_dict_precision_med["Mangroves"] = list()
acc_stats_dict_precision_med["Mangroves > Not Mangroves"] = list()
acc_stats_dict_precision_med["Not Mangroves"] = list()
acc_stats_dict_precision_med["Not Mangroves > Mangroves"] = list()

acc_stats_dict_precision_up = dict()
acc_stats_dict_precision_up["Mangroves"] = list()
acc_stats_dict_precision_up["Mangroves > Not Mangroves"] = list()
acc_stats_dict_precision_up["Not Mangroves"] = list()
acc_stats_dict_precision_up["Not Mangroves > Mangroves"] = list()

# Support
acc_stats_dict_support_low = dict()
acc_stats_dict_support_low["Mangroves"] = list()
acc_stats_dict_support_low["Mangroves > Not Mangroves"] = list()
acc_stats_dict_support_low["Not Mangroves"] = list()
acc_stats_dict_support_low["Not Mangroves > Mangroves"] = list()

acc_stats_dict_support_med = dict()
acc_stats_dict_support_med["Mangroves"] = list()
acc_stats_dict_support_med["Mangroves > Not Mangroves"] = list()
acc_stats_dict_support_med["Not Mangroves"] = list()
acc_stats_dict_support_med["Not Mangroves > Mangroves"] = list()

acc_stats_dict_support_up = dict()
acc_stats_dict_support_up["Mangroves"] = list()
acc_stats_dict_support_up["Mangroves > Not Mangroves"] = list()
acc_stats_dict_support_up["Not Mangroves"] = list()
acc_stats_dict_support_up["Not Mangroves > Mangroves"] = list()

for i in range(n_vec_files):
    percentile_vals = numpy.percentile(culm_n_pts_lst_iters_arr[...,i], [5,50,95])
    culm_n_pts_low_lst.append(float(percentile_vals[0]))
    culm_n_pts_median_lst.append(float(percentile_vals[1]))
    culm_n_pts_up_lst.append(float(percentile_vals[2]))

    percentile_vals = numpy.percentile(acc_stats_overall_arr[..., i], [5, 50, 95])
    overall_low_lst.append(float(percentile_vals[0]))
    overall_median_lst.append(float(percentile_vals[1]))
    overall_up_lst.append(float(percentile_vals[2]))

    percentile_vals = numpy.percentile(f1_score_dict_iters_arr["Mangroves"][..., i], [5, 50, 95])
    acc_stats_dict_f1_score_low["Mangroves"].append(float(percentile_vals[0]))
    acc_stats_dict_f1_score_med["Mangroves"].append(float(percentile_vals[1]))
    acc_stats_dict_f1_score_up["Mangroves"].append(float(percentile_vals[2]))

    percentile_vals = numpy.percentile(f1_score_dict_iters_arr["Mangroves > Not Mangroves"][..., i], [5, 50, 95])
    acc_stats_dict_f1_score_low["Mangroves > Not Mangroves"].append(float(percentile_vals[0]))
    acc_stats_dict_f1_score_med["Mangroves > Not Mangroves"].append(float(percentile_vals[1]))
    acc_stats_dict_f1_score_up["Mangroves > Not Mangroves"].append(float(percentile_vals[2]))

    percentile_vals = numpy.percentile(f1_score_dict_iters_arr["Not Mangroves"][..., i], [5, 50, 95])
    acc_stats_dict_f1_score_low["Not Mangroves"].append(float(percentile_vals[0]))
    acc_stats_dict_f1_score_med["Not Mangroves"].append(float(percentile_vals[1]))
    acc_stats_dict_f1_score_up["Not Mangroves"].append(float(percentile_vals[2]))

    percentile_vals = numpy.percentile(f1_score_dict_iters_arr["Not Mangroves > Mangroves"][..., i], [5, 50, 95])
    acc_stats_dict_f1_score_low["Not Mangroves > Mangroves"].append(float(percentile_vals[0]))
    acc_stats_dict_f1_score_med["Not Mangroves > Mangroves"].append(float(percentile_vals[1]))
    acc_stats_dict_f1_score_up["Not Mangroves > Mangroves"].append(float(percentile_vals[2]))


    percentile_vals = numpy.percentile(recall_dict_iters_arr["Mangroves"][..., i], [5, 50, 95])
    acc_stats_dict_recall_low["Mangroves"].append(float(percentile_vals[0]))
    acc_stats_dict_recall_med["Mangroves"].append(float(percentile_vals[1]))
    acc_stats_dict_recall_up["Mangroves"].append(float(percentile_vals[2]))

    percentile_vals = numpy.percentile(recall_dict_iters_arr["Mangroves > Not Mangroves"][..., i], [5, 50, 95])
    acc_stats_dict_recall_low["Mangroves > Not Mangroves"].append(float(percentile_vals[0]))
    acc_stats_dict_recall_med["Mangroves > Not Mangroves"].append(float(percentile_vals[1]))
    acc_stats_dict_recall_up["Mangroves > Not Mangroves"].append(float(percentile_vals[2]))

    percentile_vals = numpy.percentile(recall_dict_iters_arr["Not Mangroves"][..., i], [5, 50, 95])
    acc_stats_dict_recall_low["Not Mangroves"].append(float(percentile_vals[0]))
    acc_stats_dict_recall_med["Not Mangroves"].append(float(percentile_vals[1]))
    acc_stats_dict_recall_up["Not Mangroves"].append(float(percentile_vals[2]))

    percentile_vals = numpy.percentile(recall_dict_iters_arr["Not Mangroves > Mangroves"][..., i], [5, 50, 95])
    acc_stats_dict_recall_low["Not Mangroves > Mangroves"].append(float(percentile_vals[0]))
    acc_stats_dict_recall_med["Not Mangroves > Mangroves"].append(float(percentile_vals[1]))
    acc_stats_dict_recall_up["Not Mangroves > Mangroves"].append(float(percentile_vals[2]))

    percentile_vals = numpy.percentile(precision_dict_iters_arr["Mangroves"][..., i], [5, 50, 95])
    acc_stats_dict_precision_low["Mangroves"].append(float(percentile_vals[0]))
    acc_stats_dict_precision_med["Mangroves"].append(float(percentile_vals[1]))
    acc_stats_dict_precision_up["Mangroves"].append(float(percentile_vals[2]))

    percentile_vals = numpy.percentile(precision_dict_iters_arr["Mangroves > Not Mangroves"][..., i], [5, 50, 95])
    acc_stats_dict_precision_low["Mangroves > Not Mangroves"].append(float(percentile_vals[0]))
    acc_stats_dict_precision_med["Mangroves > Not Mangroves"].append(float(percentile_vals[1]))
    acc_stats_dict_precision_up["Mangroves > Not Mangroves"].append(float(percentile_vals[2]))

    percentile_vals = numpy.percentile(precision_dict_iters_arr["Not Mangroves"][..., i], [5, 50, 95])
    acc_stats_dict_precision_low["Not Mangroves"].append(float(percentile_vals[0]))
    acc_stats_dict_precision_med["Not Mangroves"].append(float(percentile_vals[1]))
    acc_stats_dict_precision_up["Not Mangroves"].append(float(percentile_vals[2]))

    percentile_vals = numpy.percentile(precision_dict_iters_arr["Not Mangroves > Mangroves"][..., i], [5, 50, 95])
    acc_stats_dict_precision_low["Not Mangroves > Mangroves"].append(float(percentile_vals[0]))
    acc_stats_dict_precision_med["Not Mangroves > Mangroves"].append(float(percentile_vals[1]))
    acc_stats_dict_precision_up["Not Mangroves > Mangroves"].append(float(percentile_vals[2]))

    percentile_vals = numpy.percentile(support_dict_iters_arr["Mangroves"][..., i], [5, 50, 95])
    acc_stats_dict_support_low["Mangroves"].append(float(percentile_vals[0]))
    acc_stats_dict_support_med["Mangroves"].append(float(percentile_vals[1]))
    acc_stats_dict_support_up["Mangroves"].append(float(percentile_vals[2]))

    percentile_vals = numpy.percentile(support_dict_iters_arr["Mangroves > Not Mangroves"][..., i], [5, 50, 95])
    acc_stats_dict_support_low["Mangroves > Not Mangroves"].append(float(percentile_vals[0]))
    acc_stats_dict_support_med["Mangroves > Not Mangroves"].append(float(percentile_vals[1]))
    acc_stats_dict_support_up["Mangroves > Not Mangroves"].append(float(percentile_vals[2]))

    percentile_vals = numpy.percentile(support_dict_iters_arr["Not Mangroves"][..., i], [5, 50, 95])
    acc_stats_dict_support_low["Not Mangroves"].append(float(percentile_vals[0]))
    acc_stats_dict_support_med["Not Mangroves"].append(float(percentile_vals[1]))
    acc_stats_dict_support_up["Not Mangroves"].append(float(percentile_vals[2]))

    percentile_vals = numpy.percentile(support_dict_iters_arr["Not Mangroves > Mangroves"][..., i], [5, 50, 95])
    acc_stats_dict_support_low["Not Mangroves > Mangroves"].append(float(percentile_vals[0]))
    acc_stats_dict_support_med["Not Mangroves > Mangroves"].append(float(percentile_vals[1]))
    acc_stats_dict_support_up["Not Mangroves > Mangroves"].append(float(percentile_vals[2]))



out_info = dict()
out_info["n_pts_low"] = culm_n_pts_low_lst
out_info["n_pts_med"] = culm_n_pts_median_lst
out_info["n_pts_up"] = culm_n_pts_up_lst

out_info["overall_low"] = overall_low_lst
out_info["overall_med"] = overall_median_lst
out_info["overall_up"] = overall_up_lst

out_info["acc_stats_f1_score_low"] = acc_stats_dict_f1_score_low
out_info["acc_stats_f1_score_med"] = acc_stats_dict_f1_score_med
out_info["acc_stats_f1_score_up"] = acc_stats_dict_f1_score_up

out_info["acc_stats_recall_low"] = acc_stats_dict_recall_low
out_info["acc_stats_recall_med"] = acc_stats_dict_recall_med
out_info["acc_stats_recall_up"] = acc_stats_dict_recall_up

out_info["acc_stats_precision_low"] = acc_stats_dict_precision_low
out_info["acc_stats_precision_med"] = acc_stats_dict_precision_med
out_info["acc_stats_precision_up"] = acc_stats_dict_precision_up

out_info["acc_stats_support_low"] = acc_stats_dict_support_low
out_info["acc_stats_support_med"] = acc_stats_dict_support_med
out_info["acc_stats_support_up"] = acc_stats_dict_support_up

rsgislib.tools.utils.write_dict_to_json(out_info, "gmw_chng_acc_stats_pt_smpls_conf_int.json")
