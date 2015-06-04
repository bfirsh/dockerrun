from dockerrun import Client

c = Client.from_env()
print c.run("ubuntu", "echo hello world")
