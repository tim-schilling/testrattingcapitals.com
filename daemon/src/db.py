import logging
import os
import threading
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DEFAULT_DB_CONNECTION_STRING = 'sqlite:///db.sqlite3'

logger = logging.getLogger('testrattingcapitals')


class Context(object):
    """SQLalchemy Session with_statement wrapper

    Creates and destroys a sqlalchemy session in the with_statement lifecycle.
    If a module-level _engine does not exist, it will acquire a lock and create
    one in your thread."""

    _engine_lock = threading.Lock()
    _engine = None
    _session_factory = None

    def __init__(self):
        """ Lazily create module-level engine
        """
        self.session = None

        Context._engine_lock.acquire()
        if Context._engine is None:
            logger.info('Creating db engine')
            Context._engine = create_engine(os.getenv(
                'DB_CONNECTION_STRING',
                DEFAULT_DB_CONNECTION_STRING
            ))
        if Context._session_factory is None:
            logger.info('Creating db session_factory')
            Context._session_factory = sessionmaker(bind=Context._engine, autocommit=False)
        Context._engine_lock.release()

    def __enter__(self):
        """Construct instance-level session to expose
        """

        if self.session is None:
            self.session = Context._session_factory()
        return self

    def __exit__(self, type, value, traceback):
        """Destroy instance-level session
        """

        if self.session:
            self.session.close()
            self.session = None
