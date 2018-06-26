import sys,pymongo
import argparse,os
client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client.sadb
db.authenticate('sadb_admin','123456789',mechanism='SCRAM-SHA-1')



def import_id(inputfile):
    with open(inputfile,"r") as reader:
        header = reader.readline().strip().split(',')
        header = ["SRA_Run","SRA_Experiment","SRA_Study","Taxonomy_ID","Sex","Tissue","Stage","group","sagd_id","Scientific_name","Common_name"]
        for line in reader:
            fields = line.rstrip("\n").split(",")
            record = dict(zip(header, fields))
            db.sagd_id.insert_one(record)

if __name__ =="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inputfile", help="the input file you give,must be csv file", type=str)
    args = parser.parse_args()
    inputfile = args.inputfile
    import_id(inputfile)