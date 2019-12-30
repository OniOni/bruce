# Bruce
One Command To Rule Them All

## Getting Started

### Write a Bruce.ini
```ini
[glob:py]
glob = **/*.py
exclude = .*venv.*,\.bruce/.*

[file:reqs]
path = requirements.txt

[file:venv]
path = venv

[task:clean]
cmd = rm -rf venv/ __pycache__/ build/ dist/ *egg*
watch = venv

[task:init]
cmd = python3 -m venv venv
watch = venv

[task:deps]
cmd = venv/bin/pip install -r requirements.txt
watch = reqs
upstream = init
```

### Execute commands
```shell
$ ./bruce.py <command>
...
```
