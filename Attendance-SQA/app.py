from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# 1. Sample student roster and in-memory attendance list
students = {
    "101": "Aarav",
    "102": "Divya",
    "103": "Rohan",
}
attendance_records = []

# 2. Browser UI template for End-to-End (Robot Framework) testing
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head><title>Attendance Portal</title></head>
<body>
  <h2>Attendance Management System</h2>
  <form method="POST" action="/mark-ui">
    <label>Student ID:</label>
    <input type="text" id="student_id" name="student_id" />
    <button type="submit" id="submit_btn">Mark Present</button>
  </form>
  <p id="message">{{ message }}</p>
  <h3>Marked Attendance (<span id="count">{{ records|length }}</span>)</h3>
  <ul id="record_list">
    {% for r in records %}
      <li>{{ r.student_id }} - {{ r.name }} ({{ r.status }})</li>
    {% endfor %}
  </ul>
</body>
</html>
"""
# (Note: removing 'required' on <input> lets empty submissions reach /mark-ui so TC05 can test blank input!)


# 3. UI Routes
@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_PAGE, message="", records=attendance_records)


@app.route("/mark-ui", methods=["POST"])
def mark_ui():
    sid = request.form.get("student_id", "").strip()
    if not sid:
        return render_template_string(
            HTML_PAGE,
            message="Error: Student ID is required",
            records=attendance_records,
        )
    if sid not in students:
        return render_template_string(
            HTML_PAGE,
            message="Error: Invalid Student ID",
            records=attendance_records,
        )
    if any(r["student_id"] == sid for r in attendance_records):
        return render_template_string(
            HTML_PAGE,
            message="Error: Attendance already marked",
            records=attendance_records,
        )

    attendance_records.append(
        {"student_id": sid, "name": students[sid], "status": "Present"}
    )
    return render_template_string(
        HTML_PAGE,
        message="Success: Attendance marked",
        records=attendance_records,
    )


# 4. REST API Routes
@app.route("/api/attendance", methods=["GET"])
def get_attendance():
    return jsonify({"total": len(attendance_records), "records": attendance_records}), 200


@app.route("/api/attendance", methods=["POST"])
def mark_attendance_api():
    data = request.get_json(silent=True) or {}
    sid = str(data.get("student_id", "")).strip()
    if not sid:
        return jsonify({"error": "Student ID is required"}), 400
    if sid not in students:
        return jsonify({"error": "Invalid Student ID"}), 404
    if any(r["student_id"] == sid for r in attendance_records):
        return jsonify({"error": "Duplicate attendance entry"}), 400

    record = {"student_id": sid, "name": students[sid], "status": "Present"}
    attendance_records.append(record)
    return jsonify({"message": "Attendance marked", "record": record}), 201


@app.route("/api/reset", methods=["POST"])
def reset():
    attendance_records.clear()
    return jsonify({"message": "Reset complete"}), 200


# 5. Start Flask server on port 5000
if __name__ == "__main__":
    app.run(port=5000)