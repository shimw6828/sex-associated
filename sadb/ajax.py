import flask_restful
import string
import json
from sadb import app, api
from sadb.core import mongo
from flask_restful import Resource, fields, marshal_with, reqparse, marshal



test_fields = {
    'gene_id': fields.String,
    'pvalue': fields.Float,
    'log2FoldChange': fields.Float,
    'lfcSE':fields.Float,
    'padj':fields.Float,
    'baseMean':fields.Float,
    'stat':fields.Float
}
testdb_fields = {
    'gene_list':fields.List(fields.Nested(test_fields)),
    'gene_list_count': fields.Integer
}
class test(Resource):
    @marshal_with(testdb_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page',type=int,default=1)
        parser.add_argument('per_page', type=int, default=15)
        parser.add_argument('gene_id',type=str)
        parser.add_argument('pvalue',type=float)
        args = parser.parse_args()
        page = args['page']
        per_page = args['per_page']
        record_skip = (page - 1) * per_page
        condition = {}
        if args['gene_id']:
            condition['gene_id'] = args['gene_id']
        if args['pvalue']:
            condition['pvalue'] = {"$gte":args['pvalue']}
        gene_list=list(mongo.db.SRP062329.find(condition).skip(record_skip).limit(per_page))
        gene_list_count = mongo.db.SRP062329.find(condition).count()
        return {"gene_list":gene_list,"gene_list_count":gene_list_count}

api.add_resource(test, '/api/test')

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

gene_list_fields={
    'gene_ID':fields.String,
    'external_gene_name':fields.String,
    'baseMean':fields.Float,
    'SRA_ID':fields.String,
    'chromosome_name':fields.String,
    'log2FoldChange':fields.Float,
    'padj':fields.Float,
    'Scientific_name':fields.String
}

taxonomy_fields={
    'gene_list': fields.List(fields.Nested(gene_list_fields)),
    'gene_list_count': fields.Integer
}

class get_taxonomy_list(Resource):
    @marshal_with(taxonomy_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page',type=int,default=1)
        parser.add_argument('per_page', type=int, default=15)
        parser.add_argument('taxon_id', type=int)
        args = parser.parse_args()
        page = args['page']
        per_page = args['per_page']
        record_skip = (page - 1) * per_page
        condition = {}
        condition['Taxon_id'] = args['taxon_id']
        results = list(mongo.db.total_result.find(condition).skip(record_skip).limit(per_page))
        gene_list_count = mongo.db.total_result.find(condition).count()
        gene_list = []

        for result in results:
            gene_detail = mongo.db.gene_detail.find_one({"ensembl_gene_id": result["gene_ID"]})
            result["external_gene_name"] = gene_detail["external_gene_name"]
            result["chromosome_name"] = gene_detail["chromosome_name"]
            if type(result["external_gene_name"])==float:
                result["external_gene_name"]=""
            gene_list.append(result)
        return {"gene_list":gene_list,"gene_list_count":gene_list_count}
api.add_resource(get_taxonomy_list,'/api/taxonomy_list')












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













