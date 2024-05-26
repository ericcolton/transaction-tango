#!/usr/bin/env python3

import sys
import csv
import re
from typing import Tuple
from collections import namedtuple

kPatterns = {r"TRADER JOE'S": None}
kInputFields = ["date", "desc", "type", "amount"]
kOutputFields = ["date", "desc", "amount", "joint", "category", "percent"]

InputRecord = namedtuple("InputRecord", kInputFields)
OutputRecord = namedtuple("OutputRecord", kOutputFields)

def match_desc_pattern(input: InputRecord) -> Tuple[float, str, float]:
    for regex in kPatterns.keys():
        match = re.search(regex, input.desc)
        if match:
            print(f"{input.desc} matched {regex}")
            return True, {"joint": input, "category": "eric", "percent": 1}
    return False, None

def build_output_record(input: InputRecord) -> OutputRecord:
    output = {"date" : input.date, "desc" : input.desc, "amount": input.amount}
    did_match, match_dict = match_desc_pattern(input)
    if did_match:
        output.extend(match_dict)
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
    return InputRecord(row["Transaction Date"], row["Description"], row["Type"], -float(row["Amount"]))

if __name__ == '__main__':
    
    infile_name = "/Users/ecolton/Downloads/Chase7103_Activity20240411_20240510_20240525.CSV"
    outfile_name = infile_name
    outfile_name.rstrip('.CSV')
    outfile_name += "_OUT.CSV"

    with open(infile_name, 'r') as infile:
        with open(outfile_name, 'w', newline='') as outfile:
            csv_reader = csv.DictReader(infile)
            csv_writer = csv.DictWriter(outfile, fieldnames=["date", "desc", "amount", ""])
        
            for row in csv_reader:
                output_entry = process_record(parse_input_record(row))
                if output_entry:
                    csv_writer.writerow(output_entry)
