from fastapi import APIRouter
from src.api.schemas import QARequest, QAResponse
from src.qa.qa_chain import ask   

router = APIRouter(
    prefix="/qa",
    tags=["qa"]
)


@router.post("/", response_model=QAResponse)
def qa_endpoint(payload: QARequest):
    """
    Run the QA RAG pipeline and return only the answer.
    """
    answer = ask(payload.question)

    return QAResponse(answer=answer)