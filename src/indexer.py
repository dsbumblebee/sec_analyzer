import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# 1. 설정
DATA_PATH = "./apple_latest_10q_clean.txt"
DB_PATH = "../chroma_db"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2" # sLLM과 궁합이 좋은 가볍고 성능 좋은 임베딩 모델

def process_document():
    print("--- 1. 문서 로드 중... ---")
    if not os.path.exists(DATA_PATH):
        print(f"파일이 없습니다: {DATA_PATH}")
        return

    loader = TextLoader(DATA_PATH, encoding='utf-8')
    documents = loader.load()
    
    # 2. 청킹 (Chunking) - 전략의 핵심!
    # 공시 보고서는 호흡이 길어서 chunk_size를 1000~2000 정도로 잡고
    # 문맥이 끊기지 않게 overlap을 200 정도 줍니다.
    print("--- 2. 문서 분할 중 (Chunking)... ---")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""] # 문단 바뀜 우선으로 자름
    )
    texts = text_splitter.split_documents(documents)
    print(f"총 {len(texts)}개의 청크로 분할되었습니다.")

    # 3. 임베딩 및 저장 (Embedding & Vector Store)
    print("--- 3. 벡터 DB 저장 중... ---")
    # 로컬에서 무료로 돌릴 수 있는 HuggingFace 임베딩 모델 사용
    embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)
    
    # ChromaDB에 저장 (디스크에 영구 저장)
    vectordb = Chroma.from_documents(
        documents=texts, 
        embedding=embeddings,
        persist_directory=DB_PATH
    )
    print(f"--- 완료! 데이터베이스가 {DB_PATH}에 저장되었습니다. ---")

if __name__ == "__main__":
    process_document()