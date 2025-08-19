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

# read yearmonth
yearmonth=$1

# read list of dates and download files for each of them
while read -r date; do
    wget $cert_opt $opts https://data.rda.ucar.edu/d633000/e5.oper.an.pl/${yearmonth}/e5.oper.an.pl.128_129_z.ll025sc.${date}00_${date}23.nc
    wget $cert_opt $opts https://data.rda.ucar.edu/d633000/e5.oper.an.pl/${yearmonth}/e5.oper.an.pl.128_130_t.ll025sc.${date}00_${date}23.nc
    wget $cert_opt $opts https://data.rda.ucar.edu/d633000/e5.oper.an.pl/${yearmonth}/e5.oper.an.pl.128_131_u.ll025uv.${date}00_${date}23.nc
    wget $cert_opt $opts https://data.rda.ucar.edu/d633000/e5.oper.an.pl/${yearmonth}/e5.oper.an.pl.128_132_v.ll025uv.${date}00_${date}23.nc
    wget $cert_opt $opts https://data.rda.ucar.edu/d633000/e5.oper.an.pl/${yearmonth}/e5.oper.an.pl.128_133_q.ll025sc.${date}00_${date}23.nc
    wget $cert_opt $opts https://data.rda.ucar.edu/d633000/e5.oper.an.pl/${yearmonth}/e5.oper.an.pl.128_157_r.ll025sc.${date}00_${date}23.nc
done
