# Pipeline Pulse

Pipeline Pulse is a Python command-line tool that checks whether a web server is responding. It requests `/health`, retries while the server starts, and returns an exit code that GitLab CI uses to pass or fail the job.

I built this project to practice Python scripting, troubleshoot a CI job, and turn a manual check into a repeatable pipeline step.

## Run locally

You need Python 3 and curl. The script uses `curl.exe` on Windows and `curl` on Linux.

1. Start the server from the repository directory.

   ```powershell
   python -m http.server 8000 --bind 127.0.0.1
   ```

2. Open a second terminal and run the checker. Pass the base URL. The script appends `/health`.

   ```powershell
   python healthcheck.py http://127.0.0.1:8000
   ```

The home page is available at `http://127.0.0.1:8000/`. The `/health` endpoint serves the `health` file from the repository.

## Test the failure cases

| Scenario | What happens | Exit code |
| --- | --- | --- |
| The server is running and the `health` file is present | `/health` returns HTTP `200` | `0` |
| The `health` file is temporarily renamed | `/health` returns HTTP `404` | `1` |
| The server is stopped | curl reports a connection error | `1` |

The checker makes up to four attempts, with three seconds between failed attempts. In PowerShell, run `$LASTEXITCODE` after the checker to see its exit code.

## GitLab CI

The `healthcheck-job` uses a Python 3.12 image and starts the web server in the background inside the job container. It then runs the same checker against `127.0.0.1:8000`. If all four attempts fail, the script exits with `1` and GitLab marks the job as failed. Curl must be available in the job image.

The check verifies that the server can serve the static `/health` file. It uses `curl --fail`, so HTTP responses with status codes of `400` or higher count as failures.