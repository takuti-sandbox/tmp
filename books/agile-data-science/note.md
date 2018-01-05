Agile Data Science 2.0
===

## Pipeline

1. **Event** - the JSON lines `.jsonl` format
  - Related to Apache Parquet *columnar* format
2. **Collector** - Kafka
3. **Bulk Storage** - HDFS/S3
4. **Batch Processing** - Spark (***PySpark***)
  - Internal pipelines are organized by ***Airframe***
  - What we do
    - Aggregate
    - Process
    - Publish (to distributed store)
5. **Distributed Store** - MongoDB
  - Sync with Spark by using ***pymongo_spark*** (part of ***mongo-hadoop*** project)
  - Here can be replaced with Elasticsearch to simply achieve scalability
    - Use ***pyelasticsearch***
6. **Application Server** - ***Flask***
  - Emit prediction event using ***kafka-python*** to:
    - Prediction model (i.e., Spark MLlib classifier) deployed with ***PySpark Streaming***
7. **Browser** - Render by the application server and visualize by D3.js

## Pyramid

The agile way - Make value from data in each step:

### Records - Collect, Display

- **Event** > **Collector**: Collect and serialize events in JSON
  1. Fetch raw data from ***Spark***
    - Aggregate them and check statistics
  2. Save records as gzipped JSON lines
    - `.toJSON()` for `.jsonl` file, or `.write.parquet()` for `.parquet` file
- **Batch Processing** > **Distributed Store**: Process and publish data
  1. Load the JSON lines data and publish them to ***MongoDB***
    - Browser now can display the records in the JSON format
  2. Implement GET request for single record with Flask and ***pymongo***
    - Render the result with ***Jinja2***
  3. Extend the GET endpoint and support listing records
    - Implement pagination at the same time // BAD - Is this book about introduction to web application? :(
  4. Support record search by using ***Elasticsearch***
    1. Create search index
    2. Publish records to Elasticsearch from Spark
    3. Implement search UI

### Charts - Clean, Aggregate, Visualize, Questions

- Choice of database and order form
  - Order form
    1. First order form
      - Find record via single, unique primary key
    2. Second order form
      - Key range scans like what Google Bigtable and its clone Apache HBase do
    3. Third order from
      - Summarize records in terms of e.g., time or category, and store the result in DB like MySQL or MongoDB
  - Lower order form is easier to scale horizontally
- Visualization
  1. Save aggregated statistics to MongoDB (= third order form)
  2. Implement new endpoints
    - Find MongoDB records
    - Render template which utilizes D3.js and visualize the records
  3. Enrich existing data by requesting and parsing external data source
    - Join the external data on tail number

### Reports - Structure, Link, Tag

- Raw data is always dirty!
- Grouping records (e.g., flight data is grouped by airlines)
  - Enable to see records from various aspects
    - e.g., airlines > flights
  - Create interesting, interconnected records: `key => {property1, property2, link => [key1, key2, key3]}`
- Enrich group information by using external data (e.g., Wikipedia abstract for description)
- Create a search widget with Elasticsearch, and put chart for visualization

### Predictions - Recommend, Learn

- Prep
  1. Explore target variable for regression and/or classification
  2. Load the JSON lines file and extract features (i.e., columns) with PySpark
- Regression with scikit-learn
  - If data does not fit to memory, sample records
  - Vectorize, train, test, evaluate the accuracy and visualize
- Classification with Spark MLlib
  - Handle large-scale data without sampling
  - Preprocess: Fill missing value, make buckets, ...
  - Vectorization: `pyspark.ml.feature`
  - Train, test, evaluate the accuracy
- Deploy predictive systems
  - Scikit-learn app as a web service
    - Save and load Python objects (model and vectorizer) as `.pkl` file using `sklearn.externals.joblib`
    - Create regress POST API -  Post record, apply transformation and predict by using the loaded vectorizer and regressor
    - Make UI to serve regression task
  - Spark ML app
    - Batch with Airflow
      - Save and load vectorizer (`StringIndexerModel` and `VectorAssembler`) and model (i.e., RandomForest classifier) by just hitting `.save()` method
      - Create classify POST API and its UI - Post record, apply feature transformation, **store prediction request** (= feature representation) **in Mongo**
      - Use ***pymongo-spark*** to fetch (daily) prediction requests from Mongo as Spark RDD, and save the requests on local as text file in the JSON format
      - Load Spark ML vectorizers and model + prediction task, and make prediction
      - Store the prediction result to a local JSON file
      - Save the result to MongoDB, and display on UI
      - All of the above steps can be automated using ***Airflow***
    - via Spark Streaming
      - Send prediction requests to Kafka
      - Create realtime_classify POST API - Post record, apply transformation and feed the request to Kafka producer (***kafka-python***) with task-specific UUID
      - Create response API; this API polls (waits) real-time response
        - UI shows something like "Processing..."
      - Spark Streaming connects to Kafka, and make classification for stream input from Kafka
      - Save the classification result to MongoDB
- Improve the accuracy of prediction by using different model, feature, data

### Actions - Derive value