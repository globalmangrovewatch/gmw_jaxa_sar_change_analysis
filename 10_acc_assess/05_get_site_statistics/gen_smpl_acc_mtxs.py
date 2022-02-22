import rsgislib.tools.utils
import numpy




def create_row(row_len, prim_idx, prim_rng, np_rng):
    out_row_arr = numpy.zeros(row_len, dtype=int)
    vals = numpy.arange(prim_rng[0], prim_rng[1], 1)
    prim_val = np_rng.choice(vals)
    out_row_arr[prim_idx] = prim_val

    idxs = numpy.arange(0, row_len, 1)
    np_rng.shuffle(idxs)
    idxs = numpy.delete(idxs, numpy.where(idxs == prim_idx))

    for i in range(row_len-1):
        idx = idxs[i]
        if i == (row_len-2):
            out_row_arr[idx] = 100 - out_row_arr.sum()
        elif idx != prim_idx:
            pos_rng = 100 - out_row_arr.sum()
            vals = numpy.arange(0, pos_rng, 1)
            out_row_arr[idx] = np_rng.choice(vals)

    return out_row_arr.tolist()


np_rng = numpy.random.default_rng()#seed=42)

mng = [80, 95]
nmng = [80, 95]
m_nm = [50, 90]
nm_m = [50, 90]



expl_err_mtxs = dict()

for i in range(250):
    mtx = [
        create_row(4, 0, mng, np_rng),
        create_row(4, 1, nmng, np_rng),
        create_row(4, 2, m_nm, np_rng),
        create_row(4, 3, nm_m, np_rng),
    ]
    expl_err_mtxs[i] = mtx

#import pprint
#pprint.pprint(expl_err_mtxs)

rsgislib.tools.utils.write_dict_to_json(expl_err_mtxs, "ref_smpl_acc_set.json")
