import re

def compile_template(template: str, *args, **kwargs):
    """
    Compiles a given template with the given args and kwargs.

    For the following template: "This is a test of {something}"

    Any of these will work:
        - compile_template('This is a test of {something}, 'this_is_the_something_text')
        - compile_template('This is a test of {something}, something='this_is_the_something_text')

    :param template: string template
    :param args: arguments tuple
    :param kwargs: arguments dict
    :return: template with values format
    """
    data = kwargs.copy()
    keys = re.findall('([^{]+(?=}))', template)

    i = 0
    for k in keys:
        if k not in data.keys():
            data.update({k: args[i]})
            i += 1

    return template.format(**data)


