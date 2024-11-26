import streamlit as st

def UI():
    # Add space using margin-top
    # Add space above the logo in the sidebar
    st.sidebar.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
    
    
    logo_url = "app/assets/images/logo.png"
    st.sidebar.image(logo_url)
    
    
    
    # Sidebar footer
    st.sidebar.write("**App Version:** 1.0.0")
    st.sidebar.write("© 2024 Angel App")
