from document.models import Document
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig

@tool
def list_documents(config:RunnableConfig):
    """
    List the most recent documents limited to 5 for curret user
    """
    limit = 5
    print(config)
    configurable = config.get('configurable') or config.get('metadata') 
    user_id = configurable.get('user_id')
    qs = Document.objects.filter(owner_id=user_id, active=True).order_by("-created_at")
    response_data = []
    # serailizing the data
    for obj in qs[:limit]:
        response_data.append(
            {
                "id":obj.id,
                "title":obj.title
            }
        )
    return response_data

@tool
def get_documents(document_id:int, config:RunnableConfig):
    """
    Get the details of a specific document from list of documents
    """
    configurable = config.get('configurable') or config.get('metadata') 
    user_id = configurable.get('user_id')
    try:
        obj = Document.objects.get(id=document_id, owner_id=user_id, active=True)
    except Document.DoesNotExist:
        raise Exception("Document not found try again")
    except:
        raise Exception("Invalid request for a document detail, try again")
    response_data = {
        "id": obj.id,
        "title": obj.title,
        "content": obj.content,
        "created_at": obj.created_at
    }
    # serailizing the data
    return response_data

@tool
def create_document(title:str, content:str, config:RunnableConfig):
    """
    Create new document based on text

    title: string max characters of 120
    content: long form text in paragraphs and pages
    """
    configurable = config.get('configurable') or config.get('metadata') 
    user_id = configurable.get('user_id')

    obj = Document.objects.create(title=title, owner_id=user_id, content=content,active=True)
    
    response_data = {
        "id": obj.id,
        "title": obj.title,
        "content": obj.content,
        "created_at": obj.created_at
    }
    # serailizing the data
    return response_data

@tool
def delete_documents(document_id:int, config:RunnableConfig):
    """
    Delete the details of a specific document from list of documents by document_id
    """
    configurable = config.get('configurable') or config.get('metadata') 
    user_id = configurable.get('user_id')
    try:
        obj = Document.objects.get(id=document_id, owner_id=user_id, active=True)
    except Document.DoesNotExist:
        raise Exception("Document not found try again")
    except:
        raise Exception("Invalid request for a document detail, try again")
    obj.delete()
    response_data = {
        "message":"success"
    }
    # serailizing the data
    return response_data

@tool
def update_document(document_id:int,title:str=None, content:str=None, config:RunnableConfig=None):
    """
    Update document based on document_id

    document_id: id of document (required)
    title: string max characters of 120
    content: long form text in paragraphs and pages
    """
    configurable = config.get('configurable') or config.get('metadata') 
    user_id = configurable.get('user_id')

    try:
        obj = Document.objects.get(id=document_id, owner_id=user_id, active=True)
    except Document.DoesNotExist:
        raise Exception("Document not found try again")
    except:
        raise Exception("Invalid request for a document detail, try again")

    # obj = Document.objects.create(title=title, owner_id=user_id, content=content,active=True)
    
    if title is not None:
        obj.title = title
    if content is not None:
        obj.content = content
    if title or content:
        obj.save()

    response_data = {
        "id": obj.id,
        "title": obj.title,
        "content": obj.content,
        "created_at": obj.created_at
    }
    # serailizing the data
    return response_data

document_tools = [
    create_document,
    list_documents,
    get_documents,
    delete_documents
]