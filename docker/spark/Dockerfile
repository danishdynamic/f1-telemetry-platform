
FROM python:3.11-slim

# Java is required by Spark.
RUN apt-get update && \
    apt-get install -y --no-install-recommends openjdk-21-jre-headless && \
    rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Install Spark through PySpark.
RUN pip install --no-cache-dir pyspark==3.5.5

WORKDIR /opt/spark

CMD ["python", "/opt/spark/jobs/bronze_to_silver.py"]
