\# Official ScriptPack Template



This directory contains the official ScriptPack template for the Aksara Nusantara ecosystem.



Every new ScriptPack SHOULD be created by copying this template.



The template serves as the canonical reference implementation of the ScriptPack SDK.



\---



\# Purpose



The ScriptPack Template demonstrates:



\- the required directory structure;

\- the required metadata;

\- the BaseScriptPack implementation;

\- recommended project organization.



It is intended to be copied and customized for a specific writing system.



\---



\# Directory Structure



```

template/



│   manifest.json

│   script.py

│   README.md

│

├── assets/

│   ├── audio/

│   ├── data/

│   ├── fonts/

│   └── images/

│

└── tests/

```



\---



\# Creating a New ScriptPack



1\. Copy the entire template directory.



2\. Rename the directory.



Example:



```

template/



↓



javanese/

```



3\. Update `manifest.json`.



4\. Implement `script.py`.



5\. Add assets.



6\. Test using the Core Engine.



\---



\# Required Files



\## manifest.json



Contains ScriptPack metadata.



\## script.py



Implements the BaseScriptPack interface.



\## README.md



Documents the ScriptPack.



\---



\# Assets



All writing-system-specific resources SHALL be stored inside the ScriptPack.



Examples:



\- fonts

\- audio

\- images

\- character data



The Core Engine SHALL NOT own these resources.



\---



\# Conformance



Every ScriptPack SHALL conform to:



\- AN-STD-001 — ScriptPack Interface Specification



\---



\# License



Unless otherwise specified, this template is released under the MIT License.

