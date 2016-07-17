Untitled: PyPI name generator
===

Untitled can help you find a name for your project which is not already taken
on [PyPI](http://pypi.python.org). By default it will use the dictionary
located on your computer at `/usr/local/dict/words` (only tested on my mac),
but you can use any text file either locally available on your computer, or
from an accessible URL.


Examples:

Default operation, 10 random words from `/usr/local/dict/words`.

```
$ untitled
stagiritic
euchrome
monoclonius
oxytone
tenuis
sarcle
almoravides
sporangiform
leprologic
restaurateur
```

Use the URL of a text file as input and limit the number of results to 5:

```
$ untitled https://github.com/NSkelsey/cvf/raw/master/war_and_peace.txt --limit 5
spurred
regrettable
fantastic
coughed
starless
```

Limit results to those that contain the string `py` with a maximum length of 6:

```
$ untitled --contains py --maxlen 6
weepy
gaspy
sloppy
clumpy
peepy
tropyl
jumpy
gilpy
pygarg
pyrus
```
