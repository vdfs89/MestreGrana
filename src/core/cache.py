import streamlit as st

def cache_resource(fn=None, **kwargs):
    return st.cache_resource(**kwargs)(fn) if fn else lambda f: st.cache_resource(**kwargs)(f)

def cache_data(fn=None, **kwargs):
    return st.cache_data(**kwargs)(fn) if fn else lambda f: st.cache_data(**kwargs)(f)
