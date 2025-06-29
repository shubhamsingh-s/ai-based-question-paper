"import streamlit as st" 

import streamlit as st

# Import the main app
try:
    from app import main
    main()
except ImportError as e:
    st.error(f"Import Error: {e}")
    st.info("Please check if app.py exists in the repository root.")
except Exception as e:
    st.error(f"Error loading application: {e}")
    st.info("Please check the deployment logs for more details.") 
