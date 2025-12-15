## 📊 Spotify ETL Pipeline Project

This project implements an **ETL (Extract, Transform, Load) pipeline** using the **Spotify Web API**, with the goal of collecting, transforming, and analyzing music data in a structured and scalable way.

### 🔍 Project Overview

Data extraction was performed using a **sample of Rock and Metal artists**. These genres were intentionally selected to **limit data volume** while maintaining focus on the project’s objectives and ensuring efficient analytical modeling.

The ETL pipeline follows these steps:

### 1. Extract
- Data was extracted from the **Spotify Web API** using Python.
- Starting from a set of Rock and Metal artists, their **subgenres** were retrieved.
- Based on these subgenres, relevant **playlists** were identified and extracted.
- Finally, all **tracks contained in each playlist** were collected.
- The extracted data was initially stored using an **OBT (One Big Table)** approach.

### 2. Transform
- The OBT dataset was transformed into a **Star Schema**, optimized for analytical queries.
- Data cleaning, normalization, and transformation were performed using **Python and Pandas**.

### 3. Load
- The transformed data was loaded into a **PostgreSQL** relational database using **SQLAlchemy**.
- The following tables were created:

#### Dimension Tables
- `dim_artists`
- `dim_albums`
- `dim_tracks`
- `dim_playlists`

#### Fact Table
- `fact_playlist_tracks`

### 🛠️ Technologies Used
- Python
- Spotify Web API
- Requests
- Pandas
- PostgreSQL
- SQLAlchemy

### 📈 Analyses Performed
- Artist most frequently featured across all playlists
- Most common tracks appearing in playlists
- Longest playlist in terms of total track duration
- Album most represented across playlists

### 🎯 Project Purpose
This project demonstrates:
- End-to-end ETL pipeline development
- API-based data ingestion
- Dimensional modeling using a Star Schema
- Integration between Python and relational databases
- Analytical insight generation from music data
