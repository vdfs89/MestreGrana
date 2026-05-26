"""MongoDB utilities and helpers."""

try:
    import streamlit as st
except Exception:
    from _stubs import st

import os
from dotenv import load_dotenv

load_dotenv()


def get_secret_or_env(key):
    """Get secret from Streamlit or environment."""
    try:
        return st.secrets[key]
    except Exception:
        return os.environ.get(key)


@st.cache_resource
def get_mongo_client():
    """Initialize MongoDB client with lazy import."""
    try:
        from pymongo import MongoClient
        uri = get_secret_or_env("MONGODB_ATLAS_URI")
        if not uri:
            return None
        client = MongoClient(uri, tls=True, serverSelectionTimeoutMS=5000)
        # Ping to verify connection
        client.admin.command("ping")
        return client
    except Exception:
        return None


@st.cache_resource
def get_mongo_db(db_name="InvestimentoDIO"):
    """Get MongoDB database."""
    client = get_mongo_client()
    if not client:
        return None
    return client[db_name]


@st.cache_data(ttl=600)
def find_documents(collection_name, query=None, limit=None):
    """Find documents in a collection with caching.
    
    Args:
        collection_name: str - Collection name
        query: dict - MongoDB query (default: {})
        limit: int - Limit results (default: None)
    
    Returns:
        list - Documents
    """
    try:
        db = get_mongo_db()
        if not db:
            return []
        
        collection = db[collection_name]
        if query is None:
            query = {}
        
        cursor = collection.find(query)
        if limit:
            cursor = cursor.limit(limit)
        
        docs = list(cursor)
        # Remove MongoDB's _id for serialization
        for doc in docs:
            doc.pop("_id", None)
        
        return docs
    except Exception as e:
        print(f"Erro ao buscar documentos em {collection_name}: {e}")
        return []


@st.cache_data(ttl=600)
def find_one_document(collection_name, query=None):
    """Find a single document.
    
    Args:
        collection_name: str - Collection name
        query: dict - MongoDB query
    
    Returns:
        dict - Document or None
    """
    try:
        db = get_mongo_db()
        if not db:
            return None
        
        collection = db[collection_name]
        if query is None:
            query = {}
        
        doc = collection.find_one(query)
        if doc:
            doc.pop("_id", None)
        
        return doc
    except Exception as e:
        print(f"Erro ao buscar documento em {collection_name}: {e}")
        return None


def insert_document(collection_name, document):
    """Insert a document (non-cached).
    
    Args:
        collection_name: str - Collection name
        document: dict - Document to insert
    
    Returns:
        str - Inserted ID or None
    """
    try:
        db = get_mongo_db()
        if not db:
            return None
        
        collection = db[collection_name]
        result = collection.insert_one(document)
        return str(result.inserted_id)
    except Exception as e:
        print(f"Erro ao inserir documento em {collection_name}: {e}")
        return None


def update_document(collection_name, query, update):
    """Update documents (non-cached).
    
    Args:
        collection_name: str - Collection name
        query: dict - MongoDB query
        update: dict - Update operations (e.g., {"$set": {...}})
    
    Returns:
        int - Number of documents modified
    """
    try:
        db = get_mongo_db()
        if not db:
            return 0
        
        collection = db[collection_name]
        result = collection.update_many(query, update)
        return result.modified_count
    except Exception as e:
        print(f"Erro ao atualizar documentos em {collection_name}: {e}")
        return 0


def delete_document(collection_name, query):
    """Delete documents (non-cached).
    
    Args:
        collection_name: str - Collection name
        query: dict - MongoDB query
    
    Returns:
        int - Number of documents deleted
    """
    try:
        db = get_mongo_db()
        if not db:
            return 0
        
        collection = db[collection_name]
        result = collection.delete_many(query)
        return result.deleted_count
    except Exception as e:
        print(f"Erro ao deletar documentos em {collection_name}: {e}")
        return 0
