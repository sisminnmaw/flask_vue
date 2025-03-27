import logging
from logging.handlers import RotatingFileHandler
import os

# Configure batch script logging
if not os.path.exists('app/logs'):
    os.makedirs('app/logs')

# Create logger
batch_logger = logging.getLogger('batch')
batch_logger.setLevel(logging.INFO)

# Create file handler
file_handler = RotatingFileHandler('app/logs/batch.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)

# Add handler to logger
batch_logger.addHandler(file_handler) 