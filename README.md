# UnoTagger
A simple tagging library for documenting python scripts

## How to install
UnoTagger only requires unotools, assuming that you already have libreoffice installed:  
```sudo pip3 install unotools```  
If you don't have libreoffice or unolibs by default, execute this to install all the required tools from scratch:  
```sudo aptitude install -y libreoffice libreoffice-script-provider-python uno-libs3 python3-uno python3```
## How to use
Startup libreoffice:  
```soffice --accept='socket,host=localhost,port=8100;urp;StarOffice.Service'```  
Use UnoTagger's ```create_tag_documents()``` function in your project.  
Run this command for demonstration:  
```python3 test.py```
### Pros
 - Module based, you don't have to pass source file paths as the parameter
 - Can create documents based on multiple modules
 - Ability to search through function names
 - Can document variables (check ```unotagger.get_comments_of_variables()``` function for more information)
### Cons
 - Can only tag functions and variables in a module. Doesn't support classes or inline functions. This can be achieved by rewriting the ```unotagger.get_docstrings()``` function to be recursive
