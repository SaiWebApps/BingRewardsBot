from browser_automation_utils.browser import AttributeType

def convert_result_to_uint(function):
    '''
        @description
            Convert the result(s) of the specified function to int(s).

        @param function
            Function whose output is being integer-ized (e.g., ['2','3']
            will be converted to [2,3])

        @return
            If function's output is a list, then convert each element
            to an int. Otherwise, just convert function output as is to int.
    '''
    def func_wrapper(*args, **kwargs):
        try:
            function_output = function(*args, **kwargs)
            # If the function result is a list, then de-stringify each
            # element in the list.
            if (type(function_output) == type([])):
                result = [int(elem) for elem in function_output]
            # Otherwise, it's just a single stringified number, so just
            # convert it back to to an int.
            else:
                result = int(function_output)
        except:
            result = int()
        return result
    return func_wrapper

def go_to_and_return_from(dest_url):
    '''
        @description
            Navigate to the specified url, execute the specified function,
            and then return to the original page.

        @param dest_url
            Url to navigate to before executing the function

        @param function
            Function to execute after navigating to dest_url

        @return
            The function's output as is
    '''
    def page_nav_decorator(function):
        def func_wrapper(*args, **kwargs):
            browser = args[0].browser
            orig_url = browser.get_current_url()
            # Go to destination.
            if orig_url != dest_url:
                browser.open(dest_url)
            # Execute function.
            function_output = function(*args, **kwargs)
            # Come back to source.
            if orig_url != dest_url:
                browser.open(orig_url)
            return function_output
        return func_wrapper
    return page_nav_decorator

def open_stats_iframe(function):
    def func_wrapper(*args, **kwargs):
        args[0].browser.click(AttributeType.Id, 'id_rc')
        args[0].browser.switch_into_iframe(AttributeType.Id, 'bepfm')
        function_output = function(*args, **kwargs)
        args[0].browser.switch_out_of_iframe()
        return function_output
    return func_wrapper