dockerrun
=========

dockerrun is a dead simple Python library for running Docker commands. It does the thing you normally want to do with minimal hassle.

It works a bit like this:

```
>>> import dockerrun
>>> client = dockerrun.from_env()

>>> client.run("ubuntu", ["echo", "hello world"])
'hello world\n'

>>> client.run("ubuntu", ["cat", "missing"])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "dockerrun/client.py", line 54, in run
    self.logs(container, stdout=False, stderr=True)
dockerrun.client.ProcessError: Command 'cat missing' in image 'ubuntu' returned non-zero exit status 1: cat: missing: No such file or directory
```
