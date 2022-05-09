<h1 align="center">Welcome to m3u_parser</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-0.2.0-blue.svg?cacheSeconds=2592000" />
</p>

> A parser for m3u files.
> It parses the contents of m3u file to a list of streams information which can be saved as a JSON/CSV file.

> > Check [go-m3u-parser](https://github.com/pawanpaudel93/go-m3u-parser) and [ts-m3u-parser](https://github.com/pawanpaudel93/ts-m3u-parser) also.

### 🏠 [Homepage](https://github.com/pawanpaudel93/m3u_parser)

## Install

> pip install m3u-parser

OR

> pipenv install m3u-parser

## Example

```python
from m3u_parser import M3uParser
url = "/home/pawan/Downloads/ru.m3u"
useragent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
parser = M3uParser(timeout=5, useragent=useragent)
parser.parse_m3u(url)
parser.remove_by_extension('mp4')
parser.filter_by('status', 'GOOD')
print(len(parser.get_list()))
parser.to_file('pawan.json')
```

## Usage

```python
from m3u_parser import M3uParser
url = "/home/pawan/Downloads/ru.m3u"
useragent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
parser = M3uParser(timeout=5, useragent=useragent)
```

> Functions

```python
def parse_m3u(self, path: str, check_live: bool = True, enforce_schema: bool = False):
        """Parses the content of local file/URL.

        It downloads the file from the given url or use the local file path to get the content and parses line by line
        to a structured format of streams information.

        :param path: Path can be a url or local filepath
        :type path: str
        :param enforce_schema: If the schema is forced, non-existing fields in a stream are filled with None/null. If it is not enforced, non-existing fields are ignored
        :type enforce_schema: bool
        :param check_live: To check if the stream links are working or not
        :type check_live: bool
        :rtype: None
        """

def filter_by(self, key: str, filters: Union[str, list], key_splitter: str = "-", retrieve: bool = True, nested_key: bool = False):
        """Filter streams infomation.

        It retrieves/removes stream information from streams information list using filter/s on key.

        :param key: Key can be single or nested. eg. key='name', key='language-name'
        :type key: str
        :param filters: List of filter/s to perform the retrieve or remove operation.
        :type filters: str or list
        :param key_splitter: A splitter to split the nested keys. Default: "-"
        :type key_splitter: str
        :param retrieve: True to retrieve and False for removing based on key.
        :type retrieve: bool
        :param nested_key: True/False for if the key is nested or not.
        :type nested_key: bool
        :rtype: None
        """

def reset_operations(self):
        """Reset the stream information list to initial state before various operations.

        :rtype: None
        """

def remove_by_extension(self, extension: Union[str, list])
        """Remove stream information with certain extension/s.

        It removes stream information from streams information list based on extension/s provided.

        :param extension: Name of the extension like mp4, m3u8 etc. It can be a string or list of extension/s.
        :type extension: str or list
        :rtype: None
        """

def retrieve_by_extension(self, extension: Union[str, list]):
        """Select only streams information with a certain extension/s.

        It retrieves the stream information based on extension/s provided.

        :param extension: Name of the extension like mp4, m3u8 etc. It can be a string or list of extension/s.
        :type extension: str or list
        :rtype: None
        """

def remove_by_category(self, filter_word: Union[str, list]):
        """Removes streams information with category containing a certain filter word/s.

        It removes stream information based on category using filter word/s.

        :param filter_word: It can be a string or list of filter word/s.
        :type filter_word: str or list
        :rtype: None
        """

def retrieve_by_category(self, filter_word: Union[str, list]):
        """Retrieve only streams information that contains a certain filter word/s.

        It retrieves stream information based on category/categories.

        :param filter_word: It can be a string or list of filter word/s.
        :type filter_word: str or list
        :rtype: None
        """

def sort_by(self, key: str, key_splitter: str = "-", asc: bool = True, nested_key: bool = False):
        """Sort streams information.

        It sorts streams information list sorting by key in asc/desc order.

        :param key: It can be single or nested key.
        :type key: str
        :param key_splitter: A splitter to split the nested keys. Default: "-"
        :type key_splitter: str
        :param asc: Sort by asc or desc order
        :type asc: bool
        :param nested_key: True/False for if the key is nested or not.
        :type nested_key: bool
        :rtype: None
        """

def get_json(self, indent: int = 4):
        """Get the streams information as json.

        :param indent: Int value for indentation.
        :type indent: int
        :return: json of the streams_info list
        :rtype: json
        """

def get_list(self):
        """Get the parsed streams information list.

        It returns the streams information list.

        :return: Streams information list
        :rtype: list
        """

def get_random_stream(self, random_shuffle: bool = True):
        """Return a random stream information

        It returns a random stream information with shuffle if required.

        :param random_shuffle: To shuffle the streams information list before returning the random stream information.
        :type random_shuffle: bool
        :return: A random stream info
        :rtype: dict
        """

def to_file(self, filename: str, format: str = "json"):
        """Save to file (CSV, JSON, or M3U)

        It saves streams information as a CSV, JSON, or M3U file with a given filename and format parameters.

        :param filename: Name of the file to save streams_info as.
        :type filename: str
        :param format: csv/json/m3u to save the streams_info.
        :type format: str
        :rtype: None
        """
```

## Author

👤 **Pawan Paudel**

- Github: [@pawanpaudel93](https://github.com/pawanpaudel93)

## 🤝 Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/pawanpaudel93/m3u_parser/issues).

## Show your support

Give a ⭐️ if this project helped you!

Copyright © 2020 [Pawan Paudel](https://github.com/pawanpaudel93).<br />
