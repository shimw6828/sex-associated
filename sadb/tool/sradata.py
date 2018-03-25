import pymongo
import argparse,os
import numpy as np
import pandas as pd
client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client.sadb
db.authenticate('sadb_admin','123456789',mechanism='SCRAM-SHA-1')


def import_gene_info(inputfile, Taxon_id):
    SRA = inputfile.split("/")[-1].split(".")[0]
    tax_list = pd.read_csv("/home/zhangna/SAdatabase/result/ensembl/Species_whole.csv",index_col="Taxon ID",dtype={'index':np.int})
    if Taxon_id not in tax_list.index:
        print "Wrong scientific name, the input not exit in the Species_whole.csv"
    with open(inputfile) as reader:
        header=reader.readline().strip().split(',')
        for line in reader:
            fields = line.rstrip("\n").split(",")
            record = dict(zip(header,fields))
            for k in record:
                if k in ["baseMean","log2FoldChange","lfcSE","stat","pvalue","padj"]:
                    record[k] = float(record[k])
            record["SRA_ID"]=SRA
            record["Scientific_name"] = tax_list.loc[Taxon_id,'Scientific name']
            record["Common_name"] = tax_list.loc[Taxon_id,'Common name']
            record["Taxon_id"] = Taxon_id
            db.total_result.insert_one(record)



if __name__ =="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--inputfile", help="the input file you give,must be csv file", type=str)
    parser.add_argument("-t", "--Taxonomy", help="give the taxonomy Scientific name", type=int)
    args = parser.parse_args()
    inputfile = args.inputfile
    Taxon_id= args.Taxonomy


    import_gene_info(inputfile, Taxon_id)