import re  # import from regular expressions (RegEx) module to use findall(), compile() and sub() operations


def get_url_list(html_page):
    # regex used to find hyperlink (href) tags
    link_finder_regex = r'href=[\"\'](.*?)[\"\']'

    # use regex and return list of all links/href tags found in html page
    return re.findall(link_finder_regex, html_page)


def get_found_emails(html_page):
    # regex used to find emails in the format name@mail.com
    email_finder_regex = r'[A-Za-z0-9._!#$%&+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,3}'

    # use regex and return list of all emails found in html page
    return re.findall(email_finder_regex, html_page)


def get_found_phone_numbers(html_page):
    """ finds norwegian phone numbers by combining the regexes to find phone numbers which might also have the land code
    restrictions: first digit cannot be 0 or 1, nor can the first two digits of the phone number be 47 (?!47) since this
    might be part of the norwegian land code (+47) - the land_code_regex allows us to find this in front of numbers
    """
    # phone_finder_regex = r'(?!47)([2-9]\d\s\d{2}\s\d{2}\s\d{2})|([2-9]\d{2}\s\d{2}\s\d{3})'

    # regex to find norwegian land code used in phone numbers in the format +47 or 0047
    land_code_regex = r'(\+*47|[0]{2}47)'

    # regex to find norwegian phone numbers in the formats 23 45 67 89 or 234 56 789 (space sensitive between digits)
    phone_number_regex = r'((?!47)([2-9]\d\s\d{2}\s\d{2}\s\d{2})|([2-9]\d{2}\s\d{2}\s\d{3}))'

    # use combined regexes and return list of all (norwegian) phone numbers found in html page
    phone_finder_regex = land_code_regex + r'?\s*' + phone_number_regex  # r'?\s*' makes the land code part optional
    return re.findall(phone_finder_regex, html_page)


def get_found_html_comments(html_page):
    # use regex and return list of all comments found in html page
    comment_finder_regex = r'\<\!\-\-(?:.|\n|\r)*?-->'
    return re.findall(comment_finder_regex, html_page)


def get_found_special_data(html_page, user_regex):
    # use regex and return list of all special data found in html page
    return re.findall(user_regex, html_page)


def remove_html_tags(html_page):
    page = re.compile(r'<.*?>')
    return page.sub("", html_page)


def remove_string_punctuations(string):
    symbols_regex = r'[^\w\s]'  # regex to find punctuations (i.e. '.,!?')
    return re.sub(symbols_regex, "", string)  # subs regex match with an empty string
