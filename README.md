# Reddit Sentiment Analysis Pipeline

## Overview
This project establishes a robust, end-to-end pipeline for streaming Reddit comments in real-time, performing sentiment analysis on the collected data, storing the processed results in a structured data warehouse, and presenting actionable insights through interactive visualizations. The pipeline is architecturally designed to be highly scalable, fully automated, and capable of managing large volumes of data that evolve daily with a dynamic structure. By integrating a series of AWS services, the system ensures seamless data flow from ingestion to visualization, enabling comprehensive analysis of public sentiment expressed on Reddit.

## Architecture
The pipeline orchestrates a sequence of AWS services to ingest, process, store, and visualize Reddit comments, creating a cohesive system that transforms raw social media data into meaningful insights. Each component plays a critical role in the data journey, contributing to the overall efficiency and scalability of the solution. Below is a detailed high-level overview of the architecture:

- **PRAW & EC2**: PRAW, a Python Reddit API Wrapper, serves as the foundation for accessing Reddit’s vast repository of user-generated content. It enables the streaming of comments in real-time by interacting with Reddit’s API. An EC2 instance, acting as a compute resource, hosts a script that leverages PRAW to continuously collect comments from specified subreddits or topics of interest. The EC2 instance then forwards this stream of comments to a data streaming service, ensuring a steady flow of incoming data for downstream processing.

- **Kinesis Data Firehose**: The streaming service captures the continuous influx of Reddit comments from the EC2 instance. Designed for high-throughput data ingestion, it buffers the incoming data, batches it for efficiency, and reliably delivers it to a storage service designated for raw data. This service ensures that no data is lost during the ingestion phase, providing a dependable mechanism for handling real-time streams at scale.

- **Lambda**: A serverless function is activated whenever new raw data arrives in the storage service. This function processes each comment by invoking Amazon Comprehend, a natural language processing service, to perform sentiment analysis. Amazon Comprehend evaluates the emotional tone of the text, assigning a sentiment label—such as POSITIVE, NEGATIVE, NEUTRAL, or MIXED—and generating detailed sentiment scores that quantify the likelihood of each sentiment category. The processed data, now enriched with sentiment metadata, is then stored for further use.

- **S3**: The storage service provides a scalable, durable repository for both raw and processed data. Raw data, as received from the streaming service, is retained for archival purposes, ensuring that the original dataset remains available for future reference or reprocessing if needed. Processed data, which includes the sentiment analysis results, is stored separately in a structured format, ready for integration into the next stage of the pipeline. This dual-storage approach supports data integrity and flexibility in the workflow.

- **Glue**: An ETL (Extract, Transform, Load) service automates the process of discovering new processed data and integrating it into a data warehouse. Operating on a daily schedule, the service identifies newly arrived data in the storage service, extracts it, applies necessary transformations to align with the data warehouse schema, and loads it into the warehouse. This automation ensures that the pipeline remains up-to-date with the latest data without requiring manual intervention, making it highly efficient for handling dynamic datasets.

- **Redshift**: The data warehouse serves as the central repository for storing processed data in a structured, query-optimized format. It is designed to handle large-scale datasets, enabling fast and efficient querying for analytical purposes. The warehouse organizes the data in a way that supports complex queries, aggregations, and joins, making it an ideal backend for generating insights from the sentiment analysis results. Its scalability ensures that it can accommodate growing data volumes over time.

- **QuickSight**: Interactive dashboards in QuickSight connect directly to the data warehouse to visualize the sentiment analysis results. QuickSight transforms the structured data into meaningful visual representations, such as pie charts for sentiment distribution, line charts for tracking sentiment trends over time, and bar charts for comparing detailed sentiment scores across different categories. These visualizations provide a clear, intuitive way to explore public sentiment on Reddit, enabling stakeholders to derive actionable insights with ease.

## Pipeline Flow Diagram
Below is a diagram illustrating the high-level flow of data through the pipeline, from ingestion to visualization:

