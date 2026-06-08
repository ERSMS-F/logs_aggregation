# Logs Aggregations

## How it works:

Ersms logging system uses loki logs stack. It consists of following 3 components:

- Alloy containers
- Loki system
- Graphana

Here is how it works

#### Alloy containers
On each node (each machine) on which our microservices are running, there is one alloy container. Alloy container attaches to all other docker containers stdout and stderr. It collects everything container prints, saves it temporary and sends to loki system.

#### Loki system
Loki saves logs, labels and filters them.

#### Graphana
Graphana connects to loki, allowing to visualize logs via dashboards.

### sum up
You don't need to do anything like `loki.log()` in your code. Simply print logs to stdout/stderr, loki will automatically collect them.


## What do change in your code?

In order for loki to be able to filter, label and aggregate your logs properly, you need to format them as one-line json string with following fileds:

- service name (e.g. 'messages')
- log level - intiger number between 1 and 100. Use following reference values:
    - 1 - debug info (e.g. `sent messsage to kafka`)
    - 20 - information of low importance (e.g. `generated notes for user of id 123`, `replied for http request with status 200`)
    - 40 - information of medium importance (e.g. `starting generating messages for all users`)
    - 60 - warning (e.g. `received user uuid are of version 1000, replying with failed status code`)
    - 80 - normal error (e.g. `notes generation via gemini failed. retrying again later`)
    - 100 - critical error (e.g. `unable to connect to database, exiting with code 1`)
- message - string with log message (e.g. `starting generating messages for all users`)

Below you can find exemplary log line:

```json
{"service":"notes","level": 40, "message":"starting generating messages for all users"}
```

Consider following exemplary file:
```python
# file ersms_logger.py
import json
import logging

__logger = logging.getLogger(__name__)

def log(erms_level: int, python_level: int, message: str):
    to_dump = {
        "service": "messages",
        "level": ersms_level,
        "message": message
    }
    __logger.log(python_level, json.dumps(to_dump, indent=None))

def debug(message: str):
    log(1, logging.DEBUG, message)

def info_low(message: str):
    log(20, logging.INFO, message)

def info_medium(message: str):
    log(40, logging.INFO, message)

def warning(message: str):
    log(60, logging.WARNING, message)

def normal_error(message: str):
    log(80, logging.ERROR, message)

def critical_error(message: str):
    log(100, logging.CRITICAL, message)
```

Now, all you need to do, is to replace
```pyton
# some code
print("message sent to user of id 123")
```
to
```python
import ersms_logger
# some code
ersms_logger.info_low("message sent to user of id 123")
```

## Notes

Loki consists one line as one log entry. Remember not to print multi-line logs. When using json dump, remember to set `indent=None` to avoid multi-line logs.


## Hot to start it?

Simply run `docker compose up`. Wait for the containers to start, then open `http://localhost:3000` in your browser. You should see grafana dashboard. (admin, admin).    
    
You can also run `docker compose -f demo/docker-compose.yml up` to start demo application, which will generate random logs for you to test the system.