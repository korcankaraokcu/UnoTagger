# UnoTagger
A simple tagging library for documenting python scripts

## How to install
UnoTagger only requires unotools, assuming that you already have libreoffice installed:  
```pip3 install unotools```  
If you don't have libreoffice or unolibs by default, execute this to install all the required tools from scratch:  
```sudo aptitude install -y libreoffice libreoffice-script-provider-python uno-libs3 python3-uno python3```
## How to use
Startup libreoffice  
```soffice --accept='socket,host=localhost,port=8100;urp;StarOffice.Service'```  
Use the UnoTagger library in your project or in a seperate terminal
```
>>> import tagger
>>> tagger.create_tag_document()
```
CONTENT UPCOMING
