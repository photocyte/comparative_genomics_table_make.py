#! /usr/bin/python 
import argparse
import sys
import pandas

parser = argparse.ArgumentParser()
parser.add_argument('tsv1',type=str,help='The first TSV file')
parser.add_argument('tsv2',type=str,help='The second TSV file')
parser.add_argument('-o',type=str,default="test.xlsx",help='The path to the output file')
args = parser.parse_args()

##Initialize final dataframe / excel spreadsheet
COLUMNS_1=["SPECIES_1_ID","Predicted function","SPC_1_RANK","SPC_1_TPM","ORTHOGROUP"]
COLUMNS_2=["ORTHOGROUP","SPC_2_RANK","SPC_2_TPM","SPECIES_2_ID"]

df_1 = None
df_2 = None
i=0

sys.stderr.write("Loading TSV #1 records into memory...")
handle_1 = open(args.tsv1)
handle_2 = open(args.tsv2)
for line in handle_1.readlines():
    splitline = line.split("\t")
    subdict = dict()
    subdict["Predicted function"] = None
    subdict["SPC_1_RANK"] = int(splitline[0].strip())
    subdict["SPECIES_1_ID"] = splitline[1].strip()
    subdict["SPECIES_1_ID"] = subdict["SPECIES_1_ID"][:subdict["SPECIES_1_ID"].rfind("-PA")]
    subdict["SPC_1_TPM"] = float(splitline[2].strip())
    subdict["ORTHOGROUP"] = splitline[3].strip()
    if df_1 is None:
        df_1 = pandas.DataFrame(subdict,columns=COLUMNS_1,index=[i])
        i+=1
    else:
        df_1.loc[i] = subdict
        i+=1

sys.stderr.write("Loading TSV #2 records into memory...")
for line in handle_2.readlines():
    splitline = line.split("\t")
    subdict = dict()
    subdict["SPC_2_RANK"] = int(splitline[0].strip())
    subdict["SPECIES_2_ID"] = splitline[1].strip()
    subdict["SPECIES_2_ID"] = subdict["SPECIES_2_ID"][:subdict["SPECIES_2_ID"].rfind("-PA")]
    subdict["SPC_2_TPM"] = float(splitline[2].strip())
    subdict["ORTHOGROUP"] = splitline[3].strip()
    if df_2 is None:
        df_2 = pandas.DataFrame(subdict,columns=COLUMNS_2,index=[i])
        i+=1
    else:
        df_2.loc[i] = subdict
        i+=1

print(df_1)
print(df_2)

handle_1.close()
handle_2.close()

df_3 = df_1.merge(df_2,how='left',left_on='ORTHOGROUP',right_on='ORTHOGROUP')
df_3.to_excel(args.o)
