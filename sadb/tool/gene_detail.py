from pybiomart import Server
from pybiomart import Dataset
import pymongo
import argparse,os
import pandas as pd

client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client.sadb
db.authenticate('sadb_admin','123456789',mechanism='SCRAM-SHA-1')

def import_gene_info(Taxon_id):
    gene_info= pd.read_csv("/opt/shimw/gene_detail.csv")

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
    os.remove("/opt/shimw/gene_detail.csv")
    print("detail put in")

def import_gene_structures():
    Transcripts=pd.read_csv("/opt/shimw/gene_structures.csv")
    exons=pd.read_csv("/opt/shimw/Transcript_exon.csv")
    for Transcript in Transcripts['ensembl_transcript_id']:
        structures=Transcripts.loc[Transcripts['ensembl_transcript_id']==Transcript]
        record = {'ensembl_gene_id': structures['ensembl_gene_id'].values[0],
                  'ensembl_transcript_id': structures['ensembl_transcript_id'].values[0],
                  'start_position': structures['start_position'].values[0],
                  'end_position': structures['end_position'].values[0],
                  'transcript_length': structures['transcript_length'].values[0],
                  'ensembl_peptide_id': structures['ensembl_peptide_id'].values[0],
                  'transcript_start': structures['transcript_start'].values[0],
                  'transcript_end': structures['transcript_end'].values[0],
                  'cds_length': structures['cds_length'].values[0],
                  'uniprotsptrembl': structures['uniprotsptrembl'].values[0],
                  'transcript_biotype': structures['transcript_biotype'].values[0],
                  'exons': []
                  }
        list_exons = get_exon(exons.loc[exons['ensembl_transcript_id']==structures["ensembl_transcript_id"].values[0]])
        record['exons'] = list_exons
        db.gene_structures.insert_one(record)
    os.remove("/opt/shimw/gene_structures.csv")
    os.remove("/opt/shimw/Transcript_exon.csv")
    print("structures put in")

def import_Proteins():
    Proteins=pd.read_csv("/opt/shimw/gene_Protein.csv")
    for i in Proteins.index:
        protein_info=Proteins.loc[i]
        record={'ensembl_gene_id':protein_info['ensembl_gene_id'],
                'ensembl_peptide_id':protein_info['ensembl_peptide_id'],
                'pfam':protein_info['pfam'],
                'pfam_start':protein_info['pfam_start'],
                'pfam_end':protein_info['pfam_end']
                }
        db.proteins.insert_one(record)
    os.remove("/opt/shimw/gene_Protein.csv")
    print("Protein put in")

def import_go_terms():
    go_terms=pd.read_csv("/opt/shimw/go_term.csv")
    for i in go_terms.index:
        go_term=go_terms.loc[i]
        record={'ensembl_gene_id':go_term['ensembl_gene_id'],
                'go_id':go_term['go_id'],
                'name_1006':go_term['name_1006'],
                'go_linkage_type':go_term['go_linkage_type'],
                'namespace_1003':go_term['namespace_1003']
                }
        db.go_terms.insert_one(record)
    os.remove("/opt/shimw/go_term.csv")
    print("go_term put in")

def import_gene_phenotype():
    if os.path.exists("/opt/shimw/gene_phenotype.csv"):
        gene_phenotypes=pd.read_csv("/opt/shimw/gene_phenotype.csv")
        for i in gene_phenotypes.index:
            gene_phenotype = gene_phenotypes.loc[i]
            record = {'ensembl_gene_id': gene_phenotype['ensembl_gene_id'],
                      'phenotype_description': gene_phenotype['phenotype_description'],
                      'study_external_id': gene_phenotype['study_external_id'],
                      'source_name': gene_phenotype['source_name']
                      }
            db.phenotype.insert_one(record)
        os.remove("/opt/shimw/gene_phenotype.csv")
        print("phenotype put in")

def import_pathway():
    if os.path.exists("/opt/shimw/gene_pathway.csv"):
        gene_pathways=pd.read_csv("/opt/shimw/gene_pathway.csv")
        for i in gene_pathways.index:
            gene_pathway = gene_pathways.loc[i]
            record = {'ensembl_gene_id': gene_pathway['ensembl_gene_id'],
                      'kegg_enzyme': gene_pathway['kegg_enzyme']
                      }
            db.pathway.insert_one(record)
        os.remove("opt/shimw/gene_pathway.csv")
        print("pathway put in")

def import_paralogue():
    paralogues=pd.read_csv("/opt/shimw/gene_paralogue.csv")
    for i in paralogues.index:
        paralogue=paralogues.loc[i]
        record = {'ensembl_gene_id': paralogue['ensembl_gene_id'],
                  'paralog_ensembl_gene': paralogue['paralog_ensembl_gene']
                  }
        db.paralogue.insert_one(record)
    os.remove("/opt/shimw/gene_paralogue.csv")
    print("paralogue put in")

def import_homolog():
    homologs=pd.read_csv("/opt/shimw/gene_homolog.csv")
    for i in homologs.index:
        homolog=homologs.loc[i]
        record = {'ensembl_gene_id': homolog['ensembl_gene_id'],
                  'external_gene_name': homolog['external_gene_name'],
                  'ortholog': homolog['ortholog'],
                  'ortholog_external_gene_name': homolog['ortholog_external_gene_name'],
                  'homolog_perc_id': homolog['homolog_perc_id'],
                  'homolog_perc_id_r1': homolog['homolog_perc_id_r1'],
                  'homolog_wga_coverage': homolog['homolog_wga_coverage'],
                  'homolog_orthology_confidence': homolog['homolog_orthology_confidence']
                  }
        db.homolog.insert_one(record)
    os.remove("/opt/shimw/gene_homolog.csv")
    print("homolog put in")



def get_exon(df):
    exons=[]
    for j in df.index:
        exon={'ensembl_exon_id':df.ix[j]["ensembl_exon_id"],
             'exon_chrom_start':df.ix[j]["exon_chrom_start"],
              'exon_chrom_end':df.ix[j]["exon_chrom_end"]}
        exons.append(exon)
    return exons


if __name__ =="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--Taxonomy", help="give the taxonomy Scientific name", type=int)
    args = parser.parse_args()
    Taxon_id= args.Taxonomy
    import_gene_info(Taxon_id)
    import_gene_structures()
    import_Proteins()
    import_go_terms()
    import_gene_phenotype()
    import_pathway()
    import_paralogue()
    import_homolog()
















