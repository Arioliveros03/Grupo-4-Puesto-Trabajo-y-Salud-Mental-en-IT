import streamlit as st   
import os
import duckdb
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("motherduck_token")

conn = duckdb.connect("md:puesto de trabajo y salud mental")