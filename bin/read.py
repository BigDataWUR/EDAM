import os
from datetime import datetime

import click

from edam.reader.Workflow import Workflow
from edam.reader.database import recreate_database
from edam.reader.models import Template, Metadata
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
@click.option('--drop', required=False, default='no', type=click.Choice(['yes', 'no']),
              help="Whether to drop stored data or not")
def cli(input, template, metadata, var, drop):
    now = datetime.now()
    if drop == "yes":
        recreate_database()
    else:
        pass

    factory = ResolverFactory(input_uri=input,
                              template=template,
                              metadata_file=metadata,
                              var=var)
    resolver = factory.resolver
    # Workflow
    if resolver.template_matches_input():
        pass


def run():
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host=SERVER['host'], port=SERVER['port'], debug=SERVER['debug'])


if __name__ == '__main__':
    cli()
