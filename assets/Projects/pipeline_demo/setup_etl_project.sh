#!/bin/bash

# Define the project root directory
PROJECT_NAME="etl_pipeline_demo"
mkdir -p $PROJECT_NAME

# Create Airflow DAGs directory
mkdir -p $PROJECT_NAME/airflow/dags
mkdir -p $PROJECT_NAME/airflow/plugins
mkdir -p $PROJECT_NAME/airflow/config

# Create API data extraction module
mkdir -p $PROJECT_NAME/api_extraction
touch $PROJECT_NAME/api_extraction/__init__.py
touch $PROJECT_NAME/api_extraction/extract.py

# Create data transformation module
mkdir -p $PROJECT_NAME/transformation
touch $PROJECT_NAME/transformation/__init__.py
touch $PROJECT_NAME/transformation/transform.py

# Create database directory
mkdir -p $PROJECT_NAME/database
touch $PROJECT_NAME/database/schema.sql
touch $PROJECT_NAME/database/load_data.py

# Create scripts directory
mkdir -p $PROJECT_NAME/scripts
touch $PROJECT_NAME/scripts/setup_airflow.sh
touch $PROJECT_NAME/scripts/start_pipeline.sh

# Create Docker & environment configuration
mkdir -p $PROJECT_NAME/config
touch $PROJECT_NAME/config/.env
touch $PROJECT_NAME/docker-compose.yml
touch $PROJECT_NAME/requirements.txt
touch $PROJECT_NAME/README.md

# Populate README with basic project description
echo "# ETL Pipeline Demo" > $PROJECT_NAME/README.md
echo "This project demonstrates an ETL pipeline using Airflow to extract data from an API and load it into a SQL database." >> $PROJECT_NAME/README.md

# Notify user
echo "File structure for ETL pipeline created successfully!"