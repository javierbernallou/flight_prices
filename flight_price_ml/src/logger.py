import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Create a logger instance
logger = logging.getLogger('flight_price_logger')

# Test logging
logger.info('Logger is set up and ready to use.')