"""
CodeCraftHub - Personalized Learning Platform API
===================================================
A simple Flask REST API that lets developers track courses they want to learn.
Course data is stored in a local JSON file (no database needed).

Endpoints:
    POST   /api/courses          - Add a new course
    GET    /api/courses          - Get all courses
    GET    /api/courses/<id>     - Get a specific course by ID
    PUT    /api/courses/<id>     - Update an existing course
    DELETE /api/courses/<id>     - Delete a course
"""

import json
import os
from datetime import datetime

from flask import Flask, jsonify, request
from flask_cors import CORS

# ---------------------------------------------------------------------------
# App initialisation
# ---------------------------------------------------------------------------

# Create the Flask application instance
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) so that a browser-based
# frontend (served from a different origin) can call this API.
CORS(app)

# Path to the JSON file that stores all course data
COURSES_FILE = "courses.json"

# Valid status values that a course can have
VALID_STATUSES = ["Not Started", "In Progress", "Completed"]

# ---------------------------------------------------------------------------
# Helper functions – reading & writing the JSON data file
# ---------------------------------------------------------------------------


def load_courses():
    """
    Read courses from the JSON file and return them as a Python dictionary.

    If the file does not exist yet, create it with an empty list and return
    the initial structure.

    Returns:
        dict: A dictionary with a 'courses' key containing a list of courses
              and a 'next_id' key for the next auto-generated ID.
    """
    # If the file doesn't exist, create it with default empty data
    if not os.path.exists(COURSES_FILE):
        default_data = {"courses": [], "next_id": 1}
        save_courses(default_data)
        return default_data

    try:
        with open(COURSES_FILE, "r") as file:
            data = json.load(file)
            # Ensure the data has the expected structure
            if "courses" not in data:
                data["courses"] = []
            if "next_id" not in data:
                data["next_id"] = 1
            return data
    except (json.JSONDecodeError, IOError) as e:
        # If the file is corrupted or unreadable, return empty data
        print(f"Warning: Error reading {COURSES_FILE}: {e}")
        return {"courses": [], "next_id": 1}


def save_courses(data):
    """
    Write the courses data dictionary to the JSON file.

    Args:
        data (dict): The complete data dictionary to save.

    Raises:
        IOError: If the file cannot be written.
    """
    try:
        with open(COURSES_FILE, "w") as file:
            # indent=2 makes the JSON file human-readable
            json.dump(data, file, indent=2)
    except IOError as e:
        print(f"Error: Could not write to {COURSES_FILE}: {e}")
        raise


def find_course_by_id(courses, course_id):
    """
    Search the list of courses for one with the given ID.

    Args:
        courses (list): The list of course dictionaries.
        course_id (int): The ID to search for.

    Returns:
        dict or None: The matching course dictionary, or None if not found.
    """
    for course in courses:
        if course["id"] == course_id:
            return course
    return None


def validate_course_data(data, is_update=False):
    """
    Validate the incoming course data from a request.

    Checks that all required fields are present and that the status value
    is one of the allowed options.

    Args:
        data (dict): The request JSON body.
        is_update (bool): If True, all fields are optional (partial update).

    Returns:
        list: A list of error message strings. Empty if validation passed.
    """
    errors = []

    if not is_update:
        # For creating a new course, all fields are required
        required_fields = ["name", "description", "target_date", "status"]
        for field in required_fields:
            if field not in data or not str(data[field]).strip():
                errors.append(f"'{field}' is required and cannot be empty.")
    else:
        # For updating, check that provided fields are not empty
        for field in ["name", "description", "target_date", "status"]:
            if field in data and not str(data[field]).strip():
                errors.append(f"'{field}' cannot be empty if provided.")

    # Validate the status value if it's present in the request
    if "status" in data and data["status"] not in VALID_STATUSES:
        errors.append(
            f"Invalid status '{data['status']}'. "
            f"Must be one of: {', '.join(VALID_STATUSES)}."
        )

    # Validate date format if target_date is provided
    if "target_date" in data and data["target_date"]:
        try:
            datetime.strptime(data["target_date"], "%Y-%m-%d")
        except ValueError:
            errors.append(
                "Invalid 'target_date' format. Use YYYY-MM-DD (e.g. 2025-12-31)."
            )

    return errors


# ---------------------------------------------------------------------------
# API Endpoints – CRUD operations for courses
# ---------------------------------------------------------------------------


@app.route("/api/courses", methods=["POST"])
def create_course():
    """
    POST /api/courses
    Create a new course.

    Expects a JSON body with: name, description, target_date, status.
    Returns the newly created course with an auto-generated ID and timestamp.
    """
    # Check that the request contains JSON data
    if not request.is_json:
        return jsonify({
            "error": "Request must be JSON. Set Content-Type to application/json."
        }), 400

    data = request.get_json()

    # Validate the incoming data
    errors = validate_course_data(data)
    if errors:
        return jsonify({"error": "Validation failed", "messages": errors}), 400

    try:
        # Load the current courses from the file
        file_data = load_courses()

        # Build the new course object with an auto-generated ID and timestamp
        new_course = {
            "id": file_data["next_id"],
            "name": data["name"].strip(),
            "description": data["description"].strip(),
            "target_date": data["target_date"].strip(),
            "status": data["status"],
            "created_at": datetime.now().isoformat()
        }

        # Add the new course to the list and increment the next ID
        file_data["courses"].append(new_course)
        file_data["next_id"] += 1

        # Save the updated data back to the file
        save_courses(file_data)

        # Return the created course with a 201 Created status
        return jsonify({
            "message": "Course created successfully",
            "course": new_course
        }), 201

    except IOError:
        return jsonify({
            "error": "Failed to save course. Please try again."
        }), 500


