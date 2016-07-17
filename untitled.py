from __future__ import print_function

import argparse
import functools
import hashlib
import logging
import os
import random
import re
from xml.etree import ElementTree

try:
    import cPickle as pickle
except ImportError:
    import pickle

try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen


logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger()


def memoize(fn):
    cache_dir = os.path.abspath(os.path.expanduser('~/.local/share/untitled/'))

    def cache_get(cache_key):
        logger.debug('cache_get %s', cache_key)
        cache_file = os.path.join(cache_dir, cache_key + '.bin')
        if not os.path.exists(cache_file):
            return None
        with open(cache_file) as f:
            return pickle.load(f)

    def cache_set(cache_key, value):
        logger.debug('cache_set %s', cache_key)
        cache_file = os.path.join(cache_dir, cache_key + '.bin')
        if not os.path.exists(cache_dir):
            logger.debug("> Creating cache directory: %s", cache_dir)
            os.mkdir(cache_dir)

        with open(cache_file, 'wb') as f:
            logger.debug("> Creating cache for %s", cache_key)
            pickle.dump(value, f)

    @functools.wraps(fn)
    def memoizer(*args):
        cache_key = hashlib.md5(':'.join(
            [fn.__name__] + [str(arg) for arg in args]
        )).hexdigest()
        cached = cache_get(cache_key)
        if cached:
            return cached

        value = fn(*args)
        cache_set(cache_key, value)
        return value

    return memoizer


def open_file(url):
    if not url.startswith('http'):
        return open(os.path.abspath(os.path.expanduser(url)))

    logger.info(' => Downloading {}'.format(url))
    return urlopen(url)


@memoize
def word_list(url):
    content = open_file(url).read()
    words = {re.sub(r'[^a-z0-9]+', '', w.lower()) for w in content.split()}
    return words


@memoize
def pypi_names(simple_index='https://pypi.python.org/simple/'):
    content = open_file(simple_index).read()
    tree = ElementTree.fromstring(content)
    names = {a.text.lower() for a in tree.iter('a')}
    return names


def filter_blacklist(words, existing):
    return set(words) - set(existing)


def filter_prefix(words, prefix):
    return {w for w in words if w.startswith(prefix)}


def filter_suffix(words, suffix):
    return {w for w in words if w.endswith(suffix)}


def filter_contains(words, substring):
    return {w for w in words if substring in w}


def filter_max_length(words, maxlen):
    return {w for w in words if len(w) <= maxlen}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('word_list', nargs='?', default='/usr/share/dict/words')
    parser.add_argument('--limit', dest='limit', type=int, default=10)
    parser.add_argument('--prefix', dest='prefix')
    parser.add_argument('--suffix', dest='suffix')
    parser.add_argument('--contains', dest='contains')
    parser.add_argument('--maxlen', dest='maxlen', type=int)
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true')
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    words = word_list(args.word_list)
    words = filter_blacklist(words, pypi_names())

    if args.prefix:
        words = filter_prefix(words, args.prefix)
    if args.suffix:
        words = filter_suffix(words, args.suffix)
    if args.contains:
        words = filter_contains(words, args.contains)
    if args.maxlen:
        words = filter_max_length(words, args.maxlen)

    words = list(words)
    random.shuffle(words)

    for word in words[:args.limit]:
        print(word)


if __name__ == '__main__':
    main()
