# airflow-dags

Two small Apache Airflow DAGs that pull data from an HTTP API every 15 minutes and push it to a Google Apps Script web app (typically one that writes rows into a Google Sheet).

## DAGs

### `dag_weather` (Weather-data-to-Sheets/)

```
Airflow (every 15 min)
    |
    v
weatherapi.com  /v1/current.json?q=<location>
    |
    v
flatten nested JSON (location_name, current_temp_c, ...)
    |
    v
POST JSON --> Apps Script web app (?location=<location>)
```

- `dag_weather.py` defines one `PythonOperator` that calls `get_current_weather`.
- `weather_utils.py` fetches current conditions from weatherapi.com, flattens the nested response into `parent_child` keys, and posts it to the web app.

### `dag_extraction` (extract-site/)

```
Airflow (every 15 min)
    |
    v
for each keyword:
    extraction API  GET <API_EP_OOB>/get?url=<SCRAPE_SITE_1><keyword>&tag=article
        |
        v
    build rows: keyword, job_id, articleText, job_tags, link
        |
        v
    POST JSON --> Apps Script web app (?keyword=<keyword>)
```

- `dag_extraction.py` reads the keyword list and target site from Airflow Variables and runs `process_main`.
- `extract_utils.py` calls a separate HTML extraction service (not in this repo) that returns `results[]` with `hrefs` and `articleText` for each `<article>` on the page. For each result it builds an absolute link, pulls an ID from a `~<id>/?` segment of the link, splits the last paragraph of the text off as comma separated tags, and posts the rows to the web app.

Both DAGs: `start_date` 2023-08-11, `catchup=False`, 1 retry after 5 minutes.

## Stack

Python, Apache Airflow 2.x (`PythonOperator`, `airflow.operators.empty`, `schedule_interval`), `requests`, Google Apps Script as the sink.

## Setup

1. Install Airflow 2.x and `requests` in the Airflow environment.
2. Copy the `.py` files into your DAGs folder. Each DAG imports its helper by plain module name (`weather_utils`, `extract_utils`), so the helper must be importable from the DAG: put both files at the top level of the DAGs folder, or add the subfolder to `PYTHONPATH`.
3. Create the Airflow Variables listed below (Admin > Variables, or `airflow variables set NAME VALUE`).
4. Point the Apps Script URLs at your own web apps. They are hardcoded as `webapp_url` in `weather_utils.py` and `extract_utils.py`; the receiving Apps Script is not part of this repo.
5. Unpause the DAGs in the Airflow UI.

## Configuration (Airflow Variables)

| Variable | Used by | Purpose |
|----------|---------|---------|
| `WEATHER_API_KEY_SECRET` | dag_weather | weatherapi.com API key |
| `WEATHER_API_LOCATION` | dag_weather | Location query, e.g. a city name |
| `SCRAPE_KEYWORDS_1` | dag_extraction | Comma separated keywords |
| `SCRAPE_SITE_1` | dag_extraction | Search URL prefix; the keyword is appended to it |
| `API_EP_OOB` | dag_extraction | Base URL of the extraction service |

## Notes

- Errors inside the tasks are printed and swallowed, so a failed API call does not fail the Airflow task. Check the task logs.
- In `dag_extraction` the row list is not reset between keywords, so each POST also contains rows from earlier keywords in the same run.
- `schedule_interval` is deprecated in later Airflow 2 releases and removed in Airflow 3; use `schedule=` there.

## Author

Built by Saim Safdar - https://saim.me
