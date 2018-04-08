import urllib,urllib2
import sys,pymongo
client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client.sadb
db.authenticate('sadb_admin','123456789',mechanism='SCRAM-SHA-1')
url = 'http://www.uniprot.org/uploadlists/'

def main():
    with open("/opt/shimw/github/sex-associated/sadb/static/file/uniprot links.csv","r") as drugs:
        header=drugs.readline().strip().split(",")
        header=["DrugBank_ID","Drug_name","Type","UniProt ID","UniProt_Name","ensembl_gene_id"]
        for drug in drugs:
            fields = drug.rstrip("\n").split(",")
            params = {
                'from': 'ACC',
                'to': 'ENSEMBL_ID',
                'format': 'tab',
                'query': fields[3]
            }
            data = urllib.urlencode(params)
            request = urllib2.Request(url, data)
            contact = ""  # Please set your email address here to help us debug in case of problems.
            request.add_header('User-Agent', 'Python %s' % contact)
            response = urllib2.urlopen(request)
            page = response.read()
            if len(page.split("\n"))>3:
                print(drug)
            ensembl_id=page.split("\n")[1].split("\t")[1]
            fields.append(ensembl_id)
            record = dict(zip(header, fields))
            db.drug_info.insert_one(record)

if __name__ =="__main__":
    main()
