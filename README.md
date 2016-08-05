#What is this module about

#Installation
This module requires Python 2.7+

    cd /path/to/word-normalizer/
    pip install requirements.txt

for nltk:

    # open a python console
    import nltk
    nltk.download()
    
#Usage

```python
    parser = Parser(spellcheck=True, deploy_abbreviations=True)
    # all lower
    print parser.normalize("somename")  
    ['some', 'name']
    
    # snake_case
    print parser.normalize("some_name")
    ['some', 'name']
    
    # camelCase
    print parser.normalize("someName")
    ['some', 'name']
    
    # PascalCase
    print parser.normalize("SomeName")
    ['some', 'name']
    
    # PascalCase with noise
    print parser.normalize("SomeName123435")
    ['some', 'name']
    
    print parser.normalize("s123435somename")
    ['some', 'name', 'south']
    
    print parser.normalize("ClientName")
    ['client', 'name']
    print parser.normalize("Iscustomer")
    ['customer', 'is']
    
    # Do not deploy abbreviations option ignores 's':
    parser = Parser(deploy_abbreviations=False)
    print parser.normalize("s123435somename")
    ['some', 'name']
```