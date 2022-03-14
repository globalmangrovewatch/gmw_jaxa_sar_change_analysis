import rsgislib.tools.utils
import matplotlib.pyplot as plt

gmw_acc_info = rsgislib.tools.utils.read_json_to_dict("gmw_chng_acc_stats_pt_smpls.json")

culm_n_pts_lst = gmw_acc_info["n_pts"]
acc_stats_dict = gmw_acc_info["acc_stats"]

mng_f1_scr = list()
nmng_f1_scr = list()
mng_nmng_f1_scr = list()
nmng_mng_f1_scr = list()

for acc_stats in acc_stats_dict["Mangroves"]:
    mng_f1_scr.append(acc_stats["f1-score"])

for acc_stats in acc_stats_dict["Not Mangroves"]:
    nmng_f1_scr.append(acc_stats["f1-score"])

for acc_stats in acc_stats_dict["Mangroves > Not Mangroves"]:
    mng_nmng_f1_scr.append(acc_stats["f1-score"])

for acc_stats in acc_stats_dict["Not Mangroves > Mangroves"]:
    nmng_mng_f1_scr.append(acc_stats["f1-score"])


mng_n_pts = list()
nmng_n_pts = list()
mng_nmng_n_pts = list()
nmng_mng_n_pts = list()

for acc_stats in acc_stats_dict["Mangroves"]:
    mng_n_pts.append(acc_stats["support"])

for acc_stats in acc_stats_dict["Not Mangroves"]:
    nmng_n_pts.append(acc_stats["support"])

for acc_stats in acc_stats_dict["Mangroves > Not Mangroves"]:
    mng_nmng_n_pts.append(acc_stats["support"])

for acc_stats in acc_stats_dict["Not Mangroves > Mangroves"]:
    nmng_mng_n_pts.append(acc_stats["support"])


cls_clrs = dict()
cls_clrs["Mangroves"] = [0.0, 1.0, 0.0]
cls_clrs["Not Mangroves"] = [0.2, 0.2, 0.2]
cls_clrs["Mangroves > Not Mangroves"] = [1.0, 0.0, 0.0]
cls_clrs["Not Mangroves > Mangroves"] = [0.0, 0.0, 1.0]

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 10), sharex=True, sharey=True)

ax1.plot(culm_n_pts_lst, mng_f1_scr, color=cls_clrs["Mangroves"])
ax1.set_title("Mangroves")
ax1.set_ylim(0.75, 1)

ax2.plot(culm_n_pts_lst, nmng_f1_scr, color=cls_clrs["Not Mangroves"])
ax2.set_title("Not Mangroves")
ax2.set_ylim(0.75, 1)

ax3.plot(culm_n_pts_lst, mng_nmng_f1_scr, color=cls_clrs["Mangroves > Not Mangroves"])
ax3.set_title("Mangroves > Not Mangroves")
ax3.set_ylim(0, 1)

ax4.plot(culm_n_pts_lst, nmng_mng_f1_scr, color=cls_clrs["Not Mangroves > Mangroves"])
ax4.set_title("Not Mangroves > Mangroves")
ax4.set_ylim(0, 1)

fig.suptitle("f1-score with increasing samples.")
fig.supxlabel("n samples")
fig.supylabel("f1-score")
plt.tight_layout()
plt.savefig("f1-score_increase_samples.pdf")


fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 10), sharex=True, sharey=False)

ax1.plot(culm_n_pts_lst, mng_n_pts, color=cls_clrs["Mangroves"])
ax1.set_title("Mangroves")
#ax1.set_ylim(0.75, 1)

ax2.plot(culm_n_pts_lst, nmng_n_pts, color=cls_clrs["Not Mangroves"])
ax2.set_title("Not Mangroves")
#ax2.set_ylim(0.75, 1)

ax3.plot(culm_n_pts_lst, mng_nmng_n_pts, color=cls_clrs["Mangroves > Not Mangroves"])
ax3.set_title("Mangroves > Not Mangroves")
#ax3.set_ylim(0, 1)

ax4.plot(culm_n_pts_lst, nmng_mng_n_pts, color=cls_clrs["Not Mangroves > Mangroves"])
ax4.set_title("Not Mangroves > Mangroves")
#ax4.set_ylim(0, 1)

fig.suptitle("Support with increasing samples.")
fig.supxlabel("n samples")
fig.supylabel("Support")
plt.tight_layout()
plt.savefig("support_increase_samples.pdf")

fig, ax = plt.subplots(figsize=(10, 10))

ax.plot(culm_n_pts_lst, acc_stats_dict["Overall"], color="black")
ax.set_title("Overall Accuracy")
ax.set_ylim(0.9, 1)
fig.supylabel("%")
plt.tight_layout()
plt.savefig("overall_accuracy_increase_samples.pdf")