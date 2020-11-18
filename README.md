# :computer: CLI client for the Shipyard system

[![codecov](https://codecov.io/gh/Varrrro/shipyard-cli/branch/master/graph/badge.svg?token=LTSBFD24GQ)](https://codecov.io/gh/Varrrro/shipyard-cli)

This command-line application lets you interact easily with a Shipyard server
instance. For more information about the Shipyard system, please check [the
server's repository](https://github.com/Varrrro/shipyard-server).

## Installation

You can install this tool by simply running:

```bash
pip install shipyard-cli
```

## Usage

By default, the application looks for the server on `localhost:8000`. If the server
is running on another host or port, you need to change the configuration by running:

```bash
shipyard config server_url 0.0.0.0
shipyard config server_port 8080
```

Once the correct values are set, you can begin managing your nodes, tasks and
deployments using the various commands. For example, to list all the nodes
present in your system you can run:

```bash
shipyard node ls
```

If you only want to see the nodes that are currently running tasks, you need to
use the `--active` flag.

```bash
shipyard node ls --active
```

Tasks can be added to the system by running:

```bash
shipyard task add TestName 1000 1000 1000 /path/to/tarfile

# Or, if you need to specify some devices
shipyard task add --device /dev/foo --device /dev/bar TestName 1000 1000 1000 /path/to/tarfile
```

Deploying tasks to nodes and removing them is as simple as using the `crane` command.

```bash
# Names can be used instead of IDs too
shipyard crane deploy node_id task_id
shipyard crane rm node_id task_id
```
