#coding=utf-8
import flask_restful
import string
import json
from sadb import app, api
from sadb.core import mongo
from flask_restful import Resource, fields, marshal_with, reqparse, marshal
import pandas as pd
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


# sagd_id_fields={
#     "SRP_id":fields.String,
#     "SRX_O":fields.List(fields.String),
#     "SRX_T":fields.List(fields.String)
# }

gene_fields={
    'gene_ID':fields.String,
    'external_gene_name':fields.String,
    'sagd_id':fields.String,
    'FPKM_F':fields.String,
    'FPKM_M':fields.String,
    'chromosome_name':fields.String,
    'log2FoldChange':fields.Float,
    'padj':fields.Float,
    'Scientific_name':fields.String,
    'Common_name':fields.String
}

gene_list_fields={
    'gene_list': fields.List(fields.Nested(gene_fields)),
    'gene_list_count': fields.Integer
}
class search(Resource):
    @marshal_with(gene_list_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page',type=int,default=1)
        parser.add_argument('query', type=str)
        parser.add_argument('per_page', type=int, default=20)
        parser.add_argument('filter', type=str)
        parser.add_argument('update', type=str)
        parser.add_argument('padj', type=str)
        args = parser.parse_args()
        page = args['page']
        per_page = args['per_page']
        record_skip = (page - 1) * per_page
        condition = {}
        print(args['query'])

        if args['query']:
            condition["$or"]=[{"gene_ID":{"$regex": args["query"],"$options": "$i"}},
                              {"external_gene_name":{"$regex": args["query"],"$options": "$i"}},
                              {"chromosome_name":{"$regex": args["query"],"$options": "$i"}},
                              {"Tissue": {"$regex": args["query"], "$options": "$i"}},
                              {"Stage": {"$regex": args["query"], "$options": "$i"}}]
        # if args['min'] or args['max']:
        #     condition["padj"] = {"$gte": 0, "$lte": 1}
        # if args['min'] :
        #     print(args['min'])
        #     condition["padj"]["$gte"]= float(args['min'])
        # if args['max']:
        #     print(args['max'])
        #     condition["padj"]["$lte"] = float(args['max'])
        if args['padj']:
            if args['padj']!="":
                condition["padj"]={"$lt":float(args['padj'])}
                print(condition)



        results = list(mongo.db.total_result.find(condition).sort([('padj',1)]).skip(record_skip).limit(per_page))
        if args["update"]!="update":
            print(condition)
            gene_list_count = mongo.db.total_result.find(condition).count()
            print(gene_list_count)
        else:
            gene_list_count=0
        gene_list = []

        for result in results:
            if type(result["external_gene_name"])==float:
                result["external_gene_name"]=""
            gene_list.append(result)
        print(gene_list)
        return {"gene_list":gene_list,"gene_list_count":gene_list_count}

api.add_resource(search, '/api/search')

commne_name_fields={
    'Taxonomy_Id':fields.Integer,
    'Common_name': fields.String
}
class get_common_name(Resource):
    @marshal_with(commne_name_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('taxon_id', type=str)
        args = parser.parse_args()
        condition = {}
        condition['Taxonomy_Id'] = args['taxon_id']
        result=mongo.db.total_result.find_one(condition,{'Taxonomy_Id':1,'Common_name':1})
        return result

api.add_resource(get_common_name,'/api/get_common_name')


significant_fields={
    "log2FoldChange": fields.Float,
    "symbol": fields.String,
    "padj": fields.Float,
    "ensembl_gene_id": fields.String
}

taxon_sagd_fields={
    "significant_gene":fields.List(fields.Nested(significant_fields)),
    "sagd_id":fields.String,
    "Common_name":fields.String,
    "Tissue":fields.String,
    "Scientific_name":fields.String,
    "Taxonomy_ID":fields.String,
    "SRA_Study":fields.String,
    "background":fields.String,
    "Stage":fields.String,
    "sag_num":fields.String
}
taxonomy_fields={
    'sagd_list': fields.List(fields.Nested(taxon_sagd_fields)),
    'sagd_list_count': fields.Integer
}
class get_taxonomy_list(Resource):
    @marshal_with(taxonomy_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page',type=int,default=1)
        parser.add_argument('per_page', type=int, default=10)
        parser.add_argument('taxon_id', type=str)
        args = parser.parse_args()
        page = args['page']
        per_page = args['per_page']
        record_skip = (page - 1) * per_page
        condition = {}
        condition['Taxonomy_ID'] = str(args['taxon_id'])
        print(condition)
        sagd_list = list(mongo.db.taxon_sagd.find(condition).skip(record_skip).limit(per_page))
        sagd_list_count = mongo.db.taxon_sagd.find(condition).count()

        return {"sagd_list":sagd_list,"sagd_list_count":sagd_list_count}
api.add_resource(get_taxonomy_list,'/api/taxonomy_list')


get_detail_fields={
    'description':fields.String,
    'hgnc_id':fields.String,
    'ensembl_gene_id':fields.String,
    'start_position':fields.Integer,
    'Taxonomy_Id':fields.Integer,
    'end_position':fields.Integer,
    'entrezgene':fields.String,
    'gene_biotype':fields.String,
    'chromosome_name':fields.String,
    'external_gene_name':fields.String
}
class get_detail(Resource):
    @marshal_with(get_detail_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('gene', type=str)
        args = parser.parse_args()
        condition = {}
        condition["ensembl_gene_id"] = args['gene']
        detail=mongo.db.gene_detail.find_one(condition)
        ##the entrezgene is float with .0,so I change it in int
        if detail["entrezgene"] !="":
            detail["entrezgene"] = int(detail["entrezgene"])
        return detail
api.add_resource(get_detail,'/api/get_detail')


get_summary_fields={
    'synonyms':fields.String,
    'summary':fields.String
}
class get_summary(Resource):
    @marshal_with(get_summary_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('gene', type=str)
        args = parser.parse_args()
        condition = {}
        condition["ensembl_gene_id"] = args['gene']
        summary=mongo.db.summary.find_one(condition)
        if not summary:
            summary={'ensembl_gene_id':args['gene'] , 'synonyms': "", 'summary': None}
        else:
            synonyms=""
            for i in summary["synonyms"]:
                synonyms = synonyms + i +" "
            summary["synonyms"]=synonyms.encode()
        return summary

api.add_resource(get_summary,'/api/get_summary')

get_drug_info_fields={
    'DrugBank_ID':fields.String,
    'ensembl_gene_id':fields.String,
    "Drug_name": fields.String,
    'UniProt_Name': fields.String,
    'Type': fields.String,
    'UniProt ID': fields.String
}
class get_drug_info(Resource):
    @marshal_with(get_drug_info_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('gene', type=str)
        args = parser.parse_args()
        condition = {}
        condition["ensembl_gene_id"] = args['gene']
        drug_info=list(mongo.db.drug_info.find(condition))
        return drug_info
api.add_resource(get_drug_info,'/api/get_drug_info')


get_transcript_fields={
    "start_position":fields.String,
    "ensembl_transcript_id": fields.String,
    "transcript_biotype": fields.String,
    "ensembl_peptide_id": fields.String,
    "end_position": fields.String,
    "transcript_length": fields.String,
    "ensembl_gene_id": fields.String,
    "transcript_end" :fields.String,
    "transcript_start":fields.String,
    "cds_length":fields.String,
    "uniprotsptrembl":fields.String

}

get_gene_structures_fields={
    'transcript': fields.List(fields.Nested(get_transcript_fields)),
    'gene_model': fields.String
}
class get_gene_structures(Resource):
    @marshal_with(get_gene_structures_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('gene', type=str)
        args = parser.parse_args()
        condition = {}
        condition["ensembl_gene_id"] = args['gene']
        structures=mongo.db.gene_structures.find_one(condition)
        gene_start=structures["Transcripts"][0]["start_position"]
        gene_end=structures["Transcripts"][0]["end_position"]
        gene_length=gene_end-gene_start
        transcription = []
        for transcript in structures["Transcripts"]:
            transcription.append({"exon":transcript["exons"],"ensembl_transcript_id":transcript["ensembl_transcript_id"]})
        gap = gene_length / 10
        svgs = ''
        scale = '<svg width="980" height="30">\n'
        scale = scale + '<line x1="0" y1="50%" x2="800" y2="50%" style="stroke:rgb(255,0,0);stroke-width:2" />\n'
        scale = scale + '<line x1="0" y1="60%" x2="0" y2="40%" style="stroke:rgb(255,0,0);stroke-width:2" />\n'
        scale = scale + '<line x1="80" y1="60%" x2="80" y2="40%" style="stroke:rgb(255,0,0);stroke-width:2" />\n'
        scale = scale + '<line x1="160" y1="60%" x2="160" y2="40%" style="stroke:rgb(255,0,0);stroke-width:2" />\n'
        scale = scale + '<line x1="240" y1="60%" x2="240" y2="40%" style="stroke:rgb(255,0,0);stroke-width:2" />\n'
        scale = scale + '<line x1="320" y1="60%" x2="320" y2="40%" style="stroke:rgb(255,0,0);stroke-width:2" />\n'
        scale = scale + '<line x1="400" y1="60%" x2="400" y2="40%" style="stroke:rgb(255,0,0);stroke-width:2" />\n'
        scale = scale + '<line x1="480" y1="60%" x2="480" y2="40%" style="stroke:rgb(255,0,0);stroke-width:2" />\n'
        scale = scale + '<line x1="560" y1="60%" x2="560" y2="40%" style="stroke:rgb(255,0,0);stroke-width:2" />\n'
        scale = scale + '<line x1="640" y1="60%" x2="640" y2="40%" style="stroke:rgb(255,0,0);stroke-width:2" />\n'
        scale = scale + '<line x1="720" y1="60%" x2="720" y2="40%" style="stroke:rgb(255,0,0);stroke-width:2" />\n'
        scale = scale + '<line x1="800" y1="60%" x2="800" y2="40%" style="stroke:rgb(255,0,0);stroke-width:2" />\n'
        scale = scale + '<text x="0" y="8" font-family="Verdana" font-size="10">' + str(round(gene_start / 1000000.0, 2)) + 'Mb' + '</text>\n'
        scale = scale + '<text x="80" y="8" font-family="Verdana" font-size="10" text-anchor="middle">' + str(round((gene_start + gap * 1) / 1000000.0, 2)) + 'Mb' + '</text>\n'
        scale = scale + '<text x="160" y="8" font-family="Verdana" font-size="10" text-anchor="middle">' + str(round((gene_start + gap * 2) / 1000000.0, 2)) + 'Mb' + '</text>\n'
        scale = scale + '<text x="240" y="8" font-family="Verdana" font-size="10" text-anchor="middle">' + str(round((gene_start + gap * 3) / 1000000.0, 2)) + 'Mb' + '</text>\n'
        scale = scale + '<text x="320" y="8" font-family="Verdana" font-size="10" text-anchor="middle">' + str(round((gene_start + gap * 4) / 1000000.0, 2)) + 'Mb' + '</text>\n'
        scale = scale + '<text x="400" y="8" font-family="Verdana" font-size="10" text-anchor="middle">' + str(round((gene_start + gap * 5) / 1000000.0, 2)) + 'Mb' + '</text>\n'
        scale = scale + '<text x="480" y="8" font-family="Verdana" font-size="10" text-anchor="middle">' + str(round((gene_start + gap * 6) / 1000000.0, 2)) + 'Mb' + '</text>\n'
        scale = scale + '<text x="560" y="8" font-family="Verdana" font-size="10" text-anchor="middle">' + str(round((gene_start + gap * 7) / 1000000.0, 2)) + 'Mb' + '</text>\n'
        scale = scale + '<text x="640" y="8" font-family="Verdana" font-size="10" text-anchor="middle">' + str(round((gene_start + gap * 8) / 1000000.0, 2)) + 'Mb' + '</text>\n'
        scale = scale + '<text x="720" y="8" font-family="Verdana" font-size="10" text-anchor="middle">' + str(round((gene_start + gap * 9) / 1000000.0, 2)) + 'Mb' + '</text>\n'
        scale = scale + '<text x="800" y="8" font-family="Verdana" font-size="10" text-anchor="middle">' + str(round((gene_start + gap * 10) / 1000000.0, 2)) + 'Mb' + '</text>\n'
        scale = scale + '</svg>\n'
        svgs = svgs + scale
        for i in transcription:
            svg = '<svg width="980" height="10">\n'
            polylines='<line x1="0" y1="50%" x2="800" y2="50%" style="stroke:rgb(255,0,0);stroke-width:2" />\n'
            rects = '<g fill="#CDCD00">\n'
            for m in i['exon']:
                width = (m["exon_chrom_end"] - m["exon_chrom_start"]) / float(gene_length) * 800
                x = (m["exon_chrom_start"] - gene_start) / float(gene_length) * 800
                rect = '<rect x="' + str(x) + '" y="0" width="' + str(width) + '" height="10"></rect>\n'
                rects = rects + rect
            rects = rects + "</g>\n"
            text = '<text x="810" y="50%" dy=".3em" fill="black" font-size="12">' + i["ensembl_transcript_id"] + '</text>\n'
            svg = svg + polylines + rects + text + '</svg>\n'
            svgs = svgs + svg
        gene_structures={"transcript": structures["Transcripts"], "gene_model": svgs}
        return gene_structures
api.add_resource(get_gene_structures,'/api/get_gene_structures')


get_go_terms_fields={
    "go_linkage_type":fields.String,
    "namespace_1003":fields.String,
    "go_id": fields.String,
    "name_1006": fields.String
}
class get_go_terms(Resource):
    @marshal_with(get_go_terms_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('gene', type=str)
        args = parser.parse_args()
        condition = {}
        condition["ensembl_gene_id"] = args['gene']
        go_terms=mongo.db.go_terms.find_one(condition)
        if go_terms:
            return go_terms["go_terms"]
api.add_resource(get_go_terms,'/api/get_go_terms')


homolog_fields={
    "ortholog":fields.String,
    "homolog_perc_id_r1":fields.Float,
    "homolog_perc_id": fields.Float,
    "homolog_wga_coverage": fields.String,
    "ortholog_external_gene_name": fields.String,
    "external_gene_name": fields.String,
    "homolog_orthology_confidence": fields.String
}
get_homolog_fields={
    "homologs":fields.List(fields.Nested(homolog_fields)),
    "homolog_list":fields.Integer(default=0)
}
class get_homolog(Resource):
    @marshal_with(get_homolog_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('gene', type=str)
        args = parser.parse_args()
        condition = {}
        condition["ensembl_gene_id"] = args['gene']
        homolog=mongo.db.homolog.find_one(condition)
        if homolog:
            homolog_list=len(homolog['homologs'])
            return {"homologs":homolog['homologs'],"homolog_list":homolog_list}

api.add_resource(get_homolog,'/api/get_homolog')


paralogue_fields={
    "paralog_ensembl_gene":fields.String,
    'paralog_gene_name': fields.String,
    'paralog_gene_chromosome':fields.String,
    'paralog_gene_start':fields.Integer,
    'paralog_gene_end':fields.Integer,
    'external_gene_name': fields.String,
    'ensembl_gene_id':fields.String
}
get_paralogue_fields={
    'paralogue': fields.List(fields.Nested(paralogue_fields)),
    'para_list':fields.Integer(default=0)
}
class get_paralogue(Resource):
    @marshal_with(get_paralogue_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('gene', type=str)
        args = parser.parse_args()
        condition = {}
        condition["ensembl_gene_id"] = args['gene']
        result = mongo.db.paralogue.find_one(condition)
        if result:
            paralogue=[]
            para_list=len(result["paralog_ensembl_gene"])
            for i in result["paralog_ensembl_gene"]:
                k={}
                k["paralog_ensembl_gene"]=i["paralog_ensembl_gene"]
                paralog_gene=mongo.db.gene_detail.find_one({"ensembl_gene_id": k["paralog_ensembl_gene"]})
                k["paralog_gene_name"]=paralog_gene["external_gene_name"]
                k["paralog_gene_chromosome"]=paralog_gene['chromosome_name']
                k["paralog_gene_start"]=paralog_gene['start_position']
                k["paralog_gene_end"] = paralog_gene['end_position']
                k["ensembl_gene_id"]=condition["ensembl_gene_id"]
                k["external_gene_name"]=mongo.db.gene_detail.find_one({"ensembl_gene_id" :condition["ensembl_gene_id"]},{"external_gene_name":1})["external_gene_name"]
                paralogue.append(k)
            return {"paralogue":paralogue,"para_list":para_list}
api.add_resource(get_paralogue,'/api/get_paralogue')

get_proteins_fields={
    "pfam":fields.String,
    "pfam_end": fields.String,
    "pfam_start": fields.String,
    "ensembl_peptide_id": fields.String
}
class get_proteins(Resource):
    @marshal_with(get_proteins_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('gene', type=str)
        args = parser.parse_args()
        condition = {}
        condition["ensembl_gene_id"] = args['gene']
        proteins=mongo.db.proteins.find_one(condition)
        if proteins:
            return proteins["Proteins"]
api.add_resource(get_proteins,'/api/get_proteins')


get_result_fields={
    "stat":fields.String,
    "baseMean": fields.String,
    "Scientific_name": fields.String,
    "padj": fields.String,
    "gene_ID": fields.String,
    "external_gene_name": fields.String,
    "Taxon_id": fields.String,
    "entrezgene": fields.String,
    "lfcSE": fields.String,
    "log2FoldChange": fields.String,
    "Common_name": fields.String,
    "chromosome_name": fields.String,
    "pvalue": fields.String,
    "sagd_id": fields.String,
    "FPKM_M":fields.String,
    "FPKM_F":fields.String,
    "Tissue":fields.String,
    "Stage":fields.String

}
# "SRA":sagd_id_fields
get_analysis_fields={
    'analysis': fields.List(fields.Nested(get_result_fields)),
    'taxname': fields.String
}

class get_analysis(Resource):
    @marshal_with(get_analysis_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('gene', type=str)
        args = parser.parse_args()
        condition = {}
        condition["gene_ID"] = args['gene']
        analysis=list(mongo.db.total_result.find(condition))
        if analysis:
            x = []
            y = [1 for i in range(len(analysis))]
            log2foldchange = []
            padj = []
            for i in range(0,len(analysis)):
                x.append(analysis[i]["sagd_id"])
                analysis[i]["SRA"]=mongo.db.sagd_id.find_one({"sagd_id":analysis[i]["sagd_id"]})
                if analysis[i]["log2FoldChange"] > 5:
                    log2foldchange.append(5)
                elif analysis[i]["log2FoldChange"] < -5:
                    log2foldchange.append(-5)
                else:
                    log2foldchange.append(analysis[i]["log2FoldChange"])
                if analysis[i]['padj']>=0.5:
                    if analysis[i]['padj']=="NA":
                        padj.append(0)
                    else:
                        padj.append(-math.log10(0.5))
                elif analysis[i]['padj']<=0.0005:
                    padj.append(-math.log10(0.0005))
                else:
                    padj.append(-math.log10(analysis[i]['padj']))
            cmmap = plt.cm.get_cmap('RdYlBu')
            plt.style.use('ggplot')
            plt.scatter(range(len(x)), y, s=np.array(padj) * 300, c=log2foldchange, cmap=cmmap, alpha=0.8)
            plt.xticks(range(len(x)), x)
            plt.yticks([1], [condition["gene_ID"]])
            plt.ylim(ymin=0.8, ymax=1.2)
            plt.xlim(xmin=-1, xmax=len(analysis))
            plt.xticks(rotation=60)
            fig = plt.gcf()
            fig.set_size_inches(len(analysis), 2)
            fig.savefig('/opt/shimw/github/sex-associated/sadb/static/image/analysis/'+ condition["gene_ID"]+".png", bbox_inches="tight",dpi=80)
            plt.clf()
            taxname=analysis[0]["Scientific_name"].replace(" ","_").encode()
            return {"analysis":analysis,"taxname":taxname}
api.add_resource(get_analysis,'/api/analysis')

get_phenotypes_fields={
    "phenotype_description":fields.String,
    "study_external_id": fields.String,
    "source_name": fields.String
}
class get_phenotypes(Resource):
    @marshal_with(get_phenotypes_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('gene', type=str)
        args = parser.parse_args()
        condition = {}
        condition["ensembl_gene_id"] = args['gene']
        phenotypes=list(mongo.db.phenotype.find(condition))
        return phenotypes
api.add_resource(get_phenotypes,'/api/get_phenotypes')

get_sagdid_fields={
    "SRA_Run":fields.String,
    "Scientific_name":fields.String,
    "SRA_Study":fields.String,
    "sagd_id":fields.String,
    "Sex":fields.String,
    "SRA_Experiment":fields.String,
    "Tissue" :fields.String,
    "Taxonomy_ID":fields.String,
    "Stage":fields.String

}

class get_sagd_id(Resource):
    @marshal_with(get_sagdid_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('sagd_id', type=str)
        args = parser.parse_args()
        condition = {}
        condition["sagd_id"] = args['sagd_id']
        items=list(mongo.db.sagd_id.find(condition))
        return items
api.add_resource(get_sagd_id,'/api/get_sagd_id')

class get_sagd_id_info(Resource):
    @marshal_with(taxon_sagd_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('sagd_id', type=str)
        args = parser.parse_args()
        condition = {}
        condition["sagd_id"] = args['sagd_id']
        items=mongo.db.taxon_sagd.find_one(condition)
        return items
api.add_resource(get_sagd_id_info,'/api/get_sagd_id_info')


class get_sagd_list(Resource):
    @marshal_with(gene_list_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page',type=int,default=1)
        parser.add_argument('sagd_id', type=str)
        parser.add_argument('per_page', type=int, default=20)
        parser.add_argument('update', type=str)
        parser.add_argument('padj', type=str)

        args = parser.parse_args()
        page = args['page']
        per_page = args['per_page']
        record_skip = (page - 1) * per_page
        condition = {}
        condition["sagd_id"]=args['sagd_id']
        sagd_info=mongo.db.taxon_sagd.find_one(condition)
        collections=sagd_info["Scientific_name"].split()[0][0]+"_"+sagd_info["Scientific_name"].split()[1]

        if args['padj']:
            if args['padj']!="":
                condition["padj"]={"$lt":float(args['padj'])}

        results = list(mongo.db[collections].find(condition).skip(record_skip).limit(per_page))
        if args["update"]!="update":
            print(condition)
            gene_list_count = mongo.db[collections].find(condition).count()
            print(gene_list_count)
        else:
            gene_list_count=0
        gene_list = []

        for result in results:
            if type(result["external_gene_name"])==float:
                result["external_gene_name"]=""
            gene_list.append(result)
        return {"gene_list":gene_list,"gene_list_count":gene_list_count}

api.add_resource(get_sagd_list, '/api/get_sagd_list')

class get_tissue(Resource):
    def get(self):
        condition = {}
        items=mongo.db.total_result.distinct("Tissue",condition)
        return items
api.add_resource(get_tissue,'/api/tissue')

class clickfilter(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('taxon_id', type=str)
        parser.add_argument('tissue', type=str)
        parser.add_argument('stage', type=str)
        args = parser.parse_args()
        condition = {}
        if args['taxon_id']:
            if args['taxon_id'] != "":
                condition["Taxon_id"] = args['taxon_id']
        if args['tissue']:
            if args['tissue'] != "":
                condition["Tissue"] = args['tissue']
        if args['stage']:
            if args['stage'] != "":
                condition["Stage"] = args['stage']
        print(condition)
        tissue=mongo.db.total_result.distinct("Tissue",condition)
        stage=mongo.db.total_result.distinct("Stage",condition)
        taxons=mongo.db.total_result.distinct("Taxon_id",condition)
        return {"tissue":tissue,"stage":stage,"taxons":taxons}
api.add_resource(clickfilter,'/api/clickfilter')



class get_filter_list(Resource):
    @marshal_with(gene_list_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('taxon_id',type=str)
        parser.add_argument('tissue', type=str)
        parser.add_argument('stage', type=str)
        parser.add_argument('log2_min', type=str)
        parser.add_argument('log2_max', type=str)
        parser.add_argument('padj', type=str)
        parser.add_argument('per_page', type=int, default=20)
        parser.add_argument('page', type=int, default=1)
        args = parser.parse_args()
        page = args['page']
        per_page = args['per_page']
        record_skip = (page - 1) * per_page
        condition = {}
        if args['taxon_id']:
            if args['taxon_id']!="":
                condition["Taxon_id"] = args['taxon_id']

        if args['tissue']:
            if args['tissue']!="":
                condition["Tissue"]=args['tissue']
        if args['stage']:
            if args['stage']!="":
                condition["Stage"]=args['stage']
                print(condition)

        if args['padj']:
            if args['padj']!="":
                condition["padj"]={"$lt":float(args['padj'])}
                print(condition)

        if args['log2_min'] or args['log2_max']:
            condition["log2FoldChange"] = {}
        if args['log2_min'] :
            print(args['min'])
            condition["log2FoldChange"]["$lt"]= float(args['log2_min'])
        if args['log2_max']:
            print(args['max'])
            condition["log2FoldChange"]["$lt"] = float(args['log2_max'])
        print(condition)
        results = list(mongo.db.total_result.find(condition).skip(record_skip).limit(per_page))
        print(results)
        gene_list_count = mongo.db.total_result.find(condition).count()
        # if args["update"]!="update":
        #     print(condition)
        #     gene_list_count = mongo.db.total_result.find(condition).count()
        #     print(gene_list_count)
        # else:
        #     gene_list_count=0
        gene_list = []

        for result in results:
            if type(result["external_gene_name"])==float:
                result["external_gene_name"]=""
            gene_list.append(result)
        return {"gene_list":gene_list,"gene_list_count":gene_list_count}

api.add_resource(get_filter_list, '/api/filter')

gene_drug_fields={
    "DrugBank_ID":fields.String,
    "ensembl_gene_id":fields.String,
    "Drug_name":fields.String,
    "UniProt_Name":fields.String,
    "Type":fields.String,
    "UniProt ID":fields.String}
gene_drug_list_fields={
    'drug_list': fields.List(fields.Nested(gene_drug_fields)),
    'drug_list_count': fields.String
}

class get_drug_list(Resource):
    @marshal_with(gene_drug_list_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('query', type=str)
        parser.add_argument('per_page', type=int, default=20)
        parser.add_argument('page', type=int, default=1)
        args = parser.parse_args()
        page = args['page']
        per_page = args['per_page']
        record_skip = (page - 1) * per_page
        condition = {}
        if args['query']:
            condition["$or"] = [{"DrugBank_ID": {"$regex": args["query"], "$options": "$i"}},
                                {"ensembl_gene_id": {"$regex": args["query"], "$options": "$i"}},
                                {"Drug_name": {"$regex": args["query"], "$options": "$i"}},
                                {"Type": {"$regex": args["query"], "$options": "$i"}}]
        drug_list = list(mongo.db.drug_info.find(condition).skip(record_skip).limit(per_page))
        drug_list_count=mongo.db.drug_info.find(condition).count()

        return {"drug_list":drug_list,"drug_list_count":drug_list_count}
api.add_resource(get_drug_list,'/api/get_drug_list')

gene_dataset_fields={
    "SRA_Run" : fields.String,
    "group" : fields.String,
    "Scientific_name" :fields.String,
    "SRA_Study" : fields.String,
    "sagd_id" : fields.String,
    "Sex" : fields.String,
    "SRA_Experiment" :fields.String,
    "Common_name" : fields.String,
    "Tissue" :fields.String,
    "Taxonomy_ID" : fields.String,
    "Stage" : fields.String
}
gene_dataset_list_fields={
    'dataset_list': fields.List(fields.Nested(gene_dataset_fields)),
    'dataset_list_count': fields.String
}
class get_dataset_list(Resource):
    @marshal_with(gene_dataset_list_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('query', type=str)
        parser.add_argument('per_page', type=int, default=20)
        parser.add_argument('page', type=int, default=1)
        args = parser.parse_args()
        page = args['page']
        per_page = args['per_page']
        record_skip = (page - 1) * per_page
        condition = {}
        if args['query']:
            condition["$or"] = [{"SRA_Run": {"$regex": args["query"], "$options": "$i"}},
                                {"Scientific_name": {"$regex": args["query"], "$options": "$i"}},
                                {"SRA_Study": {"$regex": args["query"], "$options": "$i"}},
                                {"sagd_id": {"$regex": args["query"], "$options": "$i"}},
                                {"Sex": {"$regex": args["query"], "$options": "$i"}},
                                {"SRA_Experiment": {"$regex": args["query"], "$options": "$i"}},
                                {"Common_name": {"$regex": args["query"], "$options": "$i"}},
                                {"Tissue": {"$regex": args["query"], "$options": "$i"}},
                                {"Stage": {"$regex": args["query"], "$options": "$i"}},]
        dataset_list = list(mongo.db.sagd_id.find(condition).skip(record_skip).limit(per_page))
        dataset_list_count=mongo.db.sagd_id.find(condition).count()

        return {"dataset_list":dataset_list,"dataset_list_count":dataset_list_count}
api.add_resource(get_dataset_list,'/api/get_dataset_list')



# get_gene_info_fields={}
#
# class get_gene_info(Resource):
#     @marshal_with(get_gene_info_fields)
#     def get(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('gene', type=str)
#         args = parser.parse_args()
#         condition = {}
#         condition["ensembl_gene_id"] = args['gene']











# gene_start=58053298
# gene_end=58094336
# gene_length=gene_end-gene_start
# transcription=[]
# transcription.append({"exon":[
#     {"start":58053298,"end":58053326},
#     {"start":58053406,"end":58053541},
#     {"start":58053610,"end":58053973},
#     {"start":58093977,"end":58094336}
# ],"transcript_id":"ENSDART00000177747"})
# transcription.append({"exon":[
#     {"start":58053298,"end":58053326},
#     {"start":58053406,"end":58053541},
#     {"start":58053610,"end":58053973},
#     {"start":58054068,"end":58054409}
# ],"transcript_id":"ENSDART00000179425"})
# transcription.append({"exon":[
#     {"start":58053298,"end":58053973},
#     {"start":58054068,"end":58054194},
#     {"start":58054353,"end":58054409}
# ],"transcript_id":"ENSDART00000178901"})


# gap=gene_length/10
# svgs=''
# scale='<svg width="980" height="30">\n'
# scale=scale+'<line x1="0" y1="50%" x2="800" y2="50%" style="stroke:rgb(255,0,0);stroke-width:2" />\n'
# scale=scale+'<line x1="0" y1="60%" x2="0" y2="40%" style="stroke:rgb(255,0,0);stroke-width:2" />\n'
# scale=scale+'<line x1="80" y1="60%" x2="80" y2="40%" style="stroke:rgb(255,0,0);stroke-width:2" />\n'
# scale=scale+'<line x1="160" y1="60%" x2="160" y2="40%" style="stroke:rgb(255,0,0);stroke-width:2" />\n'
# scale=scale+'<line x1="240" y1="60%" x2="240" y2="40%" style="stroke:rgb(255,0,0);stroke-width:2" />\n'
# scale=scale+'<line x1="320" y1="60%" x2="320" y2="40%" style="stroke:rgb(255,0,0);stroke-width:2" />\n'
# scale=scale+'<line x1="400" y1="60%" x2="400" y2="40%" style="stroke:rgb(255,0,0);stroke-width:2" />\n'
# scale=scale+'<line x1="480" y1="60%" x2="480" y2="40%" style="stroke:rgb(255,0,0);stroke-width:2" />\n'
# scale=scale+'<line x1="560" y1="60%" x2="560" y2="40%" style="stroke:rgb(255,0,0);stroke-width:2" />\n'
# scale=scale+'<line x1="640" y1="60%" x2="640" y2="40%" style="stroke:rgb(255,0,0);stroke-width:2" />\n'
# scale=scale+'<line x1="720" y1="60%" x2="720" y2="40%" style="stroke:rgb(255,0,0);stroke-width:2" />\n'
# scale=scale+'<line x1="800" y1="60%" x2="800" y2="40%" style="stroke:rgb(255,0,0);stroke-width:2" />\n'
# scale=scale+'<text x="0" y="8" font-family="Verdana" font-size="10">'+str(round(gene_start/1000000.0,2))+'Mb'+'</text>\n'
# scale=scale+'<text x="80" y="8" font-family="Verdana" font-size="10" text-anchor="middle">'+str(round((gene_start+gap*1)/1000000.0,2))+'Mb'+'</text>\n'
# scale=scale+'<text x="160" y="8" font-family="Verdana" font-size="10" text-anchor="middle">'+str(round((gene_start+gap*2)/1000000.0,2))+'Mb'+'</text>\n'
# scale=scale+'<text x="240" y="8" font-family="Verdana" font-size="10" text-anchor="middle">'+str(round((gene_start+gap*3)/1000000.0,2))+'Mb'+'</text>\n'
# scale=scale+'<text x="320" y="8" font-family="Verdana" font-size="10" text-anchor="middle">'+str(round((gene_start+gap*4)/1000000.0,2))+'Mb'+'</text>\n'
# scale=scale+'<text x="400" y="8" font-family="Verdana" font-size="10" text-anchor="middle">'+str(round((gene_start+gap*5)/1000000.0,2))+'Mb'+'</text>\n'
# scale=scale+'<text x="480" y="8" font-family="Verdana" font-size="10" text-anchor="middle">'+str(round((gene_start+gap*6)/1000000.0,2))+'Mb'+'</text>\n'
# scale=scale+'<text x="560" y="8" font-family="Verdana" font-size="10" text-anchor="middle">'+str(round((gene_start+gap*7)/1000000.0,2))+'Mb'+'</text>\n'
# scale=scale+'<text x="640" y="8" font-family="Verdana" font-size="10" text-anchor="middle">'+str(round((gene_start+gap*8)/1000000.0,2))+'Mb'+'</text>\n'
# scale=scale+'<text x="720" y="8" font-family="Verdana" font-size="10" text-anchor="middle">'+str(round((gene_start+gap*9)/1000000.0,2))+'Mb'+'</text>\n'
# scale=scale+'<text x="800" y="8" font-family="Verdana" font-size="10" text-anchor="middle">'+str(round((gene_start+gap*10)/1000000.0,2))+'Mb'+'</text>\n'
# scale=scale+'</svg>\n'
# svgs=svgs+scale
#
# for i in transcription:
#     svg='<svg width="980" height="10">\n'
#     rects='<g fill="#CDCD00">\n'
#     for m in i['exon']:
#         width = (m["end"] - m["start"]) / float(gene_length) * 800
#         x = (m["start"] - gene_start) / float(gene_length) * 800
#         rect='<rect x="'+str(x)+ '" y="0" width="'+str(width)+ '" height="10"></rect>\n'
#         rects=rects+rect
#     rects = rects + "</g>\n"
#     polylines='<g>\n'
#     if i['exon'][0]["start"]!=gene_start:
#         intro_start=0
#         intro_end=(i['exon'][0]["end"]-gene_start)/float(gene_length)*800
#         middle = (intro_start + intro_end) / 2
#         polyline = '<polyline points="' + str(intro_start) + ',5 ' + str(middle) + ',5 ' + str(intro_end) + ',5 ' + '" style="fill:none;stroke:black;stroke-width:1"/>\n'
#         polylines=polylines+polyline
#     for j in range(0,len(i["exon"])-1):
#         intro_start=(i['exon'][j]["end"]-gene_start)/float(gene_length)*800
#         intro_end=(i['exon'][j+1]["start"]-gene_start)/float(gene_length)*800
#         middle=(intro_start+intro_end)/2
#         polyline = '<polyline points="' + str(intro_start) + ',5 ' + str(middle) + ',5 ' + str(intro_end) + ',5 '+'" style="fill:none;stroke:black;stroke-width:1"/>\n'
#         polylines = polylines + polyline
#
#     if i['exon'][-1]["end"]!=gene_end:
#         intro_end=gene_length/float(gene_length)*800
#         intro_start=(i['exon'][-1]["end"]-gene_start)/float(gene_length)*800
#         middle = (intro_start + intro_end) / 2
#         polyline = '<polyline points="' + str(intro_start) + ',5 ' + str(middle) + ',5 ' + str(intro_end) + ',5 ' + '" style="fill:none;stroke:black;stroke-width:1"/>\n'
#         polylines=polylines+polyline
#     polylines=polylines+'</g>\n'
#     text='<text x="810" y="50%" dy=".3em" fill="black" font-size="12">'+i["transcript_id"]+'</text>\n'
#     svg=svg+rects+polylines+text+'</svg>\n'
#     svgs=svgs+svg













