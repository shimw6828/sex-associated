from sadb import app, api

from sadb.core import mongo
from flask_restful import Resource, fields, marshal_with, reqparse, marshal



test_fields = {
    'gene_id': fields.String,
    'pvalue': fields.Float,
    'log2FoldChange': fields.Float,
    'lfcSE':fields.Float,
    'padj':fields.Float,
    'baseMean':fields.Float
}

testdb_fields = {
    'gene_list':fields.List(fields.Nested(test_fields)),
    'gene_list_count': fields.Integer
}

class testdb(Resource):
    @marshal_with(testdb_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('gene_id',type=str)
        args = parser.parse_args()
        condition = {}
        if args['gene_id']:
            condition["gene_id"]=args['gene_id']
        gene_list = mongo.db.SRP062329.find(condition)
        gene_list_count = gene_list.count()
        return {"gene_list": gene_list, "gene_list_count": gene_list_count}

api.add_resource(testdb, '/api/testdb')

