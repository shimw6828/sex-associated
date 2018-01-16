import sys,pymongo
client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client.sadb
db.authenticate('sadb_admin','123456789',mechanism='SCRAM-SHA-1')

input_file = sys.argv[1]
def import_gene_info():
    with open(input_file) as reader:
        header=reader.readline().strip().split(',')
        for line in reader:
            fields = line.rstrip("\n").split(",")
            record = dict(zip(header,fields))
            for k in record:
                if k in ["baseMean","log2FoldChange","lfcSE","stat","pvalue","padj"]:
                    record[k] = float(record[k])
            db.SRP062329.insert_one(record)

if __name__ =="__main__":
    import_gene_info()