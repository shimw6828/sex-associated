import eutils
import pandas as pd
import pymongo
import os
import argparse
client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client.sadb
db.authenticate('sadb_admin','123456789',mechanism='SCRAM-SHA-1')
def main(taxon):
    query=db.gene_detail.find({"entrezgene":{"$ne":float("nan")},"Taxonomy_Id":taxon},{"ensembl_gene_id":1,"entrezgene":1})
    for result in query:
        ec = eutils.Client()
        id=int(result["entrezgene"])
        gene=ec.efetch(db='gene',id=id)
        detail=gene.entrezgenes[0]
        summary = detail.summary
        synonyms=detail.synonyms
        record={'ensembl_gene_id':result["ensembl_gene_id"],'summary':summary,'synonyms':synonyms}
        db.summary.insert_one(record)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("Taxonomy", help="give the taxonomy Scientific name", type=int)
    args = parser.parse_args()
    taxon= args.Taxonomy
    main(taxon)


