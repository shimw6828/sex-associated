import pymongo
import argparse,os
import numpy as np
import pandas as pd
client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client.sadb
db.authenticate('sadb_admin','123456789',mechanism='SCRAM-SHA-1')

def import_gene_info(inputfile):
    sagd_id = inputfile.split("/")[-1].split(".")[0]
    sagd_info = db.sagd_id.find_one({"sagd_id": sagd_id})
    Scientific_name=sagd_info['Scientific_name']
    Common_name=sagd_info['Common_name']
    Taxon_id=sagd_info["Taxonomy_ID"]
    collection_name=Scientific_name.split()[0][0]+"_"+Scientific_name.split()[1]
    with open(inputfile) as reader:
        header=reader.readline().strip().split(',')
        header=["gene_ID","baseMean","log2FoldChange","lfcSE","stat","pvalue","padj","FPKM_M","FPKM_F"]
        for line in reader:
            fields = line.rstrip("\n").split(",")
            record = dict(zip(header,fields))
            for k in record:
                if k in ["FPKM_F","log2FoldChange","lfcSE","FPKM_M","pvalue","padj"]:
                    if record[k]!="NA":
                        record[k] = float("{0:.5}".format(float(record[k])))

            record["sagd_id"]=sagd_id
            record["Scientific_name"] = Scientific_name
            record["Common_name"] = Common_name
            record["Taxon_id"] = Taxon_id
            gene_detial=db.gene_detail.find_one({"ensembl_gene_id":record["gene_ID"]})
            if not gene_detial:
                print(record["gene_ID"])
                continue
            record["external_gene_name"]=gene_detial["external_gene_name"]
            record["entrezgene"]=gene_detial["entrezgene"]
            record["chromosome_name"]=gene_detial["chromosome_name"]
            db[collection_name].insert_one(record)


if __name__ =="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inputfile", help="the input file you give,must be csv file", type=str)
    args = parser.parse_args()
    inputfile = args.inputfile
    import_gene_info(inputfile)


