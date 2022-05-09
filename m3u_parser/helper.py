import asyncio
import csv
import ipaddress
import re
from typing import Union
from urllib.parse import urlsplit, urlunsplit

# URLValidator
ul = '\u00a1-\uffff'  # Unicode letters range (must not be a raw string).

# IP patterns
ipv4_re = r'(?:0|25[0-5]|2[0-4]\d|1\d?\d?|[1-9]\d?)(?:\.(?:0|25[0-5]|2[0-4]\d|1\d?\d?|[1-9]\d?)){3}'
ipv6_re = r'\[[0-9a-f:.]+\]'  # (simple regex, validated later)

# Host patterns
hostname_re = r'[a-z' + ul + r'0-9](?:[a-z' + ul + r'0-9-]{0,61}[a-z' + ul + r'0-9])?'
# Max length for domain name labels is 63 characters per RFC 1034 sec. 3.1
domain_re = r'(?:\.(?!-)[a-z' + ul + r'0-9-]{1,63}(?<!-))*'
tld_re = (
    r'\.'  # dot
    r'(?!-)'  # can't start with a dash
    r'(?:[a-z' + ul + '-]{2,63}'  # domain label
    r'|xn--[a-z0-9]{1,59})'  # or punycode label
    r'(?<!-)'  # can't end with a dash
    r'\.?'  # may have a trailing dot
)
host_re = '(' + hostname_re + domain_re + tld_re + '|localhost)'

regex = re.compile(
    r'^(?:[a-z0-9.+-]*)://'  # scheme is validated separately
    r'(?:[^\s:@/]+(?::[^\s:@/]*)?@)?'  # user:pass authentication
    r'(?:' + ipv4_re + '|' + ipv6_re + '|' + host_re + ')'
    r'(?::\d{1,5})?'  # port
    r'(?:[/?#][^\s]*)?'  # resource path
    r'\Z',
    re.IGNORECASE,
)
schemes = ['http', 'https', 'ftp', 'ftps']
unsafe_chars = frozenset('\t\r\n')
streams_regex = re.compile(r'acestream://[a-zA-Z0-9]+')


# get matching regex from content
def get_by_regex(regex, content: str) -> Union[str, None]:
    """Matches content by regex and returns the value captured by the first group, or None if there was no match

    :param regex: A compiled regex to match
    :type regex: re.Pattern
    :param content: The content on which the regex should be applied
    :type content: str
    :rtype: str, None
    """
    match = re.search(regex, content)
    return match.group(1).strip() if match else None


def is_dict(item: dict, ans: Union[None, list] = None) -> list:
    if ans is None:
        ans = []
    tree = []
    for k, v in item.items():
        if isinstance(v, dict):
            ans.append(str(k))
            tree.extend(is_dict(v, ans))
            ans = []
        else:
            if ans:
                ans.append(str(k))
                key = "_".join(ans)
                tree.extend([(key, str(v) if v else "")])
                ans.remove(str(k))
            else:
                tree.extend([(str(k), str(v) if v else "")])
    return tree


def get_tree(item: Union[list, dict]) -> list:
    tree = []
    if isinstance(item, dict):
        tree.extend(is_dict(item, ans=[]))
    elif isinstance(item, list):
        for i in item:
            tree.append(get_tree(i))
    return tree


def render_csv(header: list, data: list, out_path: str = "output.csv") -> None:
    input = []
    with open(out_path, "w") as f:
        dict_writer = csv.DictWriter(f, fieldnames=header)
        dict_writer.writeheader()
        for i in data:
            input.append(dict(i))
        dict_writer.writerows(input)


def ndict_to_csv(obj: list, output_path: str) -> None:
    """Convert nested dictionary to csv.

    :param obj: Stream information list
    :type obj: list
    :param output_path: Path to save the csv file.
    :return: None
    """
    tree = get_tree(obj)
    header = [i[0] for i in tree[0]]
    render_csv(header, tree, output_path)


def run_until_completed(coros):
    futures = [asyncio.ensure_future(c) for c in coros]

    async def first_to_finish():
        while True:
            await asyncio.sleep(0)
            for f in futures:
                if f.done():
                    futures.remove(f)
                    return f.result()

    while len(futures) > 0:
        yield first_to_finish()


# Django URLValidator
class ValidationError(Exception):
    pass


def punycode(domain):
    """Return the Punycode of the given domain if it's non-ASCII."""
    return domain.encode('idna').decode('ascii')


def regex_search(regex, value):
    regex_matches = regex.search(str(value))
    if not regex_matches:
        raise ValidationError


def is_valid_ipv6_address(ip_str):
    """
    Return whether or not the `ip_str` string is a valid IPv6 address.
    """
    try:
        ipaddress.IPv6Address(ip_str)
    except ValueError:
        return False
    return True


def is_valid_url(value):
    """
    Validate that the input can be represented as a URL.
    """
    try:
        if not isinstance(value, str):
            return False
        if unsafe_chars.intersection(value):
            return False
        scheme = value.split('://')[0].lower()
        if scheme not in schemes:
            return False

        try:
            splitted_url = urlsplit(value)
        except ValueError:
            return False

        try:
            regex_search(regex, value)
        except ValidationError:
            if value:
                scheme, netloc, path, query, fragment = splitted_url
                try:
                    netloc = punycode(netloc)
                except UnicodeError:
                    return False
                url = urlunsplit((scheme, netloc, path, query, fragment))
                regex_search(regex, url)
            else:
                return False
        else:
            # Now verify IPv6 in the netloc part
            host_match = re.search(r'^\[(.+)\](?::\d{1,5})?$', splitted_url.netloc)
            if host_match:
                potential_ip = host_match[1]
                if not is_valid_ipv6_address(potential_ip):
                    return False

        if splitted_url.hostname is None or len(splitted_url.hostname) > 253:
            return False
    except ValidationError:
        return False
    return True
