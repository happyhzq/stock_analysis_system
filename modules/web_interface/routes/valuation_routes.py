# modules/web_interface/routes/valuation_routes.py
from flask_restx import Namespace, Resource, fields
from valuation_engine.core import ValuationEngine
from flask import jsonify

api = Namespace('valuation', description='股票估值接口')

valuation_model = api.model('ValuationRequest', {
    'symbol': fields.String(required=True, example='AAPL'),
    'model_type': fields.String(enum=['dcf', 'comps'], default='dcf')
})

@api.route('/')
class ValuationResource(Resource):
    @api.expect(valuation_model)
    @api.response(200, '估值成功')
    @api.response(400, '无效请求')
    def post(self):
        """执行股票估值计算"""
        try:
            data = api.payload
            result = ValuationEngine().run_valuation(
                data['symbol'], 
                data.get('model_type', 'dcf')
            )
            return jsonify({
                'symbol': result['symbol'],
                'valuation': result['value'],
                'model': result['model'],
                'currency': 'USD'
            })
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, '服务器内部错误')