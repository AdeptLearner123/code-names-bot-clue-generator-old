import sqlite3


class CluesDatabase:
    def __init__(self, PATH):
        self.con = sqlite3.connect(PATH)
        self.cur = self.con.cursor()

    def setup(self):
        self.cur.execute(
            """
                CREATE TABLE IF NOT EXISTS term_clue (
                    term TEXT NOT NULL,
                    clue TEXT NOT NULL,
                    score REAL NOT NULL,
                    type TEXT NOT NULL,
                    reason TEXT NOT NULL,
                    CONSTRAINT term_clue_unique UNIQUE (term, clue)
                );
            """
        )
        self.cur.execute(
            """
                CREATE INDEX IF NOT EXISTS term_clue_index ON term_clue (term, clue);
            """
        )

    def insert_term_clue(self, term, clue, score, type, reason):
        self.cur.execute(
            "SELECT * FROM term_clue WHERE term=? AND clue=?;", [term, clue]
        )
        if len(self.cur.fetchall()) == 0:
            self.cur.execute(
                "INSERT INTO term_clue (term, clue, score, type, reason) VALUES(?,?,?,?,?);",
                [term, clue, score, type, reason],
            )
        else:
            self.cur.execute(
                "UPDATE term_clue SET score=?, type=?, reason=? WHERE term=? AND clue=?;",
                [score, type, reason, term, clue],
            )

    def get_top_clues(self, term, count, reverse=False):
        order_str = "ASC" if reverse else "DESC"
        self.cur.execute(
            "SELECT clue, score, type, reason FROM term_clue WHERE term=? ORDER BY score {0} LIMIT ?".format(
                order_str
            ),
            [term, count],
        )
        return self.cur.fetchall()

    def get_all_clues(self, term):
        self.cur.execute("SELECT clue, score, type, reason FROM term_clue WHERE term=?", [term])
        scores = {}
        for row in self.cur.fetchall():
            scores[row[0]] = row[1:]
        return scores

    def get_term_clue(self, term, clue):
        self.cur.execute(
            "SELECT score, type, reason FROM term_clue WHERE term=? AND clue=?",
            [term, clue],
        )
        row = self.cur.fetchone()
        if row is None:
            return None, None, None
        return row

    def commit(self):
        self.con.commit()

    def clear_term_clues(self, term):
        self.cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='term_clue';"
        )
        if self.cur.fetchone() is None:
            return

        self.cur.execute("DELETE FROM term_clue WHERE term=?", [term])
        self.con.commit()
        self.cur.execute("VACUUM")
        self.con.commit()

    def clear(self):
        self.cur.execute("DELETE FROM term_clue")
        self.con.commit()
        self.cur.execute("VACUUM")
        self.con.commit()
