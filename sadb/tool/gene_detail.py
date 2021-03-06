from pybiomart import Server
from pybiomart import Dataset
import pymongo
import argparse,os
import pandas as pd

client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client.sadb
db.authenticate('sadb_admin','123456789',mechanism='SCRAM-SHA-1')

def import_gene_info(Taxon_id):
    gene_info= pd.read_csv("/opt/shimw/"+str(Taxon_id)+"gene_detail.csv").fillna("")

    for i in gene_info['ensembl_gene_id']:
        detail=gene_info.loc[gene_info['ensembl_gene_id']==i]
        record={'ensembl_gene_id':detail['ensembl_gene_id'].values[0],
                'start_position':detail['start_position'].values[0],
                'end_position':detail['end_position'].values[0],
                'external_gene_name':detail['external_gene_name'].values[0],
                'description':detail['description'].values[0],
                'gene_biotype':detail['gene_biotype'].values[0],
                'chromosome_name':detail['chromosome_name'].values[0],
                'entrezgene':detail['entrezgene'].values[0],
                'hgnc_id':detail['hgnc_id'].values[0]
                }
        record['Taxonomy_Id']=Taxon_id
        db.gene_detail.insert_one(record)
    os.remove("/opt/shimw/"+str(Taxon_id)+"gene_detail.csv")
    print("detail put in")

def import_gene_structures(Taxon_id):
    Transcripts=pd.read_csv("/opt/shimw/"+str(Taxon_id)+"gene_structures.csv").fillna("")
    exons=pd.read_csv("/opt/shimw/"+str(Taxon_id)+"Transcript_exon.csv").fillna("")
    for ensembl_gene_id in Transcripts['ensembl_gene_id'].drop_duplicates():
        structures=Transcripts.loc[Transcripts['ensembl_gene_id']==ensembl_gene_id]
        records=[]
        for Transcript in structures.index:
            record = dict(structures.ix[Transcript])
            del record['ensembl_gene_id']
            record['exons'] = get_exon(exons.loc[exons['ensembl_transcript_id']==record["ensembl_transcript_id"]])
            records.append(record)
        result={"ensembl_gene_id":ensembl_gene_id,"Transcripts":records}
        db.gene_structures.insert_one(result)

    os.remove("/opt/shimw/"+str(Taxon_id)+"gene_structures.csv")
    os.remove("/opt/shimw/"+str(Taxon_id)+"Transcript_exon.csv")
    print("structures put in")

def import_Proteins(Taxon_id):
    Proteins=pd.read_csv("/opt/shimw/"+str(Taxon_id)+"gene_Protein.csv").fillna("")
    for ensembl_gene_id in Proteins['ensembl_gene_id'].drop_duplicates():
        proteins=Proteins.loc[Proteins['ensembl_gene_id']==ensembl_gene_id]
        records=[]
        for i in proteins.index:
            protein = dict(proteins.ix[i])
            del protein["ensembl_gene_id"]
            records.append(protein)
        result = {"ensembl_gene_id": ensembl_gene_id, "Proteins": records}
        db.proteins.insert_one(result)
    os.remove("/opt/shimw/"+str(Taxon_id)+"gene_Protein.csv")
    print("Protein put in")

def import_go_terms(Taxon_id):
    go_terms=pd.read_csv("/opt/shimw/"+str(Taxon_id)+"go_term.csv")
    go_terms=go_terms.dropna(subset=["go_id"]).fillna("")
    for ensembl_gene_id in go_terms['ensembl_gene_id'].drop_duplicates():
        go_term=go_terms.loc[go_terms['ensembl_gene_id']==ensembl_gene_id]
        records = []
        for i in go_term.index:
            record=dict(go_term.ix[i])
            del record["ensembl_gene_id"]
            records.append(record)
        result={"ensembl_gene_id":ensembl_gene_id,"go_terms":records}
        db.go_terms.insert_one(result)
    os.remove("/opt/shimw/"+str(Taxon_id)+"go_term.csv")
    print("go_term put in")

