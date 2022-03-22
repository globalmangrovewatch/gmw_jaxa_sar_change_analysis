import rsgislib.tools.utils
import matplotlib.pyplot as plt

gmw_acc_info = rsgislib.tools.utils.read_json_to_dict("gmw_chng_acc_stats_pt_smpls_conf_int.json")

culm_n_pts_low_lst = gmw_acc_info["n_pts_low"]
culm_n_pts_med_lst = gmw_acc_info["n_pts_med"]
culm_n_pts_up_lst = gmw_acc_info["n_pts_up"]

overall_low_lst = gmw_acc_info["overall_low"]
overall_med_lst = gmw_acc_info["overall_med"]
overall_up_lst = gmw_acc_info["overall_up"]

acc_stats_dict_f1_score_low = gmw_acc_info["acc_stats_f1_score_low"]
acc_stats_dict_f1_score_med = gmw_acc_info["acc_stats_f1_score_med"]
acc_stats_dict_f1_score_up = gmw_acc_info["acc_stats_f1_score_up"]

acc_stats_dict_recall_low = gmw_acc_info["acc_stats_recall_low"]
acc_stats_dict_recall_med = gmw_acc_info["acc_stats_recall_med"]
acc_stats_dict_recall_up = gmw_acc_info["acc_stats_recall_up"]

acc_stats_dict_precision_low = gmw_acc_info["acc_stats_precision_low"]
acc_stats_dict_precision_med = gmw_acc_info["acc_stats_precision_med"]
acc_stats_dict_precision_up = gmw_acc_info["acc_stats_precision_up"]

acc_stats_dict_support_low = gmw_acc_info["acc_stats_support_low"]
acc_stats_dict_support_med = gmw_acc_info["acc_stats_support_med"]
acc_stats_dict_support_up = gmw_acc_info["acc_stats_support_up"]


cls_clrs = dict()
cls_clrs["Mangroves"] = [0.0, 1.0, 0.0]
cls_clrs["Not Mangroves"] = [0.2, 0.2, 0.2]
cls_clrs["Mangroves > Not Mangroves"] = [1.0, 0.0, 0.0]
cls_clrs["Not Mangroves > Mangroves"] = [0.0, 0.0, 1.0]

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 10), sharex=True, sharey=True)

ax1.plot(culm_n_pts_med_lst, acc_stats_dict_f1_score_med["Mangroves"], color=cls_clrs["Mangroves"])
ax1.fill_between(culm_n_pts_med_lst, acc_stats_dict_f1_score_low["Mangroves"], acc_stats_dict_f1_score_up["Mangroves"], color=[0.9,0.9,0.9])
ax1.set_title("Mangroves")
ax1.set_ylim(0.75, 1)

ax2.plot(culm_n_pts_med_lst, acc_stats_dict_f1_score_med["Not Mangroves"], color=cls_clrs["Not Mangroves"])
ax2.fill_between(culm_n_pts_med_lst, acc_stats_dict_f1_score_low["Not Mangroves"], acc_stats_dict_f1_score_up["Not Mangroves"], color=[0.9,0.9,0.9])
ax2.set_title("Not Mangroves")
ax2.set_ylim(0.75, 1)

ax3.plot(culm_n_pts_med_lst, acc_stats_dict_f1_score_med["Mangroves > Not Mangroves"], color=cls_clrs["Mangroves > Not Mangroves"])
ax3.fill_between(culm_n_pts_med_lst, acc_stats_dict_f1_score_low["Mangroves > Not Mangroves"], acc_stats_dict_f1_score_up["Mangroves > Not Mangroves"], color=[0.9,0.9,0.9])
ax3.set_title("Mangroves > Not Mangroves")
ax3.set_ylim(0, 1)

ax4.plot(culm_n_pts_med_lst, acc_stats_dict_f1_score_med["Not Mangroves > Mangroves"], color=cls_clrs["Not Mangroves > Mangroves"])
ax4.fill_between(culm_n_pts_med_lst, acc_stats_dict_f1_score_low["Not Mangroves > Mangroves"], acc_stats_dict_f1_score_up["Not Mangroves > Mangroves"], color=[0.9,0.9,0.9])
ax4.set_title("Not Mangroves > Mangroves")
ax4.set_ylim(0, 1)

fig.suptitle("f1-score with increasing samples.")
fig.supxlabel("n samples")
fig.supylabel("f1-score")
plt.tight_layout()
plt.savefig("f1-score_increase_samples_conf_int.pdf")


fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 10), sharex=True, sharey=False)

ax1.plot(culm_n_pts_med_lst, acc_stats_dict_support_med["Mangroves"], color=cls_clrs["Mangroves"])
ax1.fill_between(culm_n_pts_med_lst, acc_stats_dict_support_low["Mangroves"], acc_stats_dict_support_up["Mangroves"], color=[0.9,0.9,0.9])
ax1.set_title("Mangroves")
#ax1.set_ylim(0.75, 1)

ax2.plot(culm_n_pts_med_lst, acc_stats_dict_support_med["Not Mangroves"], color=cls_clrs["Not Mangroves"])
ax2.fill_between(culm_n_pts_med_lst, acc_stats_dict_support_low["Not Mangroves"], acc_stats_dict_support_up["Not Mangroves"], color=[0.9,0.9,0.9])
ax2.set_title("Not Mangroves")
#ax2.set_ylim(0.75, 1)

ax3.plot(culm_n_pts_med_lst, acc_stats_dict_support_med["Mangroves > Not Mangroves"], color=cls_clrs["Mangroves > Not Mangroves"])
ax3.fill_between(culm_n_pts_med_lst, acc_stats_dict_support_low["Mangroves > Not Mangroves"], acc_stats_dict_support_up["Mangroves > Not Mangroves"], color=[0.9,0.9,0.9])
ax3.set_title("Mangroves > Not Mangroves")
#ax3.set_ylim(0, 1)

ax4.plot(culm_n_pts_med_lst, acc_stats_dict_support_med["Not Mangroves > Mangroves"], color=cls_clrs["Not Mangroves > Mangroves"])
ax4.fill_between(culm_n_pts_med_lst, acc_stats_dict_support_low["Not Mangroves > Mangroves"], acc_stats_dict_support_up["Not Mangroves > Mangroves"], color=[0.9,0.9,0.9])
ax4.set_title("Not Mangroves > Mangroves")
#ax4.set_ylim(0, 1)

fig.suptitle("Support with increasing samples.")
fig.supxlabel("n samples")
fig.supylabel("Support")
plt.tight_layout()
plt.savefig("support_increase_samples_conf_int.pdf")

fig, ax = plt.subplots(figsize=(10, 10))

ax.plot(culm_n_pts_med_lst, overall_med_lst, color="black")
ax.fill_between(culm_n_pts_med_lst, overall_low_lst, overall_up_lst, color=[0.9,0.9,0.9])
ax.set_title("Overall Accuracy")
ax.set_ylim(0.8, 1)
fig.supylabel("%")
plt.tight_layout()
plt.savefig("overall_accuracy_increase_samples_conf_int.pdf")
