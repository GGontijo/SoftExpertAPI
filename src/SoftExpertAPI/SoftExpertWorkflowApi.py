import base64
from io import BufferedReader
from .SoftExpertOptions import SoftExpertOptions
from .SoftExpertBaseAPI import SoftExpertBaseAPI
from .SoftExpertException import SoftExpertException

import xml.etree.ElementTree as ET


class SoftExpertWorkflowApi(SoftExpertBaseAPI):

    def __init__(self, options: SoftExpertOptions):
        super().__init__(options, "/apigateway/se/ws/wf_ws.php")  

    def _remove_namespace(self, xml):
            return xml.replace('xmlns="urn:workflow"', '')

    def newWorkflow(self, ProcessID:str , WorkflowTitle: str, UserID: str = None):
        """
        Cria um workflow
        
        :param ProcessID: ID da instância de workflow
        :type ProcessID: str

        :param WorkflowTitle: ID da entidade/tabela que será editada
        :type WorkflowTitle: str

        :param UserID: Matrícula do usuário
        :type UserID: str, optional

        :raises SoftExpertException: Tipo de erro retornado pelo SoftExpert
        :raises Exception: Demais erros
        
        :return: O ID da instância de workflow gerada. Em caso de erro, um SoftExpertException ou Exception é lançado e deve ser capturado com try/catch
        :rtype: str

        Exemplos: https://github.com/GGontijo/SoftExpertAPI/blob/main/README.md
        """

        action = "urn:newWorkflow"

        xml_UserID = ""
        if(UserID != None):
            xml_UserID = f"<urn:UserID>{UserID}</urn:UserID>"
        
        xml_body = f"""
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:workflow">
            <soapenv:Header/>
            <soapenv:Body>
                <{action}>
                    <!--You may enter the following 3 items in any order-->
                    <urn:ProcessID>{ProcessID}</urn:ProcessID>
                    <urn:WorkflowTitle>{WorkflowTitle}</urn:WorkflowTitle>

                    <!--Optional:-->
                    {xml_UserID}

                </{action}>
            </soapenv:Body>
            </soapenv:Envelope>
        """

        reponse_body = self.request(action=action, xml_body=xml_body)

        
        
        # Parseando o XML
        response_body_cleaned = self._remove_namespace(reponse_body)
        root = ET.fromstring(response_body_cleaned)

        try:
           # Encontrando o RecordID
            record_id = root.find(".//RecordID").text
            return record_id
        
        except:
            Detail = root.find(".//Detail").text
            raise SoftExpertException(f"Resposta do SoftExpert: {Detail}")

       


       

        
    def executeActivity(self, WorkflowID: str, ActivityID: str, ActionSequence: int, UserID: str = None):
        """
        Executa uma atividade
        """
        action = "urn:executeActivity"

        xml_UserID = ""
        if(UserID != None):
            xml_UserID = f"<urn:UserID>{UserID}</urn:UserID>"
        
        xml_body = f"""
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:workflow">
            <soapenv:Header/>
            <soapenv:Body>
                <{action}>
                    <!--You may enter the following 5 items in any order-->
                    <urn:WorkflowID>{WorkflowID}</urn:WorkflowID>
                    <urn:ActivityID>{ActivityID}</urn:ActivityID>
                    <urn:ActionSequence>{ActionSequence}</urn:ActionSequence>

                    <!--Optional:-->
                    {xml_UserID}
                    <!--Optional:-->
                    <urn:ActivityOrder></urn:ActivityOrder>

                </{action}>
            </soapenv:Body>
            </soapenv:Envelope>
        """

        reponse_body = self.request(action=action, xml_body=xml_body)

        # Parseando o XML
        response_body_cleaned = self._remove_namespace(reponse_body)
        root = ET.fromstring(response_body_cleaned)

        Status = root.find(".//Status").text
        Detail = root.find(".//Detail").text
        if(Status == "FAILURE"):
            raise SoftExpertException(f"Resposta do SoftExpert: {Detail}")





       
    def editEntityRecord(self, WorkflowID: str, EntityID: str, form: dict = None, relationship: dict = None, files: dict = None):
        """
        Permite editar o(s) formulário(s) de uma instância de workflow

        :param WorkflowID: ID da instância de workflow
        :type WorkflowID: str

        :param EntityID: ID da entidade/tabela que será editada
        :type ActivityID: str

        :param form: Dicionário contendo chave/valor de todos os itens a serem editados
        :type form: dict

        :param relationship: Dicionário contendo chave/valor de todos os relacionamentos a serem editados
        :type relationship: dict

        :param files: Dicionário contendo chave/valor de todos os arquivos do formulário a serem anexados
        :type files: str, optional

        :raises SoftExpertException: Tipo de erro retornado pelo SoftExpert
        :raises Exception: Demais erros
        
        :return: None. Em caso de sucesso, nada é retornado. Em caso de erro, um SoftExpertException ou Exception é lançado e deve ser capturado com try/catch
        :rtype: Nome

        Obs.: 
        Valor do atributo da tabela de formulário.
        Observações de acordo com o tipo do atributo:
        ▪ Número: dígitos numéricos sem separador de milhar e decimal
        ▪ Decimal: dígitos numéricos sem separador de milhar e com ponto (.) como separador decimal
        ▪ Data: YYYY-MM-DD
        ▪ Hora: HH:MM
        ▪ Boolean: 0 ou 1

        Exemplos: https://github.com/GGontijo/SoftExpertAPI/blob/main/README.md
        """

        if(form == None and relationship == None and files == None):
            raise SoftExpertException("Nada informado para ser editado")
            # Se nada passado para ser editado, então retorna exception

        
        action = "urn:editEntityRecord"
        xml_Form = ""
        if(form != None):
            for key, value in form.items():
                xml_Form += f"""
                    <urn:EntityAttribute>
                        <urn:EntityAttributeID>{key}</urn:EntityAttributeID>
                        <urn:EntityAttributeValue>{value}</urn:EntityAttributeValue>
                    </urn:EntityAttribute>
                """
        

        xml_Relationship = ""
        if(relationship != None):
            for key, value in relationship.items():
                for subkey, subvalue in value.items():
                    xml_Relationship += f"""
                        <urn:Relationship>
                            <urn:RelationshipID>{key}</urn:RelationshipID>
                            <urn:RelationshipAttribute>
                                <urn:RelationshipAttributeID>{subkey}</urn:RelationshipAttributeID>
                                <urn:RelationshipAttributeValue>{subvalue}</urn:RelationshipAttributeValue>
                            </urn:RelationshipAttribute>
                        </urn:Relationship>
                    """

        xml_Files = ""
        if (files != None):
            for key, value in files.items():
                for subkey, subvalue in value.items():
                    xml_Files += f"""
                        <urn:EntityAttributeFile>
                            <urn:EntityAttributeID>{key}</urn:EntityAttributeID>
                            <urn:FileName>{subkey}</urn:FileName>
                            <urn:FileContent>{base64.b64encode(subvalue).decode()}</urn:FileContent>
                        </urn:EntityAttributeFile>
                    """


        xml_body = f"""
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:workflow">
            <soapenv:Header/>
            <soapenv:Body>
                <{action}>
                    <!--You may enter the following 5 items in any order-->
                    <urn:WorkflowID>{WorkflowID}</urn:WorkflowID>
                    <urn:EntityID>{EntityID}</urn:EntityID>
                    
                    <urn:EntityAttributeList>
                        {xml_Form}
                    </urn:EntityAttributeList>

                    <urn:RelationshipList>
                        {xml_Relationship}
                    </urn:RelationshipList>

                    <urn:EntityAttributeFileList>
                        {xml_Files}
                    </urn:EntityAttributeFileList>
                    
                </{action}>
            </soapenv:Body>
            </soapenv:Envelope>
        """

        reponse_body = self.request(action=action, xml_body=xml_body)

        # Parseando o XML
        response_body_cleaned = self._remove_namespace(reponse_body)
        root = ET.fromstring(response_body_cleaned)

        Status = root.find(".//Status").text
        Detail = root.find(".//Detail").text
        if(Status == "FAILURE"):
            raise SoftExpertException(f"Resposta do SoftExpert: {Detail}", xml_body)







    def newAttachment(self, WorkflowID: str, ActivityID: str, FileName: str, FileContent: BufferedReader, UserID: str = None):
        """
        Anexa um arquivo em uma instância de workflow em uma determinada atividade

        :param WorkflowID: ID da instância de workflow
        :type WorkflowID: str

        :param ActivityID: ID da atividade em que o arquivo será anexado
        :type ActivityID: str

        :param FileName: Nome do arquivo com a extensão. Ex. documento.docx
        :type FileName: str

        :param FileContent: Arquivo em formato binário. Ex.: open(os.path.join(os.getcwd(), "example.png"), "rb").read()
        :type FileContent: BufferedReader

        :param UserID: Matrícula do usuário
        :type UserID: str, optional

        :raises SoftExpertException: Tipo de erro retornado pelo SoftExpert
        :raises Exception: Demais erros
        
        :return: None. Em caso de sucesso, nada é retornado. Em caso de erro, um SoftExpertException ou Exception é lançado e deve ser capturado com try/catch
        :rtype: Nome

        Exemplos: https://github.com/GGontijo/SoftExpertAPI/blob/main/README.md
        """
        action = "urn:newAttachment"

        xml_UserID = ""
        if(UserID != None):
            xml_UserID = f"<urn:UserID>{UserID}</urn:UserID>"
        
        xml_body = f"""
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:workflow">
            <soapenv:Header/>
            <soapenv:Body>
                <{action}>
                    <urn:WorkflowID>{WorkflowID}</urn:WorkflowID>
                    <urn:ActivityID>{ActivityID}</urn:ActivityID>
                    <urn:FileName>{FileName}</urn:FileName>
                    <urn:FileContent>{base64.b64encode(FileContent).decode()}</urn:FileContent>
                    {xml_UserID}
                </{action}>
            </soapenv:Body>
            </soapenv:Envelope>
        """

        reponse_body = self.request(action=action, xml_body=xml_body)

        # Parseando o XML
        response_body_cleaned = self._remove_namespace(reponse_body)
        root = ET.fromstring(response_body_cleaned)

        Status = root.find(".//Status").text
        Detail = root.find(".//Detail").text
        if(Status == "FAILURE"):
            raise SoftExpertException(f"Resposta do SoftExpert: {Detail}")





    def newChildEntityRecord(self, WorkflowID: str, MainEntityID: str, ChildRelationshipID: str, FormGrid: dict):
        """
        Adiciona um item em uma grid de uma instância de workflow

        :param WorkflowID: ID da instância de workflow
        :type WorkflowID: str    

        :param MainEntityID: ID da entidade/tabela que será editada na instância de workflow
        :type MainEntityID: str

        :param ChildRelationshipID: ID do relacionamento que será editado na instância de workflow
        :type ChildRelationshipID: str

        :param FormGrid: Dicionário com os campos e seus respectivos valores
        """
        action = "urn:newChildEntityRecord"

        xml_FormGrid = ""
        for key, value in FormGrid.items():
            xml_FormGrid += f"""
                <urn:EntityAttribute>
                    <urn:EntityAttributeID>{key}</urn:EntityAttributeID>
                    <urn:EntityAttributeValue>{value}</urn:EntityAttributeValue>
                </urn:EntityAttribute>
            """

        xml_body = f"""
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:workflow">
            <soapenv:Header/>
            <soapenv:Body>
                <{action}>
                    <urn:WorkflowID>{WorkflowID}</urn:WorkflowID>
                    <urn:MainEntityID>{MainEntityID}</urn:MainEntityID>
                    <urn:ChildRelationshipID>{ChildRelationshipID}</urn:ChildRelationshipID>
                    <urn:EntityAttributeList>
                        {xml_FormGrid}
                    </urn:EntityAttributeList>
                </{action}>
            </soapenv:Body>
            </soapenv:Envelope>
        """

        reponse_body = self.request(action=action, xml_body=xml_body)

        # Parseando o XML
        response_body_cleaned = self._remove_namespace(reponse_body)
        root = ET.fromstring(response_body_cleaned)

        Status = root.find(".//Status").text
        Detail = root.find(".//Detail").text
        if(Status == "FAILURE"):
            raise SoftExpertException(f"Resposta do SoftExpert: {Detail}")