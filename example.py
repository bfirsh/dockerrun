import dockerrun

client = dockerrun.from_env()
print client.run("ubuntu", "echo hello world")
