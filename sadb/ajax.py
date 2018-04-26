import flask_restful
import string
import json
from sadb import app, api
from sadb.core import mongo
from flask_restful import Resource, fields, marshal_with, reqparse, marshal
#coding=utf-8


gene_list_fields={
    'gene_ID':fields.String,
    'external_gene_name':fields.String,
    'baseMean':fields.Float,
    'SRP':fields.String,
    'SRX_T':fields.String,
    'SRX_O':fields.String,
    'FPKM_SRX_T':fields.Float,
    'FPKM_SRX_O':fields.Float,
    'chromosome_name':fields.String,
    'log2FoldChange':fields.Float,
    'padj':fields.Float,
    'Scientific_name':fields.String
}

taxonomy_fields={
    'gene_list': fields.List(fields.Nested(gene_list_fields)),
    'gene_list_count': fields.Integer
}
class search(Resource):
    @marshal_with(taxonomy_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page',type=int,default=1)
        parser.add_argument('per_page', type=int, default=20)
        parser.add_argument('filter', type=str)
        parser.add_argument('min', type=str)
        parser.add_argument('max', type=str)
        args = parser.parse_args()
        page = args['page']
        per_page = args['per_page']
        record_skip = (page - 1) * per_page
        condition = {}
        condition["padj"]={"$gte":0,"$lte":1}
        if args['query']:
            condition["$or"]=[{"gene_ID":{"$regex": args["query"],"$options": "$i"}},
                              {"external_gene_name":{"$regex": args["query"],"$options": "$i"}},
                              {"chromosome_name":{"$regex": args["query"],"$options": "$i"}}]
        if args['min'] :
            condition["padj"]["$gte"]= float(args['min'])
        if args['max']:
            condition["padj"]["$lte"] = float(args['max'])


        results = list(mongo.db.total_result.find(condition).sort([("padj",-1)]).skip(record_skip).limit(per_page))

        gene_list_count = mongo.db.total_result.find(condition).count()
        gene_list = []

        for result in results:
            if type(result["external_gene_name"])==float:
                result["external_gene_name"]=""
            gene_list.append(result)
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
        parser.add_argument('taxon_id', type=int)
        args = parser.parse_args()
        condition = {}
        condition['Taxonomy_Id'] = args['taxon_id']
        result=mongo.db.total_result.find_one(condition,{'Taxonomy_Id':1,'Common_name':1})
        return result

api.add_resource(get_common_name,'/api/get_common_name')



class get_taxonomy_list(Resource):
    @marshal_with(taxonomy_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page',type=int,default=1)
        parser.add_argument('per_page', type=int, default=20)
        parser.add_argument('taxon_id', type=int)
        parser.add_argument('filter', type=str)
        parser.add_argument('sort', type=str,default="default")
        parser.add_argument('min', type=str)
        parser.add_argument('max', type=str)
        args = parser.parse_args()
        page = args['page']
        per_page = args['per_page']
        record_skip = (page - 1) * per_page
        condition = {}
        condition['Taxon_id'] = args['taxon_id']
        condition["padj"]={"$gte":0,"$lte":1}
        if args['filter']:
            condition["$or"]=[{"gene_ID":{"$regex": args["filter"],"$options": "$i"}},
                              {"external_gene_name":{"$regex": args["filter"],"$options": "$i"}},
                              {"chromosome_name":{"$regex": args["filter"],"$options": "$i"}}]
        if args['min'] :
            condition["padj"]["$gte"]= float(args['min'])
        if args['max']:
            condition["padj"]["$lte"] = float(args['max'])


        results = list(mongo.db.total_result.find(condition).sort([("padj",-1)]).skip(record_skip).limit(per_page))

        gene_list_count = mongo.db.total_result.find(condition).count()
        gene_list = []

        for result in results:
            if type(result["external_gene_name"])==float:
                result["external_gene_name"]=""
            gene_list.append(result)
        return {"gene_list":gene_list,"gene_list_count":gene_list_count}
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
        if str(detail["entrezgene"])=="nan":
            detail["entrezgene"]=str(detail["entrezgene"])
        else:
            detail["entrezgene"]=int(detail["entrezgene"])
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
        gene_structures={"transcript": structures, "gene_model": svgs}
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
        return go_terms["go_terms"]
api.add_resource(get_go_terms,'/api/get_go_terms')


get_homolog_fields={
    "ortholog":fields.String,
    "homolog_perc_id_r1":fields.Float,
    "homolog_perc_id": fields.Float,
    "homolog_wga_coverage": fields.String,
    "ortholog_external_gene_name": fields.String,
    "external_gene_name": fields.String,
    "homolog_orthology_confidence": fields.String
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
        return homolog['homologs']
api.add_resource(get_homolog,'/api/get_homolog')


get_paralogue_fields={
    "paralog_ensembl_gene":fields.String,
    'paralog_gene_name': fields.String,
    'paralog_gene_chromosome':fields.String,
    'paralog_gene_start':fields.Integer,
    'paralog_gene_end':fields.Integer,
    'external_gene_name': fields.String,
    'ensembl_gene_id':fields.String
}
class get_paralogue(Resource):
    @marshal_with(get_paralogue_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('gene', type=str)
        args = parser.parse_args()
        condition = {}
        condition["ensembl_gene_id"] = args['gene']

        result = mongo.db.paralogue.find_one(condition)["paralog_ensembl_gene"]
        paralogue=[]
        for i in result:
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
        return paralogue
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
        return proteins["Proteins"]
api.add_resource(get_proteins,'/api/get_proteins')


get_result_fields={
    "stat":fields.String,
    "baseMean": fields.Float,
    "Scientific_name": fields.String,
    "padj": fields.Float,
    "gene_ID": fields.String,
    "external_gene_name": fields.String,
    "Taxon_id": fields.String,
    "entrezgene": fields.String,
    "lfcSE": fields.Float,
    "log2FoldChange": fields.Float,
    "Common_name": fields.String,
    "chromosome_name": fields.String,
    "pvalue": fields.Float,
    "SRA_ID": fields.String
}
get_analysis_fields={
    'analysis': fields.List(fields.Nested(get_result_fields)),
    'taxname': fields.String,
    'taxon_id':fields.Integer
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
        taxname=analysis[0]["Scientific_name"].replace(" ","_").encode()
        return {"analysis":analysis,"taxname":taxname,"taxon_id":analysis[0]["Taxon_id"]}
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













