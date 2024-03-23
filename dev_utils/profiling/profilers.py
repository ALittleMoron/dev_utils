import queue


class QueryInfo:
    ...


class SQLAlchemyQueryProfiler:
    def __init__(self, engine=sqlalchemy.engine.Engine):
        self.started = False
        self.engine = engine
