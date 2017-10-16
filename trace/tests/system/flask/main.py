# Copyright 2017, OpenCensus Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys

import flask
import mysql.connector
import psycopg2
import sqlalchemy

from opencensus.trace.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.trace import config_integration
from opencensus.trace.reporters import google_cloud_reporter

INTEGRATIONS = ['mysql', 'postgresql', 'sqlalchemy']

DB_HOST = '127.0.0.1'

PROJECT = os.environ.get('GCLOUD_PROJECT_PYTHON')

# MySQL settings
MYSQL_PASSWORD = '12345'

# PostgreSQL settings
POSTGRES_PASSWORD = '12345'

app = flask.Flask(__name__)

# Enbale tracing, send traces to Stackdriver Trace
reporter = google_cloud_reporter.GoogleCloudReporter(project_id=PROJECT)
middleware = FlaskMiddleware(app, reporter=reporter)
config_integration.trace_integrations(INTEGRATIONS)


@app.route('/')
def hello():
    return 'hello'


@app.route('/mysql')
def mysql_query():
    # try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user='root',
            password=MYSQL_PASSWORD)
        cursor = conn.cursor()

        query = 'SELECT 2*3'
        cursor.execute(query)

        result = []

        for item in cursor:
            result.append(item)

        cursor.close()
        conn.close()

        return str(result)
    #
    # except Exception:
    #     msg = "Query failed. Check your env vars for connection settings."
    #     return msg, 500


@app.route('/postgresql')
def postgresql_query():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            user='postgres',
            password=POSTGRES_PASSWORD,
            dbname='postgres')
        cursor = conn.cursor()

        query = 'SELECT 2*3'
        cursor.execute(query)

        result = []

        for item in cursor.fetchall():
            result.append(item)

        cursor.close()
        conn.close()

        return str(result)

    except Exception:
        msg = "Query failed. Check your env vars for connection settings."
        return msg, 500


@app.route('/sqlalchemy-mysql')
def sqlalchemy_mysql_query():
    try:
        engine = sqlalchemy.create_engine(
            'mysql+mysqlconnector://{}:{}@{}'.format(
                'root', MYSQL_PASSWORD, DB_HOST))
        conn = engine.connect()

        query = 'SELECT 2*3'

        result_set = conn.execute(query)

        result = []

        for item in result_set:
            result.append(item)

        return str(result)

    except Exception:
        msg = "Query failed. Check your env vars for connection settings."
        return msg, 500


@app.route('/sqlalchemy-postgresql')
def sqlalchemy_postgresql_query():
    try:
        engine = sqlalchemy.create_engine(
            'postgresql://{}:{}@{}/{}'.format(
                'postgres', POSTGRES_PASSWORD,
                DB_HOST, 'postgres'))
        conn = engine.connect()

        query = 'SELECT 2*3'

        result_set = conn.execute(query)

        result = []

        for item in result_set:
            result.append(item)

        return str(result)

    except Exception:
        msg = "Query failed. Check your env vars for connection settings."
        return msg, 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True, use_reloader=False)
