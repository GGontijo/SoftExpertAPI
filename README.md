# SoftExpertAPI
Esta lib fornece um wrapper às APIs SoftExpert  

# Getting Stated
Instalar a Lib:
``` bash
pip install SoftExpertAPI
```

Configurar e criar uma instância:
``` python
from SoftExpertAPI import SoftExpertException, SoftExpertOptions, SoftExpertWorkflowApi

option = SoftExpertOptions(
    url = "https://softexpert.com",
    authorization = "Basic SEU_TOKEN", # pode ser Basic ou Bearer
    userID = "sistema.automatico" # Matricula do usuário padrão das operações. Pode ser informado usuário diferente em cada endpoint chamado
)
api = SoftExpertWorkflowApi(option)
```

Criar instância de Workflow
``` python
try:
    instancia = api.newWorkflow(ProcessID="SM", WorkflowTitle="Apenas um teste")
    print(f"Instancia criada com sucesso: {instancia}")
except SoftExpertException as e:
    print(f"Erro do SE: {e}")
    exit()
except Exception as e:
    print(f"Erro genérico: {e}")
    exit()
```

Editar o formulário, relacionamentos (selectbox) e anexar arquivos no formulário:
``` python
try:
    
    form = {
        # chave é o id do campo no banco de dados
        # valor é o valor que será atribuido
        "pedcompra": "Perdido de compra",
        "chave": "2390840923890482093849023849023904809238904",
    }

    relations = {
        # chave é o id do relacionamento
        # valor:
            # chave é o id do campo da tabela do relacionamento
            # valor é o valor que será atribuido
        "relmoeda": {
            "idmoeda": "DOLAR"
        }
    }

    files = {
        # chave é o id do campo no banco de dados
        # valor:
            # chave é o nome do arquivo
            # valor é binário do arquivo (não passar o base64)
        "boleto": {
            "example.png": open(os.path.join(os.getcwd(), "example.png"), "rb").read()
        }
    }

    api.editEntityRecord(WorkflowID=instancia, EntityID="SOLMIRO", form=form, relationship=relations, files=files)
    print(f"Formulário editado com sucesso!")
except SoftExpertException as e:
    print(f"Erro do SE: {e}")
    exit()
except Exception as e:
    print(f"Erro genérico: {e}")
    exit()
```

Adiciona um item em uma grid
``` python
try:
    MainEntityID = "adte";               # ID da tabela principal
    ChildRelationshipID = "relcheck";    # ID do relacionamento da grid
    formGrid = {
        # chave é o id do campo no banco de dados
        # valor é o valor que será atribuido
        "atividade": "teste de grid"
    }

    api.newChildEntityRecord(WorkflowID=instancia, MainEntityID=MainEntityID, ChildRelationshipID=ChildRelationshipID, FormGrid=formGrid)
    print(f"Item adicionado à grid com sucesso!")
except SoftExpertException as e:
    print(f"Erro do SE: {e}")
    exit()
except Exception as e:
    print(f"Erro genérico: {e}")
    exit()
```

Anexar arquivo em uma instância (menu de anexo do lado esquerdo):
``` python
try:
    bin = open(os.path.join(os.getcwd(), "example.png"), "rb").read()
    filename = "example.png"
    api.newAttachment(WorkflowID=instancia, ActivityID="atvsolicitarmiro", FileName="example.png", FileContent=bin)
    print(f"Atividade executada com sucesso!")
except SoftExpertException as e:
    print(f"Erro do SE: {e}")
    exit()
except Exception as e:
    print(f"Erro genérico: {e}")
    exit()
```


Executar atividade:
``` python
try:
    api.executeActivity(WorkflowID=instancia, ActivityID="atvsolicitarmiro", ActionSequence=1)
    print(f"Atividade executada com sucesso!")
except SoftExpertException as e:
    print(f"Erro do SE: {e}")
    exit()
except Exception as e:
    print(f"Erro genérico: {e}")
    exit()
```

Exemplos completos e funcionais no arquivo [example.py](example.py)


## Build

Instale as ferramentas de build e upload
```bash
pip install build twine
```

Execute o comando abaixo na raiz do seu projeto para gerar os arquivos de distribuição
```bash
python -m build
```

Enviar pacote
```bash
twine upload dist/*
```

Para buildar de forma automática:
```bash
git tag v1.0.1
git push origin v1.0.1
```