from flask import jsonify, request, current_app
from app.api.frontend import bp

@bp.route('/user', methods=['GET'])
def get_user():
    """
    Example endpoint for getting user information.
    This would typically be used by the frontend.
    """
    current_app.logger.info('User info endpoint called')
    # Mocked user data
    user_data = {
        'id': 1,
        'username': 'user1',
        'email': 'user1@example.com',
        'role': 'admin'
    }
    return jsonify(user_data), 200

@bp.route('/dashboard', methods=['GET'])
def get_dashboard_data():
    """
    Example endpoint for getting dashboard data.
    This would typically be used by the frontend.
    """
    current_app.logger.info('Dashboard data endpoint called')
    # Mocked dashboard data
    dashboard_data = {
        'stats': {
            'users': 100,
            'active_sessions': 25,
            'pending_tasks': 5
        },
        'recent_activities': [
            {'id': 1, 'action': 'Login', 'timestamp': '2023-01-01T12:00:00Z'},
            {'id': 2, 'action': 'Update Profile', 'timestamp': '2023-01-01T12:05:00Z'},
            {'id': 3, 'action': 'Logout', 'timestamp': '2023-01-01T12:30:00Z'}
        ]
    }
    return jsonify(dashboard_data), 200 