def import_gene_phenotype(Taxon_id):
    if os.path.exists("/opt/shimw/"+str(Taxon_id)+"gene_phenotype.csv"):
        gene_phenotypes=pd.read_csv("/opt/shimw/"+str(Taxon_id)+"gene_phenotype.csv")
        gene_phenotypes=gene_phenotypes.dropna(subset=["phenotype_description"]).fillna("")
        for i in gene_phenotypes.index:
            gene_phenotype = gene_phenotypes.loc[i]
            record = {'ensembl_gene_id': gene_phenotype['ensembl_gene_id'],
                      'phenotype_description': gene_phenotype['phenotype_description'],
                      'study_external_id': gene_phenotype['study_external_id'],
                      'source_name': gene_phenotype['source_name']
                      }
            db.phenotype.insert_one(record)
        os.remove("/opt/shimw/"+str(Taxon_id)+"gene_phenotype.csv")
        print("phenotype put in")

def import_pathway(Taxon_id):
    if os.path.exists("/opt/shimw/"+str(Taxon_id)+"gene_pathway.csv"):
        gene_pathways=pd.read_csv("/opt/shimw/"+str(Taxon_id)+"gene_pathway.csv")
        gene_pathways=gene_pathways.dropna(subset=["kegg_enzyme"]).fillna("")
        for i in gene_pathways.index:
            record =dict(gene_pathways.ix[i])
            db.pathway.insert_one(record)
        os.remove("/opt/shimw/"+str(Taxon_id)+"gene_pathway.csv")
        print("pathway put in")

def import_paralogue(Taxon_id):
    paralogues=pd.read_csv("/opt/shimw/"+str(Taxon_id)+"gene_paralogue.csv").dropna(subset=["paralog_ensembl_gene"]).fillna("")
    paralogues_g=paralogues.groupby('ensembl_gene_id')
    for i in paralogues_g.groups:
        paralogue=list(paralogues.loc[paralogues_g.groups[i].values]['paralog_ensembl_gene'])
        if pd.isnull(list(paralogues.loc[paralogues_g.groups[i].values]['paralog_ensembl_gene'])[0]):
            continue
        paralog=get_paralog(paralogue)
        record = {'ensembl_gene_id': i,
                  'paralog_ensembl_gene': paralog
                  }
        db.paralogue.insert_one(record)
    os.remove("/opt/shimw/"+str(Taxon_id)+"gene_paralogue.csv")
    print("paralogue put in")

def import_homolog(Taxon_id):
    homologs=pd.read_csv("/opt/shimw/"+str(Taxon_id)+"gene_homolog.csv").dropna(subset=["ortholog"]).fillna("")
    homologs_g=homologs.groupby('ensembl_gene_id')
    for i in homologs_g.groups:
        homolog=homologs.loc[homologs_g.groups[i].values]
        homo=get_homolog(homolog)
        record={'ensembl_gene_id':i,'homologs':homo}
        db.homolog.insert_one(record)
    os.remove("/opt/shimw/"+str(Taxon_id)+"gene_homolog.csv")
    print("homolog put in")


def get_exon(df):
    exons=[]
    for j in df.index:
        exon=dict(df.ix[j])
        del exon['ensembl_transcript_id']
        exons.append(exon)
    return exons
def get_paralog(list):
    paralog=[]
    for i in list:
        paralog.append({'paralog_ensembl_gene':i})
    return paralog

def get_homolog(df):
    homologs=[]
    for j in df.index:
        homo=dict(df.ix[j])
        del homo['ensembl_gene_id']
        homologs.append(homo)
    return homologs

if __name__ =="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--Taxonomy", help="give the taxonomy Scientific name", type=int)
    args = parser.parse_args()
    Taxon_id= args.Taxonomy
    import_gene_info(Taxon_id)
    import_gene_structures(Taxon_id)
    import_Proteins(Taxon_id)
    import_go_terms(Taxon_id)
    import_gene_phenotype(Taxon_id)
    import_pathway(Taxon_id)
    import_paralogue(Taxon_id)
    import_homolog(Taxon_id)
















