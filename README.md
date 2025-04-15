# SoftExpertAPI
Esta lib fornece um wrapper às APIs SoftExpert


Instanciar a lib:
``` python
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