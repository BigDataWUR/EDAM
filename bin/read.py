import click

from edam.reader.Workflow import Workflow
from edam.reader.manage import DatabaseInstantiation
from edam.reader.utilities import check_if_path_exists, identify_input_type, determine_storage_type
from edam.viewer.app.views import app
from edam.settings import SERVER
from datetime import datetime


@click.command()
@click.option('--input', required=True, help='input string')
@click.option('--query', required=False, help='SQL query')
@click.option('--template', required=True, help='template file to parse data with')
@click.option('--metadata', required=True, help='configuration file to annotate data with')
@click.option('--var', required=False, default="", help='Extra variables for URI generation')
@click.option('--storage', required=False, default='file', type=click.Choice(['file', 'memory']),
              help="Whether input files to be stored or not")
@click.option('--drop', required=False, default='no', type=click.Choice(['yes', 'no']),
              help="Whether to drop stored data or not")
def cli(input, template, query, metadata, var, storage, drop):
    now = datetime.now()
    if drop == "yes":
        # Dropping database
        DatabaseInstantiation(drop=True)
    else:
        DatabaseInstantiation(drop=False)
    
    template_path, template_object = handle_input_files(template)
    config_path, config_object = handle_input_files(metadata)
    
    success, inputs_path, file_type = identify_input_type(input_file=input, extra_variables=var,
                                                          template=template_path, template_object=template_object,
                                                          sql_query=query,
                                                          storage=determine_storage_type(storage_as_string=storage))
    if success:
        if not inputs_path:
            # It means template and input file does not match
            click.echo(f"I can't match template: {template_path} with input: {input}")
            exit(3)
        elif inputs_path:
            if template_path and config_path:
                mid_time = datetime.now()
                Workflow(input_list=inputs_path, template_file=template_object, configuration_file=config_object)
                end_time = datetime.now()
                print(f"Download all data: {mid_time - now}")
                
                print(f"Store all data: {end_time - mid_time}")
                print(f"Total time: {end_time - now}")
                # run()
            else:
                click.echo("No template or config were given")
        else:
            click.echo(f"{input} does not exist")
            exit(2)
        # run()
    else:
        click.echo(f"{input} does not exist")
        exit(4)


def handle_input_files(filename):
    if filename == "":
        # User didn't provide a template... Are we going to check every template?
        pass
    else:
        exists, file_type, file_path, file_object = check_if_path_exists(filename=filename)
        if exists:
            return file_path, file_object
        else:
            click.echo(f"{filename} does not exist")
            raise SystemExit(0)
            # raise Exception("File does not exit")


def run():
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host=SERVER['host'], port=SERVER['port'], debug=SERVER['debug'])


if __name__ == '__main__':
    cli()
