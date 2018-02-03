# bruce
One Command To Rule Them All

## Write a Brucefile
```Makefile
lint: flake8

test: pytest

+qa: lint test
```

## Execute commands
```shell
$ bruce lint
<flake8 output>
...
$ bruce +qa
<flake8 output>
<pytest output>
...
```

