FROM quay.io/astronomer/astro-runtime:11.5.0

USER root

# Install OpenJDK-11
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get install -y ant && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64
ENV PATH $JAVA_HOME/bin:$PATH

# Copy and install Python requirements
COPY requirements.txt /usr/local/airflow/requirements.txt


RUN pip install --no-cache-dir -r /usr/local/airflow/requirements.txt


RUN /usr/local/bin/install-python-dependencies

USER astro