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

[task:black]
cmd = venv/bin/black src/python --exclude venv bruce.py
watch = py
upstream = deps

[task:isort]
cmd = venv/bin/isort --skip venv -rc -y src/python bruce.py
watch = py
upstream = deps

[task:mypy]
cmd = venv/bin/mypy --strict src/python/bruce/*/*.py bruce.py
watch = py
upstream = black, isort

[group:qa]
upstream = mypy,black,isort
```

### Execute commands
```shell
$ ./bruce.py qa
...
```
