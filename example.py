import os
import sys
import uuid



sys.path.append(os.path.abspath("src")) # Just for API development

from SoftExpertAPI import SoftExpertException, SoftExpertOptions, SoftExpertWorkflowApi





option = SoftExpertOptions(
    url = "https://softexpert.com.br",
    authorization = "Basic YOUR_TOKEN_HERE",
    userID = "your.user"
)
api = SoftExpertWorkflowApi(option)



#### CRIAR UMA INSTANCIA
instancia = None
try:
    instancia = api.newWorkflow(ProcessID="ADTE", WorkflowTitle="Apenas um teste")
    print(f"Instancia criada com sucesso: {instancia}")
except SoftExpertException as e:
    print(f"Erro do SE: {e}")
    exit()
except Exception as e:
    print(f"Erro genérico: {e}")
    exit()




#### EDITAR O FORMULÁRIO
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




#### ADICIONA UM ITEM EM UMA GRID
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





#### ANEXAR UM ARQUIVO NA INSTÂNCIA (MENU ANEXO DO LADO ESQUERDO)
try:
    bin = open(os.path.join(os.getcwd(), "example.png"), "rb").read()
    filename = "example.png"
    api.newAttachment(WorkflowID=instancia, ActivityID="atvsolicitarmiro", FileName="example.png", FileContent=bin)
    print(f"Arquivo anexado com sucesso!")
except SoftExpertException as e:
    print(f"Erro do SE: {e}")
    exit()
except Exception as e:
    print(f"Erro genérico: {e}")
    exit()





#### EXECUTAR ATIVIDADE
try:
    api.executeActivity(WorkflowID=instancia, ActivityID="atvsolicitarmiro", ActionSequence=1)
    print(f"Atividade executada com sucesso!")
except SoftExpertException as e:
    print(f"Erro do SE: {e}")
    exit()
except Exception as e:
    print(f"Erro genérico: {e}")
    exit()