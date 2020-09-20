#!/bin/bash

sudo tcpdump -n -i <interface> tcp -w /tmp/report.pcap

tshark -r sender.pcap -Y " tcp.flags==0x010 && ip.addr==172.23.90.1" -T fields -E separator=/s -e ip.dst -e tcp.seq > sequence_numbers.log

gnuplot << EOF


set terminal postscript eps color

set xlabel "time (seconds)"
set ylabel "packets"

set output "file_name . eps"

set datafile separator ’,’


plot "datei_1.log" using 1:7 with lines title " test 1" , \
plot "datei_2.log" using :2 with lines title " test 2"
EOF