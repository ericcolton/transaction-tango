#!/usr/bin/env python3

import os
import sys
import csv
import re
from typing import Tuple
from collections import namedtuple

kOutputFields = ["date", "desc", "amount_precise", "amount", "joint", "category", "percent"]
OutputRecord = namedtuple("OutputRecord", kOutputFields)

if __name__ == '__main__':
    print("reading amazon transaction HTML from STDIN. (Press ^d when complete.)")
    html = []
    for line in sys.stdin:
        html.append(line)
    print(''.join(html))
    exit()
    output_records = []
    with open(infile_name, 'r') as infile:
        csv_reader = csv.DictReader(infile)
        for row in csv_reader:
            output_record = process_record(parse_input_record(row))
            if output_record:
                output_records.append(output_record)

    output_records.reverse()
    outfile_name = infile_name.rstrip('.CSV')
    outfile_name += "_OUT.CSV"
    with open(outfile_name, 'w', newline='') as outfile:
        csv_writer = csv.DictWriter(outfile, fieldnames=kOutputFields)
        for output_record in output_records:
            csv_writer.writerow(output_record._asdict())
