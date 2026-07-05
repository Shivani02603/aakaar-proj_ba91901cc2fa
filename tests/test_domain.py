import pytest
from datetime import datetime

def test_fr_001_register_then_login_returns_jwt(client):
    email = "unique_email@example.com"
    password = "securepassword123"
    register_response = client.post("/api/auth/register", json={"email": email, "password": password})
    assert register_response.status_code == 201
    assert "access_token" in register_response.json()

    login_response = client.post("/api/auth/login", json={"email": email, "password": password})
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()

def test_fr_002_upload_document_stores_file_and_returns_id(client, auth_headers):
    file_content = b"Sample text content for testing."
    files = {"file": ("test.txt", file_content, "text/plain")}
    response = client.post("/api/documents/upload", files=files, headers=auth_headers)
    assert response.status_code == 201
    assert "document_id" in response.json()

def test_fr_003_uploaded_documents_processed_for_text_extraction(client, auth_headers):
    file_content = b"Another sample text for extraction testing."
    files = {"file": ("test.txt", file_content, "text/plain")}
    upload_response = client.post("/api/documents/upload", files=files, headers=auth_headers)
    assert upload_response.status_code == 201
    document_id = upload_response.json()["document_id"]

    response = client.get(f"/api/documents/{document_id}", headers=auth_headers)
    assert response.status_code == 200
    assert "extracted_text" in response.json()
    assert response.json()["extracted_text"] == file_content.decode()

def test_fr_004_extracted_text_chunked_correctly(client, auth_headers):
    file_content = b"A" * 1200  # 1200 characters to test chunking
    files = {"file": ("test.txt", file_content, "text/plain")}
    upload_response = client.post("/api/documents/upload", files=files, headers=auth_headers)
    assert upload_response.status_code == 201
    document_id = upload_response.json()["document_id"]

    response = client.get(f"/api/documents/{document_id}", headers=auth_headers)
    assert response.status_code == 200
    chunks = response.json()["chunks"]
    assert len(chunks) > 1
    assert all(len(chunk["text"]) <= 1000 for chunk in chunks)
    assert all(chunk["text"].startswith("A") for chunk in chunks)

def test_fr_005_embeddings_generated_for_chunks(client, auth_headers):
    file_content = b"Embedding test content."
    files = {"file": ("test.txt", file_content, "text/plain")}
    upload_response = client.post("/api/documents/upload", files=files, headers=auth_headers)
    assert upload_response.status_code == 201
    document_id = upload_response.json()["document_id"]

    response = client.get(f"/api/documents/{document_id}", headers=auth_headers)
    assert response.status_code == 200
    chunks = response.json()["chunks"]
    assert all("embedding" in chunk for chunk in chunks)

def test_fr_006_chunks_and_embeddings_stored_in_postgresql(client, auth_headers):
    file_content = b"Storage test content."
    files = {"file": ("test.txt", file_content, "text/plain")}
    upload_response = client.post("/api/documents/upload", files=files, headers=auth_headers)
    assert upload_response.status_code == 201
    document_id = upload_response.json()["document_id"]

    response = client.get(f"/api/documents/{document_id}", headers=auth_headers)
    assert response.status_code == 200
    chunks = response.json()["chunks"]
    assert len(chunks) > 0
    assert all("embedding" in chunk for chunk in chunks)

def test_fr_007_similarity_search_retrieves_top_chunks(client, auth_headers):
    query = "Find relevant content."
    response = client.post("/api/ai/query", json={"query": query}, headers=auth_headers)
    assert response.status_code == 200
    results = response.json()["results"]
    assert len(results) <= 5
    assert all("chunk_id" in result for result in results)

def test_fr_008_answers_generated_with_cited_sources(client, auth_headers):
    query = "What is the meaning of life?"
    response = client.post("/api/ai/query", json={"query": query}, headers=auth_headers)
    assert response.status_code == 200
    answer = response.json()["answer"]
    source_chunk_ids = response.json()["source_chunk_ids"]
    assert answer is not None
    assert len(source_chunk_ids) > 0

def test_fr_009_frontend_provides_interfaces(client, auth_headers):
    # This test assumes the endpoints are functional and accessible
    response = client.get("/api/documents", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    response = client.get("/api/chat/history", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)