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
        "title": obj.title
    }
    # serailizing the data
    return response_data

document_tools = [
    list_documents,
    get_documents
]