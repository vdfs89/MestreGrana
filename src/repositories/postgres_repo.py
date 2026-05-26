try:
    import streamlit as st
except Exception:
    from _stubs import st

from psycopg2.pool import SimpleConnectionPool
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")


@st.cache_resource
def get_pool(minconn=1, maxconn=10):
    if not DATABASE_URL:
        return None
    return SimpleConnectionPool(minconn, maxconn, dsn=DATABASE_URL)


def get_conn():
    pool = get_pool()
    if pool is None:
        return None
    return pool.getconn()


def put_conn(conn):
    pool = get_pool()
    if pool is None or conn is None:
        return
    pool.putconn(conn)
