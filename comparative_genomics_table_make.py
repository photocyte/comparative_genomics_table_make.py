#! /usr/bin/python 
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('tsv1',type=str,help='The path to the fasta file to clean')
parser.add_argument('tsv2',type=str,help='The path to the fasta file to clean')
args = parser.parse_args()

sys.stderr.write("Loading TSV #1 records into memory...")
handle = open(args.tsv1)
for line in handle.readlines():
    print(line)
handle.close()

