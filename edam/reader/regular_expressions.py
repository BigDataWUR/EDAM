import re

variable_name = re.compile(r"{{(.*?)}}")
for_loop_variables = re.compile(r"{%\s?for (.*?) in (.*?)%}")
end_for_loop = re.compile(r"{%endfor%}")
template_file_header = r"((.*\n){1}){%\s?for.*%}"
# Below regex is for the case of same_timestamp(function) found in BoM template
same_timestamp_bom = re.compile(
    r"(same_timestamp)\s?\((?P<args>(?P<arg>[\w.]+(,\s?)?)+)\)")

# This var corresponds to observables which value is located in more than one columns
# In our templating language they are represented as:
# {{observable.value[0]}},{{observable.value[1]}}, etc.
# With that regex we are going to determine the existence of those observables
multicolumn_values_bom = re.compile(r"{{.*?\..*?(\[[0-9]\])*}}")

# For the following regex, line has to be split to ',' and then
# each individual var to be parsed with var_name
var_for_line = re.compile(r"{%\s?for .*? in .*?%}\n(.*)\n{%\s?endfor\s?%}")
var_parse_header = re.compile(r"(.*?)\n*{%\s?for .*? in .*?%}")

# var_anything_but_value = re.compile(r"{{.*?.value(.*?)}}")
# var_anything_but_value = re.compile(r"{{.+.value(\[.+\]).?.?}}")
var_for_value_timestamp = re.compile(r"{{.+.(timestamp.?)}}")
