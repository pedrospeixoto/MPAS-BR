#!/bin/bash
#
# bash-shell script to download selected files from rda.ucar.edu using Wget
# NOTE: if you want to run under a different shell, make sure you change
#       the 'set' commands according to your shell's syntax
# after you save the file, don't forget to make it executable
#   i.e. - "chmod 755 <name_of_script>"
#
# Experienced Wget Users: add additional command-line flags here
#   Use the -r (--recursive) option with care
opts="-N"
#
cert_opt=""
# If you get a certificate verification error (version 1.10 or higher),
# uncomment the following line:
#set cert_opt = "--no-check-certificate"
#
# download the file(s)

# year and month of dates
yearmonth=$1

wget $cert_opt $opts https://data.rda.ucar.edu/d633000/e5.oper.an.sfc/${yearmonth}/e5.oper.an.sfc.128_031_ci.ll025sc.${yearmonth}0100_${yearmonth}3123.nc
wget $cert_opt $opts https://data.rda.ucar.edu/d633000/e5.oper.an.sfc/${yearmonth}/e5.oper.an.sfc.128_034_sstk.ll025sc.${yearmonth}0100_${yearmonth}3123.nc
wget $cert_opt $opts https://data.rda.ucar.edu/d633000/e5.oper.an.sfc/${yearmonth}/e5.oper.an.sfc.128_039_swvl1.ll025sc.${yearmonth}0100_${yearmonth}3123.nc
wget $cert_opt $opts https://data.rda.ucar.edu/d633000/e5.oper.an.sfc/${yearmonth}/e5.oper.an.sfc.128_040_swvl2.ll025sc.${yearmonth}0100_${yearmonth}3123.nc
wget $cert_opt $opts https://data.rda.ucar.edu/d633000/e5.oper.an.sfc/${yearmonth}/e5.oper.an.sfc.128_041_swvl3.ll025sc.${yearmonth}0100_${yearmonth}3123.nc
wget $cert_opt $opts https://data.rda.ucar.edu/d633000/e5.oper.an.sfc/${yearmonth}/e5.oper.an.sfc.128_042_swvl4.ll025sc.${yearmonth}0100_${yearmonth}3123.nc
wget $cert_opt $opts https://data.rda.ucar.edu/d633000/e5.oper.an.sfc/${yearmonth}/e5.oper.an.sfc.128_134_sp.ll025sc.${yearmonth}0100_${yearmonth}3123.nc
wget $cert_opt $opts https://data.rda.ucar.edu/d633000/e5.oper.an.sfc/${yearmonth}/e5.oper.an.sfc.128_139_stl1.ll025sc.${yearmonth}0100_${yearmonth}3123.nc
wget $cert_opt $opts https://data.rda.ucar.edu/d633000/e5.oper.an.sfc/${yearmonth}/e5.oper.an.sfc.128_141_sd.ll025sc.${yearmonth}0100_${yearmonth}3123.nc
wget $cert_opt $opts https://data.rda.ucar.edu/d633000/e5.oper.an.sfc/${yearmonth}/e5.oper.an.sfc.128_151_msl.ll025sc.${yearmonth}0100_${yearmonth}3123.nc
wget $cert_opt $opts https://data.rda.ucar.edu/d633000/e5.oper.an.sfc/${yearmonth}/e5.oper.an.sfc.128_165_10u.ll025sc.${yearmonth}0100_${yearmonth}3123.nc
wget $cert_opt $opts https://data.rda.ucar.edu/d633000/e5.oper.an.sfc/${yearmonth}/e5.oper.an.sfc.128_166_10v.ll025sc.${yearmonth}0100_${yearmonth}3123.nc
wget $cert_opt $opts https://data.rda.ucar.edu/d633000/e5.oper.an.sfc/${yearmonth}/e5.oper.an.sfc.128_167_2t.ll025sc.${yearmonth}0100_${yearmonth}3123.nc
wget $cert_opt $opts https://data.rda.ucar.edu/d633000/e5.oper.an.sfc/${yearmonth}/e5.oper.an.sfc.128_168_2d.ll025sc.${yearmonth}0100_${yearmonth}3123.nc
wget $cert_opt $opts https://data.rda.ucar.edu/d633000/e5.oper.an.sfc/${yearmonth}/e5.oper.an.sfc.128_170_stl2.ll025sc.${yearmonth}0100_${yearmonth}3123.nc
wget $cert_opt $opts https://data.rda.ucar.edu/d633000/e5.oper.an.sfc/${yearmonth}/e5.oper.an.sfc.128_183_stl3.ll025sc.${yearmonth}0100_${yearmonth}3123.nc
wget $cert_opt $opts https://data.rda.ucar.edu/d633000/e5.oper.an.sfc/${yearmonth}/e5.oper.an.sfc.128_235_skt.ll025sc.${yearmonth}0100_${yearmonth}3123.nc
wget $cert_opt $opts https://data.rda.ucar.edu/d633000/e5.oper.an.sfc/${yearmonth}/e5.oper.an.sfc.128_236_stl4.ll025sc.${yearmonth}0100_${yearmonth}3123.nc
wget $cert_opt $opts https://data.rda.ucar.edu/d633000/e5.oper.an.sfc/${yearmonth}/e5.oper.an.sfc.128_033_rsn.ll025sc.${yearmonth}0100_${yearmonth}3123.nc
