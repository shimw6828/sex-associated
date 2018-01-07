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
            db.gene_info.insert_one(record)

if __name__ =="__main__":
    import_gene_info()