@app.route("/api/courses", methods=["GET"])
def get_all_courses():
    """
    GET /api/courses
    Retrieve all courses.

    Returns a list of all courses stored in the JSON file.
    """
    try:
        file_data = load_courses()
        return jsonify({
            "courses": file_data["courses"],
            "total": len(file_data["courses"])
        }), 200
    except Exception as e:
        return jsonify({
            "error": f"Failed to retrieve courses: {str(e)}"
        }), 500


@app.route("/api/courses/<int:course_id>", methods=["GET"])
def get_course(course_id):
    """
    GET /api/courses/<id>
    Retrieve a specific course by its ID.

    Args:
        course_id (int): The ID of the course to retrieve.

    Returns the course if found, or a 404 error if not.
    """
    try:
        file_data = load_courses()
        course = find_course_by_id(file_data["courses"], course_id)

        if course is None:
            return jsonify({
                "error": f"Course with ID {course_id} not found."
            }), 404

        return jsonify({"course": course}), 200

    except Exception as e:
        return jsonify({
            "error": f"Failed to retrieve course: {str(e)}"
        }), 500


@app.route("/api/courses/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    """
    PUT /api/courses/<id>
    Update an existing course.

    Expects a JSON body with any of: name, description, target_date, status.
    Only provided fields will be updated.

    Args:
        course_id (int): The ID of the course to update.
    """
    # Check that the request contains JSON data
    if not request.is_json:
        return jsonify({
            "error": "Request must be JSON. Set Content-Type to application/json."
        }), 400

    data = request.get_json()

    # Validate the incoming data (partial updates allowed)
    errors = validate_course_data(data, is_update=True)
    if errors:
        return jsonify({"error": "Validation failed", "messages": errors}), 400

    try:
        file_data = load_courses()
        course = find_course_by_id(file_data["courses"], course_id)

        if course is None:
            return jsonify({
                "error": f"Course with ID {course_id} not found."
            }), 404

        # Update only the fields that were provided in the request
        if "name" in data:
            course["name"] = data["name"].strip()
        if "description" in data:
            course["description"] = data["description"].strip()
        if "target_date" in data:
            course["target_date"] = data["target_date"].strip()
        if "status" in data:
            course["status"] = data["status"]

        # Save the updated data back to the file
        save_courses(file_data)

        return jsonify({
            "message": "Course updated successfully",
            "course": course
        }), 200

    except IOError:
        return jsonify({
            "error": "Failed to update course. Please try again."
        }), 500


@app.route("/api/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    """
    DELETE /api/courses/<id>
    Delete a course by its ID.

    Args:
        course_id (int): The ID of the course to delete.
    """
    try:
        file_data = load_courses()
        course = find_course_by_id(file_data["courses"], course_id)

        if course is None:
            return jsonify({
                "error": f"Course with ID {course_id} not found."
            }), 404

        # Remove the course from the list
        file_data["courses"] = [
            c for c in file_data["courses"] if c["id"] != course_id
        ]

        # Save the updated data back to the file
        save_courses(file_data)

        return jsonify({
            "message": f"Course with ID {course_id} deleted successfully."
        }), 200

    except IOError:
        return jsonify({
            "error": "Failed to delete course. Please try again."
        }), 500


# ---------------------------------------------------------------------------
# Statistics endpoint
# ---------------------------------------------------------------------------


@app.route("/api/courses/stats", methods=["GET"])
def get_course_stats():
    """
    GET /api/courses/stats
    Retrieve statistics about all courses.

    Returns the total number of courses and a breakdown by status.
    """
    try:
        file_data = load_courses()
        courses = file_data["courses"]

        # Count courses by status
        status_counts = {status: 0 for status in VALID_STATUSES}
        for course in courses:
            if course["status"] in status_counts:
                status_counts[course["status"]] += 1

        return jsonify({
            "total_courses": len(courses),
            "by_status": status_counts
        }), 200

    except Exception as e:
        return jsonify({
            "error": f"Failed to retrieve stats: {str(e)}"
        }), 500


# ---------------------------------------------------------------------------
# Run the application
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Ensure the courses.json file exists when the app starts
    if not os.path.exists(COURSES_FILE):
        save_courses({"courses": [], "next_id": 1})
        print(f"Created {COURSES_FILE} with empty course list.")

    # Start the Flask development server
    # - debug=True enables auto-reload on code changes and detailed error pages
    # - port=5000 is the default Flask port
    print("=" * 60)
    print("  CodeCraftHub API is starting...")
    print("  Server: http://localhost:5000")
    print("  Endpoints:")
    print("    POST   /api/courses          - Create a course")
    print("    GET    /api/courses          - List all courses")
    print("    GET    /api/courses/<id>     - Get a course")
    print("    PUT    /api/courses/<id>     - Update a course")
    print("    DELETE /api/courses/<id>     - Delete a course")
    print("=" * 60)
    app.run(debug=True, port=5000)
