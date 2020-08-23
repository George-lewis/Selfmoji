import logging, crayons


def setup_logging():

    logging.basicConfig(
        format="%(levelname)s:%(name)s:%(asctime)s: %(message)s",
        datefmt="%I:%M:%S:%p",
        level=logging.ERROR,
    )

    old_record_factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs) -> logging.LogRecord:
        record: logging.LogRecord = old_record_factory(*args, **kwargs)
        level = record.levelno
        _format = None
        if level <= logging.INFO:
            _format = crayons.green
        elif level <= logging.WARNING:
            _format = crayons.yellow
        else:
            _format = crayons.red
        record.msg = _format(record.msg)
        return record

    logging.setLogRecordFactory(record_factory)
