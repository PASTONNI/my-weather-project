# Weather Pipeline

A daily ETL pipeline built with Apache Airflow that retrieves hourly weather data for Berlin from the [Open-Meteo API](https://open-meteo.com/), stores the raw data in Amazon S3, loads it into PostgreSQL, transforms it into a daily summary, and sends an email with clothing and umbrella recommendations.

The AWS infrastructure is provisioned using Terraform.

## Architecture

```text
Open-Meteo API
      │
      ▼
 extract_data ─────────► Amazon S3
      │                  raw/<YYYY-MM-DD>.csv
      ▼
load_data_to_db ───────────────┐
                               ├──► transform_data
load_weather_codes ────────────┘
                                       │
                                       ▼
                                   recommend
                                       │
                                       ▼
                                     notify
                                       │
                                       ▼
                              HTML email report
```

`load_data_to_db` and `load_weather_codes` run in parallel before `transform_data`.

## Tech Stack

| Layer          | Tool                               |
| -------------- | ---------------------------------- |
| Orchestration  | Apache Airflow                     |
| Data source    | Open-Meteo API                     |
| Storage        | Amazon S3                          |
| Database       | Amazon RDS PostgreSQL              |
| Processing     | pandas and SQLAlchemy              |
| Notifications  | Jinja2 and Airflow email utilities |
| Infrastructure | Terraform                          |

## Project Structure

```text
.
├── dags/
│   └── weather_dag.py
├── include/
│   ├── tasks.py
│   ├── config.py
│   ├── db_engine.py
│   ├── extract.py
│   ├── db_load.py
│   ├── transform.py
│   ├── recommend.py
│   ├── notify.py
│   └── templates/
│       └── weather_report.html
├── terraform/
│   ├── main.tf
│   ├── s3_bucket.tf
│   ├── provider.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── backend.tf
│   └── .terraform.lock.hcl
├── requirements.txt
├── .gitignore
└── README.md
```

## Pipeline Stages

1. **Extract**
   Retrieves hourly temperature, apparent temperature, wind speed, precipitation, and weather-code data for Berlin.

2. **Load raw data**
   Writes the API response to:

   ```text
   s3://<bucket-name>/raw/<YYYY-MM-DD>.csv
   ```

   The file is then loaded into the PostgreSQL `weather_table`.

3. **Load weather codes**
   Loads a reference table that maps Open-Meteo weather codes to readable descriptions.

4. **Transform**
   Joins the weather data with the code lookup, creates clothing and umbrella recommendations, and writes the result to `weather_table_silver`.

5. **Recommend**
   Summarises weather between 07:00 and 18:00, including:

   * Lowest apparent temperature
   * Highest apparent temperature
   * Clothing recommendation
   * Umbrella recommendation

   The result is stored in `weather_table_summary`.

6. **Notify**
   Renders `include/templates/weather_report.html` and emails the daily recommendation.

## Prerequisites

* Python 3.9+
* Apache Airflow or Astro CLI
* AWS account and configured credentials
* Terraform 1.x
* Existing S3 bucket for Terraform remote state
* Configured Airflow email backend

## Python Dependencies

```text
boto3
pandas
sqlalchemy
psycopg2-binary
python-dotenv
jinja2
apache-airflow
requests
```

Install them with:

```bash
pip install -r requirements.txt
```

## Setup

### 1. Provision the infrastructure

Create `terraform/terraform.tfvars`:

```hcl
db_username = "your_database_username"
db_password = "your_database_password"
my_ip       = "your_public_ip/32"
```

Run:

```bash
cd terraform
terraform init
terraform fmt
terraform validate
terraform plan -var-file="terraform.tfvars"
terraform apply -var-file="terraform.tfvars"
```

Terraform creates:

* An S3 bucket with versioning enabled
* An Amazon RDS PostgreSQL instance
* A security group allowing PostgreSQL access from `my_ip`

### 2. Configure environment variables

Create a `.env` file:

```env
DB_USER=<database_username>
DB_PASSWORD=<database_password>
DB_HOST=<rds_endpoint>
DB_PORT=5432
DB_NAME=weather_db
BUCKET_NAME=<s3_bucket_name>
AWS_DEFAULT_REGION=eu-central-1
NOTIFICATION_RECIPIENT=<recipient_email>
```

Do not commit `.env` or `terraform.tfvars`.

Recommended `.gitignore` entries:

```gitignore
.env
*.tfvars
*.tfstate
*.tfstate.*
.terraform/
```

### 3. Run with Astro

```bash
astro dev start
```

Open Airflow at:

```text
http://localhost:8080
```

Enable and trigger the `weather_pipeline` DAG.

## Schedule

The DAG runs daily using:

```python
schedule="@daily"
```

For a 05:00 daily run, use:

```python
schedule="0 5 * * *"
```

Set the Airflow timezone explicitly if the schedule must follow Berlin local time.

## Known Limitations

* Database tables currently use `if_exists="replace"`, so historical data is overwritten.
* The RDS instance is publicly accessible for development purposes.
* The weather-code table is loaded during every DAG run.
* The pipeline does not yet include automated data-quality checks.
