# First real test for the aqa-db-testing skill. Creates a bug through the
# practice app's API, then asserts directly against Postgres rather than
# trusting the API response, since the whole point of this skill is
# verifying what actually landed in the database, not what the API claims.
#
# Cleanup matters here specifically because the row gets created through a
# real API call, not a direct insert this test controls, so there is no
# single transaction to roll back. Deleting it explicitly in a fixture is
# the only way to keep this from leaving rows behind on every run, which it
# was doing before this fixture existed.

import os
import requests
import psycopg2

PRACTICE_APP_URL = "http://localhost:8000"
DB_URL = os.getenv("TEST_DATABASE_URL")


def _delete_bug(bug_id):
    conn = psycopg2.connect(DB_URL)
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM bugs WHERE id = %s", (bug_id,))
            conn.commit()
    finally:
        conn.close()


def test_db_bugs_create_inserts_correct_row():
    response = requests.post(
        f"{PRACTICE_APP_URL}/bugs",
        json={"title": "test db assertion", "severity": "high"},
    )
    assert response.status_code == 200
    bug_id = response.json()["id"]

    try:
        conn = psycopg2.connect(DB_URL)
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT title, severity, status, closed_at FROM bugs WHERE id = %s",
                    (bug_id,),
                )
                row = cur.fetchone()
        finally:
            conn.close()

        assert row is not None
        title, severity, status, closed_at = row
        assert title == "test db assertion"
        assert severity == "high"
        assert status == "open"
        assert closed_at is None
    finally:
        # Runs whether the assertions above passed or failed, so a failed
        # test does not also leave a row behind on top of failing.
        _delete_bug(bug_id)
