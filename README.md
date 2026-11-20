# Attendance Management System — Automated Testing (UI & API)

An automated Software Quality Assurance (SQA) testing setup for a Flask-based Attendance Management System, covering end-to-end browser UI tests with **Robot Framework** and backend API tests with **REST Assured** and **JUnit**.

## Project Structure

```text
Attendance-SQA/
├── app.py                              # Flask web application and API server ([http://127.0.0.1:5000](http://127.0.0.1:5000))
├── attendance_e2e.robot                # Robot Framework end-to-end UI test suite (TC01–TC05)
├── pom.xml                             # Maven configuration for REST Assured and JUnit
├── src/
│   └── test/
│       └── java/
│           └── AttendanceApiTest.java  # REST Assured API test suite
└── results/                            # Generated Robot Framework reports and logs
