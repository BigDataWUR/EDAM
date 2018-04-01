import io
import logging
import re

from edam.reader.utilities import remove_template_placeholders_from_string


class Preprocess(object):
    """
    This class will produce 4 files of 2 types (data and preamble) if applicable.
    It identifies the case an input document has preamble, and created two separate
    files (_data, _preamble). Given that input and .tmpl documents have the same
    structure, this "split" process is applied to both input and .tmpl documents
    (thus, 4 documents in total).
    """
    
    def __init__(self, input_file, template_file):
        """
        
        :param input_file: Initial input file path (eg ~/inputs/Agmip.csv)
        :param template_file: Initial template file path (eg ~/templates/Agmip.tmpl)
        """
        self.preprocess_logger = logging.getLogger('edam.reader.Preprocess.Preprocess')
        self.input_file = input_file
        self.input_file.seek(0)
        self.template_file = template_file
        self.template_file.seek(0)
        
        self.header = ""
        self.extract_header_from_template()
        
        self.new_input_file_data = None
        self.new_input_file_preamble = None
        self.new_template_file_data = None
        self.new_template_file_preamble = None
        
        if self.header != "":
            self.new_template_file_data, self.new_template_file_preamble, \
            self.new_input_file_data, self.new_input_file_preamble = \
                self.split_preamble_from_data(self.template_file, self.input_file)
    
    def extract_header_from_template(self):
        var_header_from_template_file = r"((.*\n){1}){%\s?for.*%}"
        regex_header_from_template_file = re.compile(var_header_from_template_file)
        template_text = self.template_file.read()
        self.template_file.seek(0)
        matches = re.findall(regex_header_from_template_file, template_text)
        if matches:
            self.header = matches[0][0].strip("\r\n")
            self.preprocess_logger.debug('Header is: %s' % self.header)
        else:
            self.preprocess_logger.error('Template does not have header line')
            self.preprocess_logger.error('Maybe it is empty')
            self.preprocess_logger.error('Please check: %s' % self.template_file)
            raise SystemExit("Empty header line")
        
        self.template_file.seek(0)
    
    def split_preamble_from_data(self, template_file, input_file):
        # eg. py, pdf
        
        # Consider a header which contains placeholders
        # e.g "Speed of maximum wind gust (km/h)","Time of maximum wind gust",{{temp.timestamp.hour=9}}
        
        # Above header differs from template file to input file.
        # So we have two types of headers.
        # 1. template_header which is the above and
        # 2. input_header which is similar to template_header (in place of the placeholder we have something different
        self.template_header = self.header.strip('\n')
        header_without_placeholders = remove_template_placeholders_from_string(self.header).strip('\n')
        input_text = input_file
        for line in input_text.readlines():
            cleaned_line = line.strip('\n')
            if header_without_placeholders in cleaned_line or header_without_placeholders in cleaned_line.replace(' ',
                                                                                                                  ''):
                self.input_header = cleaned_line
                break
        
        # template_file_to_be_parsed_as_list_by_period = os.path.splitext(template_file)
        # input_file_to_be_parsed_as_list_by_period = os.path.splitext(input_file)
        
        template_data_file_text = template_file
        input_data_file_text = input_file
        
        template_file_text = template_file.read()
        template_file.seek(0)
        input_file.seek(0)
        input_file_text = input_file.read()
        input_file.seek(0)
        
        template_lines_before, _, template_lines_after = template_file_text.partition(self.template_header)
        input_lines_text_before, _, input_lines_text_after = input_file_text.partition(self.input_header)
        # TODO: I should probably insert an else statement here.
        # TODO: If there is no match, I could just rename the file to sth_data.sth
        
        # We can safely presume that the same condition verifies input text
        
        template_preamble_file_text = io.StringIO()
        input_preamble_file_text = io.StringIO()
        if template_lines_before != "":
            # Find preamble text and write file
            template_preamble_text = template_lines_before
            input_preamble_text = input_lines_text_before
            template_preamble_file_text.write(template_preamble_text)
            input_preamble_file_text.write(input_preamble_text)
            
            # Remove preamble text and save only data
            # We will use re.sub function
            # Preamble will be substituted by the header
            
            template_data_text = self.header + template_lines_after.replace(template_preamble_text, '')
            input_data_text = self.header + input_lines_text_after.replace(input_preamble_text, '')
            
            template_data_file_text = io.StringIO()
            input_data_file_text = io.StringIO()
            
            template_data_file_text.write(template_data_text)
            input_data_file_text.write(input_data_text)
        # That means document does not have a preamble
        template_data_file_text.seek(0)
        template_preamble_file_text.seek(0)
        input_data_file_text.seek(0)
        input_preamble_file_text.seek(0)
        
        return template_data_file_text, template_preamble_file_text, input_data_file_text, input_preamble_file_text


if __name__ == "__main__":
    test = Preprocess("inputs/Agmip.csv", "templates/Agmip.tmpl")
