# SoftExpertAPI
This library provides a wrapper for SoftExpert APIs

# Getting Started
Install the library:
```bash
pip install SoftExpertAPI

Configure and create an instance:
``` python
from SoftExpertAPI import SoftExpertException, SoftExpertOptions, SoftExpertWorkflowApi

from SoftExpertAPI import SoftExpertException, SoftExpertOptions, SoftExpertWorkflowApi

option = SoftExpertOptions(
    url = "https://softexpert.com",
    authorization = "Basic YOUR_TOKEN", # can be Basic or Bearer
    userID = "system.user" # Default user ID for operations. Different users can be specified in each endpoint call
)
api = SoftExpertWorkflowApi(option)
```

Create Workflow instance
``` python
try:
    instance = api.newWorkflow(ProcessID="SM", WorkflowTitle="Just a test")
    print(f"Instance created successfully: {instance}")
except SoftExpertException as e:
    print(f"SE Error: {e}")
    exit()
except Exception as e:
    print(f"Generic error: {e}")
    exit()
```

Edit the form, relationships (select boxes), and attach files to the form:
``` python
try:
    
    form = {
        # key is the field ID in the database
        # value is the value to be assigned
        "pedcompra": "Purchase order",
        "chave": "2390840923890482093849023849023904809238904",
    }

    relations = {
        # key is the relationship ID
        # value:
            # key is the field ID in the related table
            # value is the value to be assigned
        "relmoeda": {
            "idmoeda": "DOLLAR"
        }
    }

    files = {
        # key is the field ID in the database
        # value:
            # key is the file name
            # value is the file binary (do not use base64)
        "boleto": {
            "example.png": open(os.path.join(os.getcwd(), "example.png"), "rb").read()
        }
    }

    api.editEntityRecord(WorkflowID=instance, EntityID="SOLMIRO", form=form, relationship=relations, files=files)
    print(f"Form edited successfully!")
except SoftExpertException as e:
    print(f"SE Error: {e}")
    exit()
except Exception as e:
    print(f"Generic error: {e}")
    exit()
```

Add an item to a grid
``` python
try:
    MainEntityID = "adte";               # Main table ID
    ChildRelationshipID = "relcheck";    # Grid relationship ID
    formGrid = {
        # key is the field ID in the database
        # value is the value to be assigned
        "atividade": "grid test"
    }

    api.newChildEntityRecord(WorkflowID=instance, MainEntityID=MainEntityID, ChildRelationshipID=ChildRelationshipID, FormGrid=formGrid)
    print(f"Item added to grid successfully!")
except SoftExpertException as e:
    print(f"SE Error: {e}")
    exit()
except Exception as e:
    print(f"Generic error: {e}")
    exit()
```

Attach file to an instance (left-side attachment menu):
``` python
try:
    bin = open(os.path.join(os.getcwd(), "example.png"), "rb").read()
    filename = "example.png"
    api.newAttachment(WorkflowID=instance, ActivityID="atvsolicitarmiro", FileName="example.png", FileContent=bin)
    print(f"Activity executed successfully!")
except SoftExpertException as e:
    print(f"SE Error: {e}")
    exit()
except Exception as e:
    print(f"Generic error: {e}")
    exit()
```


Execute activity:
``` python
try:
    api.executeActivity(WorkflowID=instance, ActivityID="atvsolicitarmiro", ActionSequence=1)
    print(f"Activity executed successfully!")
except SoftExpertException as e:
    print(f"SE Error: {e}")
    exit()
except Exception as e:
    print(f"Generic error: {e}")
    exit()
```


Complete working examples in [example.py](example.py)


## Build

Install build tools and upload
```bash
pip install build twine
```

Run this command in the project root to generate distribution files
```bash
python -m build
```

Upload package
```bash
twine upload dist/*
```

For automatic build:
```bash
git tag v1.0.1
git push origin v1.0.1
```

