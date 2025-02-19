# modules/web_interface/routes/health_routes.py （补充）
@api.route('/health')
class HealthCheck(Resource):
    def get(self):
        """系统健康检查"""
        return {
            'status': 'healthy',
            'database': 'connected' if check_db() else 'down'
        }