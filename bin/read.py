import click

from edam.reader.models.database import recreate_database
from edam.reader.resolvers.resolver_factory import ResolverFactory
from edam import SERVER
from edam.utilities.decorators import timer
from edam.utilities.utilities import verify_database
from edam.viewer.app.views import app


@click.command()
@click.option('--input', 'input_file', required=True, help='input string')
@click.option('--template', required=True,
              help='template file to parse data with')
@click.option('--metadata', required=True,
              help='metadata file to annotate data with')
@click.option('--var', required=False, default="",
              help='Extra variables for URI generation')
@click.option('--drop', required=False, default='no',
              type=click.Choice(['yes', 'no']),
              help="Whether to drop stored data or not")
@timer
def cli(input_file, template, metadata, var, drop):
    if drop == "yes":
        recreate_database()

    factory = ResolverFactory(input_uri=input_file,
                              template=template,
                              metadata_file=metadata,
                              var=var)
    resolvers = factory.resolver
    # Workflow
    for resolver in resolvers:
        if resolver.template_matches_input():
            dataframes = resolver.timeseries
            resolver.store_timeseries()


if __name__ == '__main__':
    verify_database()
    cli()
