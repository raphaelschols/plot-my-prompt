create_query_prompt = """
Given the following input {question}, create a syntactically correct {dialect} query to help find the answer. 
Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results. 
You can order the results by a relevant column to return the most meaningful or interesting examples in the database.

Never query for all the columns from a table; only select the relevant columns needed to answer the question.

Use only the column names and table relationships explicitly provided below. 
Be careful not to reference non-existent columns or incorrect table relationships. 
Pay attention to which column belongs to which table and how tables are linked via their relationships.

Only use the following tables and relationships:
{tables_and_relationship}
"""

adjust_query_prompt = """
You are given:
- An EXISTING {dialect} SQL query.
- Given the following user {question} query should be modified.

Task:
Rewrite the SQL so it applies ONLY the requested changes while keeping the rest of the query intact and valid.

Rules:
1) Preserve existing SELECT columns, JOINs, filters, GROUP BY, HAVING, ORDER BY, LIMIT unless explicitly changed.
2) Use ONLY the tables/columns/relationships listed below. Do NOT invent columns or tables.
3) Add filters in WHERE (or HAVING if filtering on aggregates). Use existing aliases.
4) If changing aggregation, update SELECT expressions and the GROUP BY accordingly.
5) If sorting/limiting is requested, edit ORDER BY/LIMIT; otherwise keep existing. If neither exists, cap results at {top_k}.
6) If renaming outputs, use AS aliases only (don’t change underlying column names).
7) If removing something (filter/column/sort/limit), remove it precisely and leave others unchanged.
8) Keep CTEs/aliases/indentation style consistent.
9) Make the smallest change that satisfies the request.

Only use the following tables and relationships:
{tables_and_relationship}

Existing query:
```sql
{existing_query}"""

