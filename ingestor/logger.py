import logging
from pythonjsonlogger import jsonlogger
from datetime import datetime, timezone

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('time'):
            log_record['time'] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        if not log_record.get('level'):
            log_record['level'] = record.levelname.upper()
        if not log_record.get('msg'):
            log_record['msg'] = record['message']

def init_logger():
    logger = logging.getLogger('kafka-consumer')
    logger.setLevel(logging.INFO)

    logHandler = logging.StreamHandler()
    format_str = '%(time)s %(level)s %(msg)s'
    formatter = CustomJsonFormatter(format_str)
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    logger.propagate = False

    return logger

logger = init_logger()
