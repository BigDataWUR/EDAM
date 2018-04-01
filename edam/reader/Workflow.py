import logging

from edam.reader.Preprocess import Preprocess
from edam.reader.SourceConfiguration import SourceConfiguration
from edam.reader.TemplateReader import TemplateReader
from edam.reader.utilities import determine_if_file_is_csv_or_not, StorageType


class Workflow(object):
    def __init__(self, input_list, template_file=None, configuration_file=None, storage=StorageType.FILE):
        self.logger = logging.getLogger('edam.reader.Workflow.Workflow')
        
        self.template_file = template_file
        self.configuration_file = configuration_file
        
        # I instantiate this to use it later.
        
        # input_file, template_file = find_input_template_from_config_file(config_file=self.configuration_file)
        for input_file in input_list:
            self.input_file = input_file
            # set_template_table()
            # firstly we are going to preprocess input and template file,
            # To identify if input doc and template have preamble
            
            # After above call input_file and template_file names will be updated
            # More specifically, input_file will become input_file_data (containing only data)
            # The same applies to the template_file (template_file -> template_file_data)
            
            # If input has preamble, two new files will be created:
            # input_file_preamble and template_file_preamble
            
            preprocess = Preprocess(input_file=self.input_file, template_file=self.template_file)
            # This MUST have a value
            self.input_data_file = preprocess.new_input_file_data
            self.template_data_file = preprocess.new_template_file_data
            # The followings could be None
            self.input_preamble_file = preprocess.new_input_file_preamble
            self.template_preamble_file = preprocess.new_template_file_preamble
            
            # We now have to determine if the _data document is in csv format
            # If not, we have to transform it to csv format (it was obvious, wasn't it?)
            # If it's not, the following method will try and convert it in csv
            # And overwrite the content in the same file name.
            self.input_data_file, self.template_data_file = determine_if_file_is_csv_or_not(self.input_data_file,
                                                                                            self.template_data_file)
            
            # Above call returns nothing, but it creates _data and _preamble (if applicable)
            # document files
            
            # In the configuration file, a user can define ONLY ONE STATION. This is a design choice which converges
            # with the most datasets we found and tested. In addition to the the previous,
            # in a configuration file a user
            # can define MORE THAN ONE observables (a station usually has a number of them),
            # MORE THAN ONE units of measurement
            # each observable should have one (or not, e.g. we have 3 observables which have the same uom). Also, a user
            # can define MORE THAN ONE sensors, usually each one for an observable.
            # However, there are cases wherein the exact
            # metadata about specific sensors are not known. In these cases, a user can create ONE GENERIC SENSOR and
            # define the required relationships (via 'relevant_observables' value).
            
            # What about the cases (eg. KNMI) a file contains an aggregated view of all available stations?
            # All stations observe the exact same observables,
            # which are observed from the very same sensors (not in the same
            # location, though). And all observables are represented with the very same uoms.
            config = SourceConfiguration(input_yaml=self.configuration_file,
                                         input_file_data=self.input_data_file,
                                         template_preamble=self.template_preamble_file,
                                         input_preamble=self.input_preamble_file)
            
            # Important questions.
            # 1. What to expect in the preamble?
            # 2. How are we going to represent multiple stations? Consider the knmi data input. Let's somehow assume
            # that we parsed stations in the preamble. When are we going to create the helperTable??
            # This table is a quick and cheap way to keep track of observations,
            # so as each observations is self-describable.
            #
            # We are now ready to call the template reader class.
            # try:
            TemplateReader(config=config, input_file=self.input_data_file, template=self.template_data_file)
            # except Exception as e:
            #     self.logger.error("Exception: %s %s" % (type(e).__name__, str(e)))
            self.input_data_file.close()
            self.input_file.close()


if __name__ == "__main__":
    pass
    # t = Workflow()
