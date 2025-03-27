from flask import jsonify, request, current_app
from app.api.services import bp

@bp.route('/health', methods=['GET'])
def health_check():
    """
    Basic health check endpoint for API services.
    """
    current_app.logger.info('Health check endpoint called')
    return jsonify({'status': 'healthy', 'service': 'API Services'}), 200

@bp.route('/example', methods=['GET'])
def example_endpoint():
    """
    Example endpoint for API services.
    """
    current_app.logger.info('Example endpoint called')
    return jsonify({'data': 'This is an example API endpoint for services'}), 200 