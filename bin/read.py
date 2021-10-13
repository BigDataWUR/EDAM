import os
from datetime import datetime

import click

from edam.reader.Workflow import Workflow
from edam.reader.manage import create_tables, drop_tables
from edam.reader.models import Template, MetadataFile
from edam.reader.resolvers.ResolverFactory import ResolverFactory
from edam.settings import SERVER
from edam.utilities.utilities import identify_input_type, \
    determine_storage_type
from edam.viewer.app.views import app


@click.command()
@click.option('--input', required=True, help='input string')
@click.option('--template', required=True, help='template file to parse data with')
@click.option('--metadata', required=True, help='configuration file to annotate data with')
@click.option('--var', required=False, default="", help='Extra variables for URI generation')
@click.option('--storage', required=False, default='file', type=click.Choice(['file', 'memory']),
              help="Whether input files to be stored or not")
@click.option('--drop', required=False, default='no', type=click.Choice(['yes', 'no']),
              help="Whether to drop stored data or not")
def cli(input, template, metadata, var, storage, drop):
    now = datetime.now()
    if drop == "yes":
        drop_tables()
    else:
        create_tables()

    factory = ResolverFactory(input_uri=input,
                              template=template,
                              metadata_file=metadata,
                              var=var)
    resolver = factory.resolver
    # Workflow
    if resolver.template_matches_input():
        pass

    # if success:
    #     if not inputs_path:
    #         # It means template and input file does not match
    #         click.echo("I can't match template: %s with input: %s" % (template_path, input_file))
    #         exit(3)
    #     elif inputs_path:
    #         if template_path and config_path:
    #             mid_time = datetime.now()
    #             Workflow(input_list=inputs_path, template_file=template_object,
    #                      configuration_file=config_object)
    #             end_time = datetime.now()
    #             print("Download all data: %s" % (mid_time - now))
    #
    #             print("Store all data: %s" % (end_time - mid_time))
    #             print("Total time: %s" % (end_time - now))
    #             # run()
    #         else:
    #             click.echo("No template or config were given")
    #     else:
    #         click.echo("%s does not exist" % input_file)
    #         exit(2)
    #     # run()
    # else :
    #     click.echo("%s does not exist" % input_file)
    #     exit(4)


def run():
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host=SERVER['host'], port=SERVER['port'], debug=SERVER['debug'])


if __name__ == '__main__':
    cli()
