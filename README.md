# Nameko Worker Logger

A nameko dependency for logging with worker context 

## Intro

Nameko - is python framework for building microservices. Each microservice interacts with another using RabbitMQ message queue (or smth else). When application grows we need to collect logs from each service into one place (For example, database) and detect errors or incorrect behavior. Because each log message is a simple string line with state of the application, and log collector merge all logs (from each service) into one batch, we need to make several additional fields for uniquely deteminating the sender and its context. 

## Additional fields for each log message

- `service_name` - name of a service, which sends the log message
- `method_name` - name of a method, which executed by the service
- `call_id` (or correlation_id) - `uuid` of a call. It is unique identifier for each user's call in the system. It is used to find call correlation between log messages in the system.
  For example:
    - User call method `fn` of service `A`, log message will look like:
        ```json 
        { "service_name": "A", "method_name": "fn", "call_id": "uuid_of_that_call", "message": "A.fn invoked" }
        ```
    - And `A.fn` calls `B.another_fn`:
        ```json 
        { "service_name": "B", "method_name": "another_fn", "call_id": "uuid_of_that_call", "message": "B.another_fn invoked" }
        ```
    - Both log messages have the same `call_id` 

## Other features 

- Auto logging worker's exceptions by overriding `worker_result()` method

## How to use

Import the `WorkerLogger` and simply add the dependency into your service definition:

```python
from nameko.rpc import rpc
from nameko_worker_logger.dependencies import WorkerLogger


class MyService:
    name = 'my_service'
    log = WorkerLogger('myservice')

    #...

    @rpc
    def do_smth(self, payload: dict):
        self.log.info({ 'payload' : payload })
        # ...
        self.log.info('successfully finished')
```

## Adapt to ELK 

You can simply adapt your log messages to ELK by adding [pyhton_json_logger](https://github.com/madzak/python-json-logger) into your dependencies.
The sample of changes in your service's `config.yaml`:

```yaml
# ...
LOGGING:
  version: 1
  handlers:
    console:
      class: logging.StreamHandler
      formatter: jsonFormatter
  root:
    level: ERROR 
    handlers: [console]
  formatters:
    jsonFormatter:
      class: pythonjsonlogger.jsonlogger.JsonFormatter
      format: '%(name)s %(asctime)s %(levelname)s %(message)s'
      datefmt: '%d/%m/%Y %H:%M:%S'
```
