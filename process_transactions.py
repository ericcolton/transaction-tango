#!/usr/bin/env python3

import os
import sys
import csv
import re
from typing import Tuple
from collections import namedtuple

kDescPatterns = {r"TRADER JOE S": [0, 'grocery', 0.5],
                 r"WHOLEFDS": [0, 'grocery', 0.5],
                 r"Spectrum": [1, 'monthly', None],
                 r"ASSOCIATED MARKET": [0, 'grocery', 0.5],
                 r"SEBCO": [0, 'grocery', 0.5],
                 r"SEAMLSS": [0, 'grocery', 0.5],
                 r"CVS/PHARMACY": [1.0, 'drugstore', None],
                 r"U-HAUL MOVING": [1.0, 'monthly', None],
                 r"FOODTOWN": [0, 'grocery', 0.5],
}
kInputFields = ["date", "desc", "type", "amount_precise", "amount"]
kOutputFields = ["date", "desc", "amount_precise", "amount", "joint", "category", "percent"]

InputRecord = namedtuple("InputRecord", kInputFields)
OutputRecord = namedtuple("OutputRecord", kOutputFields)

def calc_joint(input: InputRecord, assign: list, regex: str) -> float:
    if len(assign) < 1:
        raise Exception(f"Malformed assignment for field 'joint' for pattern '{regex}'")
    elif (isinstance(assign[0], int) or isinstance(assign[0], float)) and assign[0] > 0:
        return assign[0] * input.amount
    return None

def calc_percent(assign: list, regex: str) -> float:
    if len(assign) < 3:
        raise Exception(f"Malformed assignment for field 'percent' for pattern '{regex}'")
    elif (isinstance(assign[2], int) or isinstance(assign[2], float)) and assign[2] > 0:
        return float(assign[2])
    return None

def match_desc_pattern(input: InputRecord) -> dict:
    for regex, assign in kDescPatterns.items():
        match = re.search(regex, input.desc)
        if match:
            return True, {"joint": calc_joint(input, assign, regex),
                          "category": assign[1],
                          "percent": calc_percent(assign, regex)
            }
    return False, None

def build_output_record(input: InputRecord) -> OutputRecord:
    output = {"date" : input.date,
              "desc" : input.desc,
              "amount": round(input.amount),
              "amount_precise": input.amount,
              }
    did_match, match_dict = match_desc_pattern(input)
    if did_match:
        output.update(match_dict)
    else:
        output["joint"] = None
        output["category"] = None
        output["percent"] = None
    return OutputRecord(**output)
 
def process_record(input: InputRecord) -> OutputRecord:
    if input.type == "Payment":
        return None
    elif input.type == "Sale" or input.type == "Return":
        return build_output_record(input)
    else:
        raise Exception(f"unexpected input record type: '{input.type}'")

def parse_input_record(row: dict) -> InputRecord:
    amount = -float(row["Amount"])
    return InputRecord(row["Transaction Date"], row["Description"], row["Type"], round(amount), amount)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception(f"no filename specified")
    infile_name = sys.argv[1]    
    if not os.path.isfile(infile_name) or not os.access(infile_name, os.R_OK):
        raise Exception(f"Filename '{infile_name}' is not readable")
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
