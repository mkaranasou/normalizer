What is this module about
---
Analyzing short, noisy data like class names and attributes, tweets and hashtags means that there is a need for some kind of normalization. This component attempts to combine several methods to normalize the aforementioned kind of data. It focuses on word-level analysis (not a whole phrase that can be split in words by spaces but e.g. "SomeClient", "FistName", "lastName" etc) and uses regex, spellcheck, nlp and dynamic programming to try analyze the data and return a list of normalized words.

Installation
---
This module requires Python 2.7+
   ```
    pip install -U /path/to/word_normalizer/
    
    or 
    
    cd /path/to/word-normalizer/
    pip install requirements.txt
   ```
for nltk:
  ```python
    # open a python console
    import nltk
    nltk.download()
  ```  
Usage
---

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
