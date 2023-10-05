import streamlit as st


show = st.toggle('Show Technical Description')
# Embed the HTML page using st.components.v1.html
if show:
	st.components.v1.html(open('technical.html').read(), width=800, height=1000,scrolling=True)
else:
	st.components.v1.html(open('rapid_care_hub.html').read(), width=800, height=1600,scrolling=True)

