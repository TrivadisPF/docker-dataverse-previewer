# docker-dataverse-previewer

This GitHub project provides a Docker image which helps to automatically deploy Dataverse previewers to a working Dataverse installlation.

The functionality is implemented by a Python CLI supporting 4 different commands

```bash
(venv) > python3 dataverse-cli.py --help
Usage: dataverse-cli.py [OPTIONS] COMMAND [ARGS]...

  Main entry point for the CLI tool.

Options:
  --help  Show this message and exit.

Commands:
  deploy      Deploys specific or all supported previewers on the...
  list        List all the previewers currently installed on the...
  previewers  Shows all the previewers which can be installed.
  remove      Removes all the previewers currently installed on the...
```

## Running it through Docker

There is a docker image which can be used to easily run it.

### Show available previewers

```bash
docker run trivadis/dataverse-deploy-previewers:latest previewers
```

### List all the installed previewers

```bash
docker run  -e DATAVERSE_URL=http://192.168.1.115:28394 trivadis/dataverse-previewers:latest list
```

### Deploy previewers

The following command can be used to deploy some of/all supported previewers of the instance represented by the `DATAVERSE_URL`. The container will first check and wait for the instance to be available (important if used during bootstrapping).

```bash
docker run -ti -e DATAVERSE_URL=http://192.168.1.115:28394 -e PREVIEWERS_PROVIDER_URL=http://192.168.1.115:28395  -e REMOVE_EXISTING=true -e INCLUDE_PREVIEWERS="text,html" trivadis/dataverse-deploy-previewers:latest deploy
```

The following environment variables are supported

  * `DATAVERSE_URL` - the url of the Dataverse instance
  * `PREVIEWERS_PROVIDER_URL` - the url of the Dataverse Previewer
  * `INCLUDE_PREVIEWERS` - a comma-separted list of previewers to install. if left empty or not defined, then all previewers will be installed.
  * `EXCLUDE_PREVIEWERS` - a comma-spearted list of previewers to include from the install. Only applicable, if `INCLUDE_PREVIEWERS` is empty or not defined.
  * `REMOVE_EXISTING` - 


### Remove all previewers

The following command can be used to remove all the previewers of the instance represented by the `DATAVERSE_URL`. The container will first check and wait for the instance to be available (important if used during bootstrapping).

```bash
docker run -ti -e DATAVERSE_URL=http://192.168.1.115:28394 trivadis/dataverse-deploy-previewers:latest remove
```
