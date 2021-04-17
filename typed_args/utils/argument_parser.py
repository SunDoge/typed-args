from argparse import OPTIONAL, ZERO_OR_MORE, _


def get_positional_kwargs(**kwargs):
    # make sure required is not specified
    if 'required' in kwargs:
        # msg = _("'required' is an invalid argument for positionals")
        # raise TypeError(msg)
        del kwargs['required']

    # mark positional arguments as required if at least one is
    # always required
    if kwargs.get('nargs') not in [OPTIONAL, ZERO_OR_MORE]:
        kwargs['required'] = True
    if kwargs.get('nargs') == ZERO_OR_MORE and 'default' not in kwargs:
        kwargs['required'] = True

    # return the keyword arguments with no option strings
    return dict(kwargs, option_strings=[])


def get_optional_kwargs(*args, **kwargs):
    # determine short and long option strings
    option_strings = []
    long_option_strings = []
    for option_string in args:
        # error on strings that don't start with an appropriate prefix
        

        # strings starting with two prefix characters are long options
        option_strings.append(option_string)
        if option_string[0] in self.prefix_chars:
            if len(option_string) > 1:
                if option_string[1] in self.prefix_chars:
                    long_option_strings.append(option_string)

    # infer destination, '--foo-bar' -> 'foo_bar' and '-x' -> 'x'
    
    if dest is None:
        if long_option_strings:
            dest_option_string = long_option_strings[0]
        else:
            dest_option_string = option_strings[0]
        dest = dest_option_string.lstrip(self.prefix_chars)
        if not dest:
            msg = _('dest= is required for options like %r')
            raise ValueError(msg % option_string)
        dest = dest.replace('-', '_')

    # return the updated keyword arguments
    return dict(kwargs, dest=dest, option_strings=option_strings)
