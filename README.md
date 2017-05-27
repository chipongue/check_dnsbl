# check_dnsbl
This Nagios plugin monitors blacklists in search of a past IP address as an argument. By default, the plugin searches in 27 of the most popular blacklists, and can optionally be added to other lists, or ignored the set of predefined blacklists. This plugin signals the presence of the server IP address on at least one of the blacklists with the critical state.
