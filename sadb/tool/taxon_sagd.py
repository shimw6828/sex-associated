import pymongo
import argparse,os
import numpy as np
import pandas as pd
client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client.sadb
db.authenticate('sadb_admin','123456789',mechanism='SCRAM-SHA-1')

def import_gene_info(inputfile):
    sagd_id = inputfile.split("/")[-1].split(".")[0]
    sign_gene=[]
    data=pd.read_csv("/home/zhangna/SAdatabase/result/SAG_Statistics.csv")
    with open(inputfile) as reader:
        header=reader.readline().strip().split(',')
        header=["gene_ID","baseMean","log2FoldChange","lfcSE","stat","pvalue","padj","FPKM_M","FPKM_F"]
        for i in ["first","second","third"]:
            fields=reader.readline().rstrip("\n").split(",")
            record = dict(zip(header, fields))
            info=db.gene_detail.find_one({"ensembl_gene_id": record["gene_ID"]})
            symbol=info["external_gene_name"]
            sign_gene.append({"ensembl_gene_id":info["ensembl_gene_id"],
                              "symbol":symbol,
                              "padj":float("{0:.5}".format(float(record["padj"]))),
                              "log2FoldChange":float("{0:.5}".format(float(record["log2FoldChange"])))})

        sagd_info = db.sagd_id.find_one({"sagd_id": sagd_id})
        if sign_gene[0]["log2FoldChange"]>0:
            background="#f4fbfd"
        elif sign_gene[0]["log2FoldChange"]<0:
            background = "#fff6f8"
        elif sign_gene[0]["log2FoldChange"]==0:
            background="#f5f4f459"
        sag_num = data.loc[data["sagd_id"] == sagd_id]["SAG_NUM"].values[0]
        item={"sagd_id":sagd_id,
               "Scientific_name":sagd_info['Scientific_name'],
               "Common_name":sagd_info['Common_name'],
               "Taxonomy_ID":sagd_info["Taxonomy_ID"],
              "Tissue": sagd_info['Tissue'],
              "Stage": sagd_info['Stage'],
              "SRA_Study": sagd_info['SRA_Study'],
               "significant_gene":sign_gene,
              "background":background,
              "sag_num":sag_num}
        db.taxon_sagd.insert_one(item)

if __name__ =="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inputfile", help="the input file you give,must be csv file", type=str)
    args = parser.parse_args()
    inputfile = args.inputfile
    import_gene_info(inputfile)



