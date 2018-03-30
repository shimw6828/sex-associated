import sys,pymongo,numpy
import argparse,os
client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client.sadb
db.authenticate('sadb_admin','123456789',mechanism='SCRAM-SHA-1')

Taxon_id=7918
page = 1
per_page = 20
record_skip = (page - 1) * per_page
condition={}
condition["Taxon_id"]=Taxon_id
filter="klh"
condition["$or"]=[{"external_gene_name":"/"+filter+"/"},{"chromosome_name":"/"+filter+"/"}]



results=list(db.total_result.find(condition).skip(record_skip).limit(per_page))
gene_list_count = db.total_result.find(condition).count()
gene_list=[]

for result in results:
    gene_detail=db.gene_detail.find_one({"ensembl_gene_id":result["gene_ID"]})
    result["external_gene_name"]=gene_detail["external_gene_name"]
    result["chromosome_name"]=gene_detail["chromosome_name"]
    if result["external_gene_name"]==float("nan"):
    gene_list.append(result)

db.total_result.aggregate([{
    {"$match":}
}])