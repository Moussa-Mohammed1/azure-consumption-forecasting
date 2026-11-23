# End-to-End Consumption Forecasting Pipeline on Microsoft Azure

An end-to-end cloud data engineering and machine learning solution built on Microsoft Azure for a fintech consumption forecasting system. This project implements automated data ingestion, immutable raw storage, data governance, time-series feature engineering, model training, and real-time inference deployment[cite: 1, 2].

---

## 1. Architecture & Azure Technology Stack

All cloud resources are provisioned in the **North Europe** region to maintain data residency and compliance[cite: 1, 2].

| Service / Tool | Role in Pipeline | Key Technical & AI-901 Concepts |
| :--- | :--- | :--- |
| **Azure Data Lake Storage (ADLS) Gen2** | Central repository storing raw, unmodified CSV files in `/raw/YYYY/MM/DD/`. | Built on Azure Blob Storage with **Hierarchical Namespace** enabled for true directory structures and fine-grained Access Control Lists (ACLs). |
| **Azure Data Factory (ADF)** | Orchestrates ingestion via a **Copy Data** activity and validates source CSV structure. | Serverless ETL/ELT service separating **Linked Services** (connections), **Datasets** (schemas), and **Pipelines** (execution workflows). |
| **Azure Machine Learning** | Manages Datastores, Datasets, Compute Clusters, and the Model Registry. | Uses a **Datastore** to securely connect to ADLS Gen2 and an autoscaling **Compute Cluster** to optimize compute costs. |
| **Azure ML Designer** | Visual drag-and-drop canvas for data cleaning, Python feature engineering, training, and deployment. | Separates the **Training Pipeline** (preprocessing, splitting, training, evaluation) from the **Real-Time Inference Pipeline** (live scoring endpoint). |

---

## 2. Azure Infrastructure Configuration

To ensure cost efficiency, reproducibility, and compliance with project specifications, resources are configured as follows[cite: 2]:

* **Region:** `North Europe`
* **Data Lake Directory Structure:** `/raw/YYYY/MM/DD/` (timestamped immutable landing zone)
* **Azure ML Compute Cluster:**
  * **Compute Type:** CPU
  * **Virtual Machine Size:** `StandardDS11v2` (2 vCPU, 14 GB RAM)
  * **Minimum Nodes:** `0` (scales to zero when idle)
  * **Maximum Nodes:** `1`
  * **Autoscale:** Enabled[cite: 2]

---

## 3. End-to-End Pipeline Workflow

### Phase 1: Ingestion & Storage (ADF + ADLS Gen2)
1. **Data Ingestion:** An Azure Data Factory pipeline uses a **Copy Data** activity to ingest source CSV files, validating schema and file format before writing[cite: 2].
2. **Data Lake Organization:** Raw data is landed untouched into `/raw/YYYY/MM/DD/` to preserve an auditable source of truth[cite: 2].

### Phase 2: Workspace & Dataset Setup (Azure ML Studio)
1. **Datastore Connection:** Configured an Azure ML Datastore pointing directly to the `/raw/` container in ADLS Gen2[cite: 2].
2. **Dataset Registration:** Created a tabular dataset from the Datastore referencing the ingested CSV files[cite: 2].

### Phase 3: Preprocessing & Feature Engineering (Azure ML Designer)
1. **Data Profiling & Cleaning:**
   * `Summarize Data`: Generates descriptive statistics to inspect distributions and anomalies[cite: 2].
   * `Clean Missing Data`: Applies time-series **interpolation** (or mean/median/row removal as appropriate) to handle missing values without breaking temporal continuity[cite: 2].
   * `Remove Duplicate Rows`: Deduplicates records based on key timestamp/entity identifiers[cite: 2].
   * `Edit Metadata`: Casts date/time strings into proper `DateTime` data types[cite: 2].
2. **Temporal Feature Engineering (`Execute Python Script`):**
   * Extracts time-series features from the `DateTime` column: `Hour`, `Daysofweek`, `Month`, `Quarter`, `Year`, and `Dayofyear`[cite: 2].

### Phase 4: Training, Evaluation & Deployment
1. **Feature Selection & Temporal Split:**
   * `Select Columns in Dataset`: Retains only relevant predictors and the target consumption variable[cite: 2].
   * `Split Data`: Performs a chronological **80% Train / 20% Test** split (non-random) to prevent data leakage in time-series forecasting[cite: 2].
2. **Model Training & Scoring:**
   * Trains a regression/forecasting algorithm using `Train Model` and generates test predictions via `Score Model`[cite: 2].
   * Evaluates accuracy using `Evaluate Model` (tracking MAE, RMSE, $R^2$)[cite: 2].
3. **Model Registration & Real-Time Inference:**
   * Registers the validated model in the Azure ML Model Registry (e.g., `forecastingmodelv1`)[cite: 2].
   * Converts the training graph into a **Real-Time Inference Pipeline**, automatically stripping out training/splitting modules while retaining `Import -> Feature Engineering -> Score Model`[cite: 2].

---

## 4. Data Governance, Catalog & GDPR Compliance

Aligned with **GDPR** and Microsoft **Responsible AI** principles (Privacy & Security, Transparency, Accountability)[cite: 1, 2]:

* **Data Minimization & Privacy:** Only columns strictly required for consumption forecasting are selected into the training pipeline; personally identifiable information (PII) is excluded or anonymized prior to modeling.
* **Access Control & Encryption:** ADLS Gen2 enforces encryption at rest and in transit, alongside Role-Based Access Control (RBAC) and folder-level ACLs.
* **Traceability & Data Lineage:** Every dataset version, Python transformation script, and registered model (`forecastingmodelv1`) is tracked in Azure ML Studio for full auditability[cite: 2].

### Data Catalog

| Dataset / Asset | Storage Path / Location | Format | Description | Retention / Governance Policy |
| :--- | :--- | :--- | :--- | :--- |
| **Raw Consumption Data** | `adls://.../raw/YYYY/MM/DD/*.csv` | CSV | Unmodified source consumption records landed via ADF. | Read-only (immutable); retained per GDPR audit schedule. |
| **Curated ML Dataset** | Azure ML Datasets (`consumption_raw`) | Tabular | Registered pointer to `/raw/` files for reproducible runs. | Version-controlled in Azure ML Workspace. |
| **Trained Model Artifact** | Azure ML Models (`forecastingmodelv1`) | Model | Serialized forecasting model trained on 80% historical split. | Registered with evaluation metrics and lineage tags. |

---

## 5. Repository Structure

```text
├── docs/
│   └── architecture-notes.md      # Detailed tool notes & AI-901 exam mappings
├── src/
│   └── feature_engineering.py     # Python script used in Azure ML Designer module
├── data-catalog/
│   └── catalog.md                 # Extended schema & lineage documentation
└── README.md                      # Project overview, setup, and governance