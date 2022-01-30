import pytest

from pytest_bdd import scenarios, given, when, then, parsers

# Constants

# Scenarios

scenarios('../features/csv.feature')


# Fixtures

@pytest.fixture
def browser():
    pass


# Given Steps

@given(parsers.parse('EDAM starts with "{input_file}","{metadata_file}" '
                     'and "{template_file}"'))
def step_impl(input_file, metadata_file, template_file):
    raise NotImplementedError(
        u'STEP: Given EDAM starts with Yucheng.met,yucheng.yml '
        u'and yucheng.tmpl')


# When Steps

# @given('the DuckDuckGo home page is displayed')
# def ddg_home(browser):
#     pass
#
#
# # Then Steps
#
# @when(parsers.parse('the user searches for "{phrase}"'))
# def search_phrase(browser, phrase):
#     search_input = browser.find_element_by_id('search_form_input_homepage')
#     search_input.send_keys(phrase + Keys.RETURN)
#
#
# @then(parsers.parse('results are shown for "{phrase}"'))
# def search_results(browser, phrase):
#     # Check search result list
#     # (A more comprehensive test would check results for matching phrases)
#     # (Check the list before the search phrase for correct implicit waiting)
#     links_div = browser.find_element_by_id('links')
#     assert len(links_div.find_elements_by_xpath('//div')) > 0
#     # Check search phrase
#     search_input = browser.find_element_by_id('search_form_input')
#     assert search_input.get_attribute('value') == phrase


@when("the user attempts to import data")
def step_impl():
    raise NotImplementedError(u'STEP: When the user attempts to import data')


@then('output contains "X" lines')
def step_impl():
    raise NotImplementedError(u'STEP: Then output contains "X" lines')
