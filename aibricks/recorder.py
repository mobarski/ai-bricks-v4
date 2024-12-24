import time
import json

from aibricks.utils.db import DbConnectionFactory
# TODO: register errors, retries and exceptions


CREATE_SQL = """
    CREATE TABLE IF NOT EXISTS recordings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model,
        created_ts,
        request_ts,
        response_ts,
        exception_ts,
        request_id,
        request_json,
        response_json,
        exception_json
    );
"""

INSERT_SQL = """
    INSERT INTO recordings (
        model,
        created_ts,
        request_ts,   response_ts,   exception_ts,
        request_id,
        request_json, response_json, exception_json
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
"""


class Recorder:
    def __init__(self, db_path):
        self.db = DbConnectionFactory.connect(db_path)
        self.db.execute(CREATE_SQL)

    def record_request(self, request, ctx):
        ctx['request_ts'] = time.time()
        ctx['request_json'] = json.dumps(request)
        ctx['request_id'] = self.record(ctx)

    def record_response(self, response, ctx):
        ctx['response_ts'] = time.time()
        ctx['response_json'] = json.dumps(response)
        self.record(ctx)

    def record_stream_response(self, response, ctx):
        ctx['request_json'] = None
        self.record_response(response, ctx)

    def record_exception(self, exception, ctx):
        ctx['exception_ts'] = time.time()
        ctx['exception_json'] = json.dumps(exception)
        self.record(ctx)

    def record(self, ctx):
        cursor = self.db.execute(INSERT_SQL, (
            ctx['model'],
            time.time(),  # created_ts
            ctx['request_ts'],
            ctx.get('response_ts'),
            ctx.get('exception_ts'),
            ctx.get('request_id'),
            ctx['request_json'],
            ctx.get('response_json'),
            ctx.get('exception_json'),
        ))
        self.db.commit()  # TODO: vs stream
        return cursor.lastrowid
