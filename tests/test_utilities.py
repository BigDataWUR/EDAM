import os

import pytest

from edam.reader.models.Template import Template
from edam.settings import test_resources
from edam.utilities.utilities import remove_template_placeholders_from_string, \
    evaluate_variable_part, generate_uri


def test_get_observables_from_template_with_observables():
    template_path = os.path.join(test_resources, 'templates', 'Agmip.tmpl')
    template = Template(path=template_path)
    expected_observables = ["timestamp", "srad", "tmax", "tmin", "rain", "wind", "dewp", "vprs",
                            "rhum"]
    assert template.observable_ids == expected_observables


def test_get_observables_from_template_without_observables():
    template_path = os.path.join(test_resources, 'templates', 'doesnot.exist')
    template = Template(path=template_path)
    with pytest.raises(FileNotFoundError):
        template.observable_ids


def test_remove_template_placeholders_from_string():
    test_string1 = "longitude   =   {{station.longitude}}"
    separator = "({.*?}+)"
    test_output1 = remove_template_placeholders_from_string(test_string1, separator)
    desired_output1 = "longitude   =   "

    assert test_output1 == desired_output1

    test_string2 = "longitude   =   {{station.longitude}}, {{station.latitude}} this is test"
    test_output2 = remove_template_placeholders_from_string(test_string2, separator)
    desired_output2 = "longitude   =   "

    assert test_output2 == desired_output2


# def test_check_template_against_input_file():
#
#     test_template1 = "Yucheng.tmpl"
#     test_input1 = "Yucheng.met"
#     test_output1 = check_template_against_input_file(template_file=test_template1, data_input=test_input1)
#     desired_output1 = True
#
#     assert test_output1 == desired_output1


def test_evaluate_variable_part():
    test_variable1 = '{01-12}'
    test_output1 = evaluate_variable_part(test_variable1)
    desired_output1 = {
        '{01-12}': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']}

    assert test_output1 == desired_output1


def test_generate_uri_placeholders_in_group_correct():
    test_uri1 = "http://{2016-2017}{01-02}/IDCJDW2006.{2016-2017}{01-02}"
    test_output1 = generate_uri(test_uri1)
    desired_output1 = ['http://201601/IDCJDW2006.201601', 'http://201701/IDCJDW2006.201701',
                       'http://201602/IDCJDW2006.201602', 'http://201702/IDCJDW2006.201702']

    assert sorted(test_output1) == sorted(desired_output1)


def test_generate_uri_placeholders_correct():
    test_uri2 = "http://example.com/{01-02}-{2010-2011}"
    test_output2 = generate_uri(test_uri2)
    desired_output2 = ['http://example.com/01-2010', 'http://example.com/01-2011',
                       'http://example.com/02-2010',
                       'http://example.com/02-2011']

    assert sorted(test_output2) == sorted(desired_output2)


def test_generate_uri_placeholders_missing_value():
    test_uri2 = "http://example.com/{01}-{2010-2011}"
    desired_output2 = 'Range {0} is not correct in the correct format {starting_int - ending_int}'
    with pytest.raises(Exception) as excinfo:
        generate_uri(test_uri2)

        assert desired_output2 in str(excinfo.value)


def test_generate_uri_without_placeholder():
    test_uri3 = "http://example.com/"
    test_output3 = generate_uri(test_uri3)
    desired_output3 = ["http://example.com/"]

    assert sorted(test_output3) == sorted(desired_output3)


def test_generate_uri_extra_vars_correct():
    test_uri4 = 'http://example.com/{$var}'
    extra_vars = "1, 2, 3"
    test_output4 = generate_uri(test_uri4, static_variables=extra_vars)
    desired_output4 = ["http://example.com/1", "http://example.com/2", "http://example.com/3"]

    assert sorted(test_output4) == sorted(desired_output4)


def test_generate_uri_extra_vars_without_vars():
    test_uri4 = 'http://example.com/{$var}'
    with pytest.raises(AttributeError) as excinfo:
        generate_uri(test_uri4)
        assert "--extra parameter (static vars) was empty" in str(excinfo.value)


# def test_handle_input_parameter_correct():
#     # Tests an existing file
#     test_filename1 = os.path.join(test_resources, 'inputs', 'Agmip.csv')
#     test_output = handle_input_parameter(test_filename1)
#     desired_output1 = VerifiedInputParameter(path=test_filename1, parameter_type=InputType.FILE)

# assert test_output == desired_output1


# def test_handle_input_parameter_existing_folder():
#     # Tests an existing folder
#     test_filename3 = os.path.join(test_resources, 'inputs')
#     test_output3 = handle_input_parameter(test_filename3)
#     desired_output3 = VerifiedInputParameter(path=test_filename3, parameter_type=InputType.FOLDER)
#
#     assert test_output3 == desired_output3


# def test_determine_storage_type_correct():
#     test = 'file'
#     output = determine_storage_type(storage_as_string=test)
#     desired = StorageType.FILE
#     assert output == desired


# def test_determine_storage_type_wrong():
#     test = 'memory!'
#
#     with pytest.raises(SystemExit) as excinfo:
#         determine_storage_type(storage_as_string=test)
#         assert 'Wrong storage option' in str(excinfo.value)
