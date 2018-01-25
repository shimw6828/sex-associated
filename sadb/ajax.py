import flask_restful
import string
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





