from sys import stdout
from settings import settings
from logging import FileHandler, Formatter, StreamHandler, getLogger


LOG = getLogger("auth")
LOG.setLevel(settings.log_level)

formatter = Formatter("%(asctime)-23s | %(name)-23s | %(levelname)-8s | %(message)s")

stream_handler = StreamHandler(stream=stdout)
stream_handler.setFormatter(formatter)
stream_handler.setLevel(settings.log_level)
LOG.addHandler(stream_handler)


if settings.log_turn_on_file_handler:
    file_handler = FileHandler(settings.log_filepath)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(settings.log_level)
    LOG.addHandler(file_handler)
