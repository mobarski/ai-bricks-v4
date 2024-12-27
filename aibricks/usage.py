from .recorder import Recorder

USAGE_SQL = """
    WITH usage AS (
        SELECT
            date(created_ts, 'unixepoch', 'localtime') as day,
            model,
            json_extract(response_json, "$.usage.prompt_tokens")     as prompt_tokens,
            json_extract(response_json, "$.usage.completion_tokens") as completion_tokens
        FROM recordings
        WHERE response_json is not null
    )
    SELECT
        day,
        model,
        sum(prompt_tokens)     as prompt_tokens,
        sum(completion_tokens) as completion_tokens
    FROM usage
    GROUP BY day, model
"""

if __name__ == "__main__":
    db = Recorder("data/recorder.db").db
    for row in db.execute('select response_json from recordings where request_json is null'):
        print(row)

# TODO: combine with the recorder
