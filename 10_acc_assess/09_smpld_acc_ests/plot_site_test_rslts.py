import os
import tqdm
from rsgislib.tools.utils import read_json_to_dict


def create_plot(ref_val, x_vals, clses, test_scrs, title, out_file, cls_colours, ref_line_clr=(0.0, 0.0, 0.0)):
    import matplotlib.pyplot as plt

    n_clses = len(clses)

    y_plt_usr_min = 0#usr_lower.min() - 5
    y_plt_usr_max = 1#usr_upper.max() + 5

    x_axs = 1
    y_axs = n_clses
    if n_clses == 4:
        x_axs = 2
        y_axs = 2
    elif n_clses > 4:
        x_axs = 3
        y_axs = round((n_clses / 3) + 0.5)

    print(f"Plot Shape: {x_axs} x {y_axs}")

    fig_x_size = 12 * x_axs
    fig_y_size = 6 * y_axs

    fig, axs = plt.subplots(
        x_axs, y_axs, figsize=(fig_x_size, fig_y_size), sharex=True, sharey=True
    )

    if x_axs > 1:
        axs_flat = list()
        for x in range(x_axs):
            for y in range(y_axs):
                axs_flat.append(axs[x][y])
    else:
        axs_flat = axs

    for j in range(n_clses):
        cls_name = clses[j]

        axs_flat[j].axhline(y=ref_val[cls_name], color=ref_line_clr, linestyle="-")
        axs_flat[j].plot(x_vals, test_scrs[cls_name], color=cls_colours[cls_name])
        axs_flat[j].set_title(cls_name)
        axs_flat[j].set_ylim(y_plt_usr_min, y_plt_usr_max)
    fig.suptitle(title)
    fig.supxlabel("n samples")
    fig.supylabel("%")
    plt.tight_layout()
    plt.savefig(out_file)

n_sites = [4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64, 68]

cls_lst = ["Mangroves", "Not Mangroves", "Mangroves > Not Mangroves", "Not Mangroves > Mangroves"]

ref_data_file = "../08_calc_ref_acc/ref_acc_stats.json"
ref_data = read_json_to_dict(ref_data_file)

ref_usr_accs = dict()
ref_prod_accs = dict()
for cls in cls_lst:
    ref_usr_accs[cls] = ref_data[cls]["recall"]
    ref_prod_accs[cls] = ref_data[cls]["precision"]

smpls = [1000, 2500, 5000, 10000, 15000, 20000, 25000, 30000, 40000, 50000, 75000, 100000]


cls_clrs = dict()
cls_clrs["Mangroves"] = [0.0, 1.0, 0.0]
cls_clrs["Not Mangroves"] = [0.2, 0.2, 0.2]
cls_clrs["Mangroves > Not Mangroves"] = [1.0, 0.0, 0.0]
cls_clrs["Not Mangroves > Mangroves"] = [0.0, 0.0, 1.0]

for n_site in tqdm.tqdm(n_sites):
    data_dir = f"./site_{n_site}_tests"
    base_file = f"sites_{n_site}"
    usr_accs = dict()
    prod_accs = dict()
    for cls in cls_lst:
        usr_accs[cls] = list()
        prod_accs[cls] = list()
    for smpl in smpls:
        smpl_data_file = os.path.join(data_dir, f"{base_file}_{smpl}.json")
        #print(smpl_data_file)
        smpl_data = read_json_to_dict(smpl_data_file)
        for cls in cls_lst:
            usr_accs[cls].append(smpl_data[cls]["recall"])
            prod_accs[cls].append(smpl_data[cls]["precision"])

    out_usr_plot = os.path.join("rslt_plots", f"{base_file}_usr_plot.png")
    create_plot(ref_usr_accs, smpls, cls_lst, usr_accs, f"User Accuracy: {n_site} Sites", out_usr_plot, cls_clrs)
    out_prod_plot = os.path.join("rslt_plots", f"{base_file}_prod_plot.png")
    create_plot(ref_prod_accs, smpls, cls_lst, prod_accs, f"Producers Accuracy: {n_site} Sites", out_prod_plot, cls_clrs)
