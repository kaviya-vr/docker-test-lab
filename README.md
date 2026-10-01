# Automated Docker Test Lab

A containerized test environment built with Docker Compose, Nginx, PostgreSQL, and Python. The project automatically validates service availability, database connectivity, and network ports, generates test reports, and runs the integration tests through GitHub Actions CI.

## Architecture

```text
                    Docker Compose
                          |
              +-----------+-----------+
              |                       |
              v                       v
        Nginx Web Server        PostgreSQL Database
           (web:80)                 (db:5432)
              |                       |
              +-----------+-----------+
                          |
                    Health Checks
                          |
                          v
                   Python Test Runner
                          |
              +-----------+-----------+
              |           |           |
              v           v           v
          HTTP Test    DB Test    Port Tests
                                      |
                                      v
                              Test Report (.txt)
```

## Technologies

- Docker
- Docker Compose
- Python 3.11
- Nginx
- PostgreSQL 15
- Git & GitHub
- GitHub Actions

## Automated Tests

The Python test runner performs the following checks:

1. **Web Server Check** – Sends an HTTP request to the Nginx service and verifies a successful response.
2. **Database Check** – Connects to PostgreSQL using `psycopg2`.
3. **Nginx Port Check** – Verifies that port `80` is reachable inside the Docker network.
4. **PostgreSQL Port Check** – Verifies that port `5432` is reachable.

The tester includes retry logic to handle temporary service startup delays.

## Docker Health Checks

Docker Compose health checks verify that Nginx and PostgreSQL are ready before the Python test runner starts.

PostgreSQL readiness is checked using:

```text
pg_isready
```

This prevents the test runner from attempting database connections before PostgreSQL is ready.

## Running Locally

### Prerequisites

Install:

- Docker Desktop
- Git

Clone the repository:

```bash
git clone https://github.com/kaviya-vr/docker-test-lab.git
cd docker-test-lab
```

Run the automated test environment:

```bash
docker compose up --build --abort-on-container-exit --exit-code-from tester
```

A successful run produces output similar to:

```text
Web Server Check: PASS - Nginx is reachable
Database Check: PASS - PostgreSQL is reachable
Port Check web:80: PASS - Port is open
Port Check db:5432: PASS - Port is open

All tests passed.
```

Clean up the environment:

```bash
docker compose down
```

## Test Reports

Each test execution generates a timestamped report in the `reports` directory.

Example:

```text
Automated Docker Test Lab Report
========================================

Web Server Check: PASS - Nginx is reachable
Database Check: PASS - PostgreSQL is reachable
Port Check web:80: PASS - Port is open
Port Check db:5432: PASS - Port is open
```

Generated reports are excluded from Git using `.gitignore`.

## Continuous Integration

GitHub Actions automatically runs the integration test environment for pushes and pull requests to the `main` branch.

The CI pipeline:

1. Checks out the repository.
2. Builds the Docker test environment.
3. Starts Nginx and PostgreSQL.
4. Waits for service health checks.
5. Runs the Python integration tests.
6. Generates the test report.
7. Uploads the report as a GitHub Actions artifact.
8. Cleans up the Docker environment.

If any automated test fails, the Python test runner exits with a non-zero exit code, causing the CI pipeline to fail.

## Project Structure

```text
docker-test-lab/
├── .github/
│   └── workflows/
│       └── docker-test.yml
├── test_runner/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── test_health.py
├── .gitignore
├── docker-compose.yml
└── README.md
```

## Key Learning Outcomes

This project demonstrates:

- Multi-container environments with Docker Compose
- Container networking and service discovery
- Docker health checks and service dependencies
- Automated infrastructure testing with Python
- HTTP, TCP port, and PostgreSQL connectivity testing
- Test report generation
- Exit-code based CI validation
- Continuous integration with GitHub Actions