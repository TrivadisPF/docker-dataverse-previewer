import click
import yaml
import requests
from jinja2 import Template

def remove_all_previewer(dataverse_url):
    url = f"{dataverse_url}/api/admin/externalTools"

    response = requests.get(url)

    if (response.status_code == 200):
        for tool in response.json()["data"]:
            if "preview" in tool["types"]:
                print (f"deleting tool {tool['displayName']}")
                response = requests.delete(url + "/" + str(tool["id"]))
                print(response.json()["status"])

def add_previewer(dataverse_url, data):

    # Data to send in JSON format
    payload_template = """
            {
                "displayName":"{{displayName}}",
                "description":"{{description}}",
                "toolName":"{{toolName}}",
                "scope":"file",
                "types":["preview"],
                "toolUrl":"{{toolUrl}}",
                "toolParameters": {
                    "queryParameters":[
                        {"fileid":"{fileId}"},
                        {"siteUrl":"{siteUrl}"},
                        {"datasetid":"{datasetId}"},
                        {"datasetversion":"{datasetVersion}"},
                        {"locale":"{localeCode}"}
                    ]
                    },
                {% if False %}    
                "requirements": {
                    "auxFilesExist": [
                        {
                            "formatTag": "NcML",
                            "formatVersion": "0.1"
                        }
                    ]
                },     
                {% endif %}            
                "contentType":"{{contentType}}",
                "allowedApiCalls": [
                    {
                    "name": "retrieveFileContents",
                    "httpMethod": "GET",
                    "urlTemplate": "/api/v1/access/datafile/{fileId}?gbrecs=true",
                    "timeOut": 3600
                    },
                    {
                    "name": "downloadFile",
                    "httpMethod": "GET",
                    "urlTemplate": "/api/v1/access/datafile/{fileId}?gbrecs=false",
                    "timeOut": 3600
                    },
                    {
                    "name": "getDatasetVersionMetadata",
                    "httpMethod": "GET",
                    "urlTemplate": "/api/v1/datasets/{datasetId}/versions/{datasetVersion}",
                    "timeOut": 3600
                    }
                ]
            }
            """
    
    # Create a Template object
    template = Template(payload_template)
    # Render the template with data
    payload = template.render(data)

    # Convert rendered template to a dictionary
    import json
    payload_dict = json.loads(payload)

    # Send the POST request
    url = f"{dataverse_url}/api/admin/externalTools"
    response = requests.post(url, json=payload_dict)

    # Checking the response status and printing the response
    if response.status_code == 200:
        print(f"Tool {payload_dict['displayName']} created successfully")
    else:
        print("Failed to create post:", response.status_code)    

def csv_option(ctx, param, value):
    return value.split(",") if value else [] 

@click.group()
def cli():
    """Main entry point for the CLI tool."""
    pass

@cli.command()
@click.option("--dataverse-url", required=True, help="The url of the dataverse server.", default="http://localhost:8080")
@click.option("--includes", callback=csv_option, help="a list of previewers to include.", default="")
@click.option("--excludes", callback=csv_option, help="a list of previewers to exclude.", default="")
@click.option("--remove-existing", is_flag=True, help="remove all existing previewers from the dataverse server.", default=False)
def deploy(dataverse_url, includes, excludes, remove_existing):

    if remove_existing:
        remove_all_previewer(dataverse_url)

    with open("./previewers.yaml", "r") as yaml_file:
        data = yaml.safe_load(yaml_file)
    
        for previewer in data["previewers"]:
            if (previewer in includes) or (not includes and previewer not in excludes):
                add_previewer (dataverse_url, data["previewers"][previewer])

@cli.command()
@click.option("--dataverse-url", required=True, help="The url of the dataverse server.", default="http://localhost:8080")
def remove(dataverse_url):
    click.echo(dataverse_url)
    remove_all_previewer(dataverse_url)

@cli.command()
def list():
    with open("./previewers.yaml", "r") as yaml_file:
        data = yaml.safe_load(yaml_file)

        COL_NAME = "name"
        COL_DESC = "description"
        click.echo(f"{COL_NAME:40}{COL_DESC}")
        click.echo("-------------------------------------------------------------------------------------------")
        for previewer in data["previewers"]:
            description = data["previewers"][previewer]["description"]
            click.echo(f"{previewer:40}{description}")

# Entry point for the CLI
if __name__ == "__main__":
    cli()
