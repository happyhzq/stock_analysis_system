# web_interface/routes/data_routes.py
from flask_restx import Namespace, Resource, fields
from data_processor.data_loader import DataLoader

api = Namespace('data', description='数据管理接口')

upload_model = api.model('Upload', {
    'source': fields.String(required=True, enum=['local', 'edgar', 'yahoo']),
    'symbol': fields.String(required=True)
})

@api.route('/upload')
class DataUpload(Resource):
    @api.expect(upload_model)
    def post(self):
        """上传并处理财务数据"""
        payload = api.payload
        loader = DataLoader()
        # 实际处理逻辑
        return {"status": "received"}, 201