# Real Time Data Sync & Query

This is a Dockerized application that integrates **PostgreSQL**, **Redis**, **Debezium**, and **FastAPI** to provide efficient data processing and querying capabilities. It leverages change data capture **(CDC)** from Debezium to capture real-time updates from PostgreSQL and store them in Redis for fast access. The FastAPI framework serves as the API layer, exposing endpoints for querying database duplicates and providing autocomplete suggestions based on stored data.

## Table of Contents

- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Features](#features)
- [API Endpoints](#api-endpoints)
- [Sample Data](#sample-data)
- [License](#license)

## Technologies Used

- **PostgreSQL:** A powerful, open-source relational database system.
- **Redis:** An in-memory data structure store, used as a database, cache, and message broker.
- **Debezium:** A distributed platform for change data capture from various databases.
- **FastAPI:** A modern, fast (high-performance) web framework for building APIs with Python.

## Setup and Installation

### Prerequisites

Ensure you have the following installed:
- Docker
- Docker Compose

### Installation Steps

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/azizic98/realtime-data-sync-and-query.git
   cd realtime-data-sync-and-query
   ```
   
2. **Start the Docker Containers:**
    ```bash
    docker-compose up -d --build
    ```

2. **Access the Application:**

    - **FastAPI:** http://localhost:8000
    - **Redis Insights:** http://localhost:8001

## Features

### Real Time Data Sync (Debezium)
**Debezium** captures changes in PostgreSQL by reading from WALs and relays them to **Redis streams** for real-time data availability.

### Data Processing 
A consumer on **Redis streams** translates data into **Redis hashes** for efficient querying.

### Duplicate Querying
You can use **FastAPI** endpoints to query for duplicates within your data & since the data is stored in redis hashes, response time is insanely fast even for huge data sets.


## API Endpoints

### Check Duplicates

- **Description:** Query for duplicates in the database.
- **Method:** `POST`
- **URL:** `/check_duplicates`
- **Parameters:**
  - `table`: Name of the table to query duplicates from (e.g., "tbl_outlets").
  - `field`: Field in the table to check for duplicates (e.g., "email").
  - `value`: Value to check for duplicates (e.g., "rodneysmith@clark.com").

Example JSON Payload:
```json
{
    "table": "tbl_outlets",
    "field": "email",
    "value": "rodneysmith@clark.com"
}
```

Example JSON Respone:
```json
{
    "duplicates": [
        {
            "id": "30",
            "name": "Garcia and Sons",
            "email": "rodneysmith@clark.com"
        }
    ]
}
```

### Suggestions

- **Description:** Autocomplete suggestions for **outlet** names.
- **Method:** `GET`
- **URL:** `/autocomplete`
- **Parameters:**

    - **query** (required): The search term for autocomplete suggestions. It must be at least 1 character long.
    - **limit** (optional): Limits the number of suggestions returned. The default value is 5.

Example request:
```http
GET /autocomplete?query=A&limit=2 HTTP/1.1
```

Example Respone:
```json
[
    "Allen PLC",
    "Acosta LLC",
]
```

## Sample Data

To populate the database with sample data, follow these steps:

1. Access the Docker container running the PostgreSQL database:
   ```bash
   docker exec -it db bash
   ```

2.  Once inside the container, log in to PostgreSQL using the *postgres* user:
    ```bash
    psql -U postgres postgres
    ```

3. Import the fake_outlets data into the test.tbl_outlets table:
    ```bash
    \copy test.tbl_outlets(id,name,email,twitter,active) FROM /docker-entrypoint-initdb.d/fake_outlets.csv DELIMITER ',' CSV HEADER;
    ```
4. Import the fake_reporters data into the test.tbl_reporters table:
    ```bash
    \copy test.tbl_reporters(reporter_id,outlet_id,name,email,twitter,active) FROM /docker-entrypoint-initdb.d/fake_reporters.csv DELIMITER ',' CSV HEADER;
    ```

Once the above steps are completed , you can test the API Endpoints as shown [above](#api-endpoints)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.







