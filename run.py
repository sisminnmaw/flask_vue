#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from app import create_app
from app.models import db, migrate
from app.models.user import User

# Get environment from environment variable or default to development
env = os.environ.get('FLASK_ENV', 'development')
app = create_app()

# Initialize database and migrations
with app.app_context():
    db.init_app(app)
    migrate.init_app(app, db)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=(env == 'development')) 