for year in '1996' '2007' '2008' '2009' '2010' '2015' '2016' '2017' '2018' '2019' '2020'; do
    for tile in "N19E072" "N19E073" "N18E073" "N17E073" "N16E073" "N16E074" "N15E074" "N14E074" "N13E074" "N13E075" "N12E075" "N11E075" "N11E076" "N10E076" "N10E078" "N10E079" "N10E080" "N09E076" "N09E077" "N09E078" "N09E079" "N09E080"; do
        singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python ../../../00_utils/chk_imgs.py --nbands 1 --rmerr --chkproj --epsg 4326 --readimg --npxls 10  --printerrs --chksum -i "/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_mjr_${year}_v310/*${tile}*.kea"
    done
done

