# NetGym API Usage Guide

This guide provides detailed documentation for the **NetGym Service** APIs.

**Base URL**: `http://localhost:8000`

---

## 🏥 Health Check

Check the status of the service and database connection.

### **GET** `/health`

**Response (200 OK):**

```json
{
  "status": "ok",
  "database": "connected"
}
```

---

## ⚾ Player Management

Manage baseball player statistics and information.

### 1. Get All Players

Retrieve a list of all players.

*   **Endpoint:** `GET /`
*   **Query Parameters:**
    *   `sort_by` (optional): Field to sort by (e.g., `hits`, `homeruns`).

**Request Example:**

```bash
curl -X 'GET' 'http://localhost:8000/?sort_by=homeruns'
```

**Response (200 OK):**

```json
{
  "success": true,
  "message": "Players retrieved successfully",
  "status_code": 200,
  "data": [
    {
      "name": "Aaron Judge",
      "position": "CF",
      "hits": 180,
      "homeruns": 62,
      "average": 0.311,
      "games": 157,
      "at_bats": 570,
      "runs": 133,
      "doubles": 28,
      "triples": 0,
      "rbi": 131,
      "walks": 111,
      "strikeouts": 175,
      "stolen_bases": 16,
      "caught_stealing": 3,
      "obp": 0.425,
      "slg": 0.686,
      "ops": 1.111
    }
  ]
}
```

### 2. Update Player details

Update specific fields for a player.

*   **Endpoint:** `PATCH /{name}`
*   **Path Parameters:**
    *   `name`: The name of the player to update (e.g., `Aaron Judge`).
*   **Body:** JSON object with fields to update.

**Request Example:**

```bash
curl -X 'PATCH' \
  'http://localhost:8000/Aaron%20Judge' \
  -H 'Content-Type: application/json' \
  -d '{
  "current_homeruns": 63,
  "current_hits": 181
}'
```

> **Note**: Fields correspond to the `PlayerRequestDTO` schema.

**Response (200 OK):**

```json
{
  "success": true,
  "message": "Player updated successfully",
  "status_code": 200,
  "data": {
    "name": "Aaron Judge",
    "position": "CF",
    "hits": 181,
    "homeruns": 63,
    "average": 0.311,
    ...
  }
}
```

---

## 🤖 AI Bio Generation

Generate creative biographies for players using AI.

### 1. Trigger Bio Generation

Start an asynchronous job to generate a bio for a player.

*   **Endpoint:** `POST /generate`
*   **Body:** Full player data object (fields from `PlayerResponseDTO`).

**Request Example:**

```bash
curl -X 'POST' \
  'http://localhost:8000/generate' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Shohei Ohtani",
  "position": "DH/P",
  "hits": 150,
  "homeruns": 44,
  "average": 0.304,
  "games": 135,
  "at_bats": 497,
  "runs": 102,
  "doubles": 26,
  "triples": 8,
  "rbi": 95,
  "walks": 91,
  "strikeouts": 143,
  "stolen_bases": 20,
  "caught_stealing": 6,
  "obp": 0.412,
  "slg": 0.654,
  "ops": 1.066
}'
```

**Response (202 Accepted):**

```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "PENDING"
}
```

### 2. Get Bio Status

Check the status or retrieve the result of a bio generation job.

*   **Endpoint:** `GET /{job_id}`
*   **Path Parameters:**
    *   `job_id`: The ID returned by the generate endpoint.

**Request Example:**

```bash
curl -X 'GET' 'http://localhost:8000/550e8400-e29b-41d4-a716-446655440000'
```

**Response (200 OK):**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "COMPLETED",
  "player_name": "Shohei Ohtani",
  "bio_content": "Shohei Ohtani, known as 'Shotime', is a generational talent redefining baseball..."
}
```
