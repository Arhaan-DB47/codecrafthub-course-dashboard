# 🎓 CodeCraftHub — Personalized Learning Platform

> **IBM AI Developer Professional Certificate**
> Course 9: *Generative AI: Elevate your Software Development Career*
> Final Project — Part 1: Building the Backend REST API

A simple REST API that helps developers track courses they want to learn. Built with **Python** and **Flask**, storing data in a local JSON file — no database needed!


---

## 📖 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
  - [Create a Course](#1-create-a-course)
  - [Get All Courses](#2-get-all-courses)
  - [Get a Single Course](#3-get-a-single-course)
  - [Update a Course](#4-update-a-course)
  - [Delete a Course](#5-delete-a-course)
- [Testing with curl](#testing-with-curl)
- [Troubleshooting](#troubleshooting)

---

## Overview

**CodeCraftHub** is a beginner-friendly REST API project that demonstrates how to build CRUD (Create, Read, Update, Delete) operations using Python and Flask. It's designed for developers who are learning REST API basics for the first time.

Instead of using a database, all course data is stored in a simple `courses.json` file, making it easy to understand how data persistence works.

---

## Features

- ✅ **Full CRUD operations** — Create, Read, Update, and Delete courses
- 📁 **JSON file storage** — No database setup required
- 🔍 **Input validation** — Checks for required fields, valid status values, and date formats
- 🌐 **CORS enabled** — Frontend applications can connect from any origin
- 🆔 **Auto-generated IDs** — Each course gets a unique, incrementing ID
- ⏰ **Timestamps** — Courses are timestamped with their creation date
- ⚠️ **Error handling** — Clear, helpful error messages for invalid requests
- 💬 **Well-commented code** — Every function is documented for learners

---

## Project Structure

```
CodeCraftHub/
├── app.py              # Main Flask application with all API endpoints
├── courses.json        # JSON file where course data is stored
├── requirements.txt    # Python dependencies (Flask, Flask-CORS)
└── README.md           # This documentation file
```

| File               | Purpose                                               |
| ------------------ | ----------------------------------------------------- |
| `app.py`           | The Flask server with all CRUD routes and validation   |
| `courses.json`     | Auto-created JSON file that stores your course data    |
| `requirements.txt` | Lists the Python packages needed to run the project    |
| `README.md`        | Project documentation (you're reading it!)             |

---

## Prerequisites

Before you begin, make sure you have the following installed on your computer:

| Tool       | Minimum Version | Check Command        |
| ---------- | --------------- | -------------------- |
| **Python** | 3.8+            | `python --version`   |
| **pip**    | 20+             | `pip --version`      |
| **Git**    | Any             | `git --version`      |
| **curl**   | Any             | `curl --version`     |

> 💡 **Tip:** On Windows, Python 3 may use `python` instead of `python3`. Use whichever works on your system.

---

## Installation

Follow these steps to set up the project on your local machine:

### Step 1: Clone or navigate to the project directory

```bash
cd CodeCraftHub
```

### Step 2: (Optional) Create a virtual environment

A virtual environment keeps your project dependencies isolated:

```bash
# Create a virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

This installs:
- **Flask** — The web framework for building the API
- **Flask-CORS** — Enables Cross-Origin Resource Sharing for frontend access

---

## Running the Application

Start the Flask development server:

```bash
python app.py
```

You should see output like this:

```
============================================================
  CodeCraftHub API is starting...
  Server: http://localhost:5000
  Endpoints:
    POST   /api/courses          - Create a course
    GET    /api/courses          - List all courses
    GET    /api/courses/<id>     - Get a course
    PUT    /api/courses/<id>     - Update a course
    DELETE /api/courses/<id>     - Delete a course
============================================================
```

The API is now running at **http://localhost:5000** 🎉

> Press `Ctrl+C` to stop the server.

---

## API Endpoints

### Base URL

```
http://localhost:5000
```

### Course Object Structure

| Field          | Type   | Description                                        | Auto-generated? |
| -------------- | ------ | -------------------------------------------------- | --------------- |
| `id`           | int    | Unique course identifier                           | ✅ Yes          |
| `name`         | string | Name of the course                                 | ❌ No           |
| `description`  | string | Brief description of the course                    | ❌ No           |
| `target_date`  | string | Target completion date (YYYY-MM-DD)                | ❌ No           |
| `status`       | string | One of: `Not Started`, `In Progress`, `Completed`  | ❌ No           |
| `created_at`   | string | ISO 8601 timestamp of creation                     | ✅ Yes          |

---

### 1. Create a Course

**Endpoint:** `POST /api/courses`

**Request Body (JSON):**

```json
{
  "name": "Introduction to Python",
  "description": "Learn Python basics including variables, loops, and functions",
  "target_date": "2025-12-31",
  "status": "Not Started"
}
```

**Success Response (201 Created):**

```json
{
  "message": "Course created successfully",
  "course": {
    "id": 1,
    "name": "Introduction to Python",
    "description": "Learn Python basics including variables, loops, and functions",
    "target_date": "2025-12-31",
    "status": "Not Started",
    "created_at": "2025-07-05T12:00:00.000000"
  }
}
```

**Error Response (400 Bad Request) — Missing fields:**

```json
{
  "error": "Validation failed",
  "messages": ["'name' is required and cannot be empty."]
}
```

---

### 2. Get All Courses

**Endpoint:** `GET /api/courses`

**Success Response (200 OK):**

```json
{
  "courses": [
    {
      "id": 1,
      "name": "Introduction to Python",
      "description": "Learn Python basics including variables, loops, and functions",
      "target_date": "2025-12-31",
      "status": "Not Started",
      "created_at": "2025-07-05T12:00:00.000000"
    }
  ],
  "total": 1
}
```

---

### 3. Get a Single Course

**Endpoint:** `GET /api/courses/<id>`

**Success Response (200 OK):**

```json
{
  "course": {
    "id": 1,
    "name": "Introduction to Python",
    "description": "Learn Python basics including variables, loops, and functions",
    "target_date": "2025-12-31",
    "status": "Not Started",
    "created_at": "2025-07-05T12:00:00.000000"
  }
}
```

**Error Response (404 Not Found):**

```json
{
  "error": "Course with ID 999 not found."
}
```

---

### 4. Update a Course

**Endpoint:** `PUT /api/courses/<id>`

**Request Body (JSON):** *(only include fields you want to update)*

```json
{
  "status": "In Progress"
}
```

**Success Response (200 OK):**

```json
{
  "message": "Course updated successfully",
  "course": {
    "id": 1,
    "name": "Introduction to Python",
    "description": "Learn Python basics including variables, loops, and functions",
    "target_date": "2025-12-31",
    "status": "In Progress",
    "created_at": "2025-07-05T12:00:00.000000"
  }
}
```

---

### 5. Delete a Course

**Endpoint:** `DELETE /api/courses/<id>`

**Success Response (200 OK):**

```json
{
  "message": "Course with ID 1 deleted successfully."
}
```

**Error Response (404 Not Found):**

```json
{
  "error": "Course with ID 999 not found."
}
```

---

## Testing with curl

Open a **new terminal** (keep the server running in the first one) and run these commands:

### ✅ Test 1: Create a course

```bash
curl -s -X POST http://localhost:5000/api/courses -H "Content-Type: application/json" -d "{\"name\": \"Introduction to Python\", \"description\": \"Learn Python basics including variables, loops, and functions\", \"target_date\": \"2025-12-31\", \"status\": \"Not Started\"}"
```

**Expected:** 201 status, course object returned with `id: 1`.

### ✅ Test 2: Create a second course

```bash
curl -s -X POST http://localhost:5000/api/courses -H "Content-Type: application/json" -d "{\"name\": \"Flask REST APIs\", \"description\": \"Build REST APIs with Flask framework\", \"target_date\": \"2025-10-15\", \"status\": \"In Progress\"}"
```

**Expected:** 201 status, course object returned with `id: 2`.

### ✅ Test 3: Get all courses

```bash
curl -s -X GET http://localhost:5000/api/courses
```

**Expected:** 200 status, list of 2 courses, `total: 2`.

### ✅ Test 4: Get a specific course

```bash
curl -s -X GET http://localhost:5000/api/courses/1
```

**Expected:** 200 status, course with `id: 1`.

### ✅ Test 5: Update a course

```bash
curl -s -X PUT http://localhost:5000/api/courses/1 -H "Content-Type: application/json" -d "{\"status\": \"In Progress\"}"
```

**Expected:** 200 status, updated course with `status: "In Progress"`.

### ✅ Test 6: Delete a course

```bash
curl -s -X DELETE http://localhost:5000/api/courses/1
```

**Expected:** 200 status, confirmation message.

### ❌ Test 7: Error — Missing required fields

```bash
curl -s -X POST http://localhost:5000/api/courses -H "Content-Type: application/json" -d "{\"name\": \"Incomplete Course\"}"
```

**Expected:** 400 status, validation error listing missing fields.

### ❌ Test 8: Error — Invalid status

```bash
curl -s -X POST http://localhost:5000/api/courses -H "Content-Type: application/json" -d "{\"name\": \"Test\", \"description\": \"Test\", \"target_date\": \"2025-12-31\", \"status\": \"Unknown\"}"
```

**Expected:** 400 status, error about invalid status value.

### ❌ Test 9: Error — Course not found

```bash
curl -s -X GET http://localhost:5000/api/courses/999
```

**Expected:** 404 status, "Course with ID 999 not found."

---

## Troubleshooting

| Problem                                  | Solution                                                                                  |
| ---------------------------------------- | ----------------------------------------------------------------------------------------- |
| `ModuleNotFoundError: No module named 'flask'` | Run `pip install -r requirements.txt` to install dependencies                        |
| `Address already in use` (port 5000)     | Stop any other process on port 5000, or change the port in `app.py`                       |
| `courses.json` permission error          | Check file permissions; make sure the directory is writable                                |
| curl returns `Connection refused`        | Make sure the Flask server is running (`python app.py`)                                   |
| CORS errors in the browser               | Verify `flask-cors` is installed and `CORS(app)` is in `app.py`                          |
| `JSONDecodeError`                        | Delete `courses.json` and restart the server — it will recreate the file automatically    |
| Python command not found                 | Try `python3` instead of `python`, or check your PATH                                     |

---

> **Built as part of the IBM AI Developer Professional Certificate program on Coursera.**
> Course 9: *Generative AI: Elevate your Software Development Career* — Final Project (Part 1)
