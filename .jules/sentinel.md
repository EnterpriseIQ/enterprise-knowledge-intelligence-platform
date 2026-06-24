## 2025-02-18 - [SQL Injection in SQLite Ingestion]
**Vulnerability:** `load_sql` in `src/ingestion/sql_loader.py` interpolates table and column names directly into SQL strings without proper escaping. This allowed malicious SQLite databases with crafted table or column names to execute arbitrary SQL or break parsing.
**Learning:** Even though `sqlite3` driver was connected in read-only mode (`?mode=ro`), executing a `UNION ALL` statement through string interpolation allowed an attacker to inject queries that can extract secrets from other tables or execute statements leading to denial of service. Dynamic SQL query construction must always escape literals and identifiers.
**Prevention:** I escaped single quotes (`'`) as double single quotes (`''`) for string literals and double quotes (`"`) as double double quotes (`""`) for table and column identifiers when building the `SELECT` queries string.

## 2025-02-18 - [Hardcoded Default API Key]
**Vulnerability:** A hardcoded default API key `"dev-secret-key"` was set in `src/config.py` when `ERAG_API_KEY` was missing from the environment. This is a critical security vulnerability, as anyone who forgets to set the environment variable would unwittingly launch the application with a highly predictable, known secret key.
**Learning:** Hardcoded keys for default developer setups can accidentally leak into production if variables aren't strictly enforced.
**Prevention:** Using a random runtime default (e.g. `secrets.token_hex(32)`) ensures that even if an environment variable isn't set, the default API key is completely unpredictable and unguessable by an attacker.
