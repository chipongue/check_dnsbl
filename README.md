# check_dnsbl
Blacklists are one of the most popular tools to combat the growing problem of spam and phishing attempts by using the email. These lists are typically implemented in the form of DNS records. In this model, an email server is inserted in a blacklist by adding its IP address to a domain managed by the list in a format previously agreed.
To verify the reliability of a server, the Antispam tools query DNS by searching the server IP address in the format defined by the list. The content of the returned registry is irrelevant since its existence in DNS signals the server's presence on the blacklist. These lists are managed by private entities, and address-insertion policies are susceptible to failures and misleading interpretations of the sometimes legitimate behavior of e-mail servers.
Typically, messages sent by servers in blacklists are strongly rejected or marked as spam by the recipient's spam detection tools. The presence of a legitimate email server in a blacklist has a negative impact on the functioning of the institution, which is important to be aware and resolve as soon as possible.

This Nagios plugin monitors blacklists in search of a past IP address as an argument. By default, the plugin searches in 27 of the most popular blacklists, and can optionally be added to other lists, or ignored the set of predefined blacklists. This plugin signals the presence of the server IP address on at least one of the blacklists with the critical state.

Mandatory arguments: The following argument must be specified when the module is executed:
-H or – hostaddress used to specify e-mail address to send.

Optional arguments: The following arguments are optionally invoked, as required by the user:
-l or – list used to specify one or a set of blacklists.
-i or – ignore used to skip the blacklist pre installed. -I or – ignore, used to specify one or more black lists to be ignored.
-V or – version used to query the module version.
-A or – author used to query the author's data.

Command-Line Execution Example:
./check_dnsbl.py -H 198.224.42.133 -l zem.spamhaus.org,spam.abuse.ch

