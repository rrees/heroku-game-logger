"""
Initial table creation
"""

from yoyo import step

__depends__ = {}

create_game_log_table = """
CREATE TABLE game_logs (
    log_id UUID PRIMARY KEY,
    game_name text NOT NULL,
    played_on date NOT NULL,
    user_id text,
    notes text,
    tags text[]
    )
"""

steps = [
    step(
        create_game_log_table,
        "DROP TABLE game_logs",
        ),
]
