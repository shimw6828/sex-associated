import pymongo
import argparse,os
import numpy as np
import pandas as pd
client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client.sadb
db.authenticate('sadb_admin','123456789',mechanism='SCRAM-SHA-1')


def import_gene_info(inputfile, Taxon_id):
    basename = inputfile.split("/")[-1].split(".")[0].split("+")
    SRP=basename[0]
    SRX_T=""
    for srx in basename[1].split("_"):
        SRX_T=SRX_T+srx+" "
    SRX_T=SRX_T.strip(" ")
    SRX_O = ""
    for srx in basename[2].split("_"):
        SRX_O=SRX_O+srx+" "
    SRX_O = SRX_O.strip(" ")
    tax_list = pd.read_csv("/home/zhangna/SAdatabase/result/ensembl/Species_whole.csv",index_col="Taxon ID",dtype={'index':np.int})
    tissue_list=pd.read_csv("/opt/shimw/SRR_select_result311_human_end.csv",index_col="SRA_Experiment")
    if Taxon_id not in tax_list.index:
        print "Wrong scientific name, the input not exit in the Species_whole.csv"
        os._exit(0)
    if db.gene_detail.find_one({"Taxonomy_Id":Taxon_id})==None:
        print("gene detail not in our db")
        os._exit(0)
    Scientific_name=tax_list.loc[Taxon_id,'Scientific name']
    Common_name=tax_list.loc[Taxon_id, 'Common name']
    tissue=tissue_list.loc[basename[1].split("_")[0],"Tissue"]
    if tissue=="Testis":
        tissue="gonad"
    with open(inputfile) as reader:
        header=reader.readline().strip().split(',')
        for line in reader:
            fields = line.rstrip("\n").split(",")
            record = dict(zip(header,fields))
            for k in record:
                if k in ["baseMean","log2FoldChange","lfcSE","stat","pvalue","padj"]:
                    if record[k]!="NA":
                        record[k] = float(record[k])
            record["SRP_ID"]=SRP
            record["SRX_T"]=SRX_T
            record["SRX_O"] = SRX_O
            record["Scientific_name"] = Scientific_name
            record["Common_name"] = Common_name
            record["tissue"]=tissue
            record["Taxon_id"] = Taxon_id
            gene_detial=db.gene_detail.find_one({"ensembl_gene_id":record["gene_ID"]})
            if not gene_detial:
                print(record["gene_ID"])
                continue
            record["external_gene_name"]=gene_detial["external_gene_name"]
            record["entrezgene"]=gene_detial["entrezgene"]
            record["chromosome_name"]=gene_detial["chromosome_name"]
            db.total_result.insert_one(record)



if __name__ =="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--inputfile", help="the input file you give,must be csv file", type=str)
    parser.add_argument("-t", "--Taxonomy", help="give the taxonomy Scientific name", type=int)
    args = parser.parse_args()
    inputfile = args.inputfile
    Taxon_id= args.Taxonomy


    import_gene_info(inputfile, Taxon_id)