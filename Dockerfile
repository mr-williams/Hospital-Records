# Start from the Astro runtime
FROM quay.io/astronomer/astro-runtime:11.5.0

# Switch to root to install system packages
USER root

# Install OpenJDK 11, Ant, and essential tools without unnecessary extras
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        openjdk-11-jdk \
        ant \
        wget \
        ca-certificates \
        gnupg \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Optional: Set JAVA_HOME environment variable for PySpark
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# Switch back to astro user
USER astro

# Copy Python dependencies
COPY requirements.txt /usr/local/airflow/requirements.txt
RUN /usr/local/bin/install-python-dependencies