![Untitled Diagram drawio (1)](https://github.com/user-attachments/assets/bfa83f73-d45d-458b-a16d-2ccc5c00b612)


## High-Level Workflow
The pipeline operates as a seamless, automated system, with each stage building on the previous one to transform raw Reddit comments into insightful visualizations. The following steps outline the workflow in detail:

1. **Data Ingestion**:
   - PRAW establishes a connection to Reddit’s API, enabling the real-time streaming of comments from targeted subreddits or topics.
   - An EC2 instance runs a script that leverages PRAW to collect these comments continuously, ensuring a steady stream of data. The script forwards the collected comments to a streaming service, initiating the pipeline’s data flow.

2. **Data Streaming**:
   - The streaming service captures the incoming comments, buffering them to handle high volumes efficiently. It then delivers the batched data to a storage service designated for raw data, ensuring reliable ingestion without data loss, even during peak traffic periods.

3. **Data Processing**:
   - A serverless function is triggered automatically whenever new raw data arrives in the storage service. This function processes each comment individually, invoking Amazon Comprehend to perform sentiment analysis.
   - Amazon Comprehend analyzes the text of each comment, determining its emotional tone and assigning a sentiment label (e.g., POSITIVE, NEGATIVE, NEUTRAL, or MIXED). It also generates a set of sentiment scores, providing a probabilistic breakdown of the sentiment categories, which adds depth to the analysis.

4. **Data Storage**:
   - Raw data is preserved in the storage service for archival purposes, maintaining a complete record of the original dataset for potential future use, such as reprocessing or auditing.
   - Processed data, now enriched with sentiment labels and scores, is stored separately in the same storage service, structured to facilitate integration into the next stage of the pipeline.

5. **Data Integration**:
   - An ETL service operates on a daily schedule to discover new processed data in the storage service. It extracts the data, applies transformations to ensure compatibility with the data warehouse schema, and loads the transformed data into the warehouse, keeping the system up-to-date with minimal manual oversight.

6. **Data Warehousing**:
   - The data warehouse stores the processed data in a structured format, optimized for analytical querying. It supports efficient retrieval and aggregation of large datasets, enabling complex analyses such as time-series trends, sentiment distributions, and comparative studies of sentiment scores.

7. **Data Visualization**:
   - QuickSight establishes a connection to the data warehouse, accessing the structured data to create interactive dashboards. These dashboards feature a variety of visualizations, including:
     - A pie chart displaying the distribution of sentiment labels across the dataset.
     - A line chart tracking sentiment trends over time, revealing patterns in public opinion.
     - A bar chart comparing detailed sentiment scores across different sentiment categories, providing a granular view of emotional tone.
   - The visualizations enable stakeholders to explore the data interactively, uncovering insights into Reddit user sentiment with clarity and precision.
   - ![image](https://github.com/user-attachments/assets/be036e73-2a26-455e-aefb-bac7a6afbf57)


## Scalability Features
The pipeline incorporates several features to ensure scalability and efficiency as data volumes grow:

- **Automated Ingestion**: The ETL service ensures that new data is discovered and loaded into the data warehouse on a daily basis, seamlessly accommodating the dynamic nature of incoming data and reducing the need for manual intervention.
- **Optimized Storage**: The data warehouse is configured with distribution and sort strategies that optimize query performance, ensuring efficient data retrieval even as the dataset expands over time.
- **Scheduled Visualization Updates**: QuickSight dashboards are set to refresh daily, ensuring that the visualizations always reflect the most recent data, providing up-to-date insights without manual updates.

## Next Steps
- Explore the QuickSight dashboards to gain deeper insights into Reddit sentiment trends, identifying patterns such as shifts in public opinion or recurring themes in user comments.
- Consider enhancing the pipeline with advanced analytics, such as aggregating sentiment by specific time periods (e.g., daily or weekly trends) or applying natural language processing to identify key topics and entities within the comments.
- Monitor the pipeline’s performance and cost efficiency, ensuring that it continues to scale effectively as data volume increases, and optimizing resource usage to maintain cost-effectiveness.
