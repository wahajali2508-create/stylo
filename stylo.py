import streamlit as st
import requests
import xml.etree.ElementTree as ET

st.set_page_config(page_title="Style Threadz Products", page_icon="🛍️", layout="wide")

st.markdown("<h1 style='text-align:center;'>🛍️ Style Threadz Products</h1>", unsafe_allow_html=True)

# 🔗 Your RSS feed URL
RSS_FEED_URL = "https://style-threadz.myspreadshop.net/1482874/products.rss?pushState=false&targetPlatform=google"

# 🧩 Fetch RSS Feed
try:
    response = requests.get(RSS_FEED_URL)
    response.raise_for_status()
    xml_data = response.text
except Exception as e:
    st.error(f"Failed to fetch feed: {e}")
    st.stop()

# 🧾 Parse XML feed
root = ET.fromstring(xml_data)

# Namespace handle (RSS XML uses ns)
ns = {'g': 'http://base.google.com/ns/1.0'}

# Extract items
items = root.findall('.//item')

# 🛍️ Display products in 3 columns
cols = st.columns(3)
for i, item in enumerate(items):
    title = item.find('title').text if item.find('title') is not None else "No Title"
    description = item.find('description').text if item.find('description') is not None else ""
    price = item.find('g:price', ns).text if item.find('g:price', ns) is not None else "N/A"
    image_link = item.find('g:image_link', ns).text if item.find('g:image_link', ns) is not None else ""
    product_link = item.find('g:link', ns).text if item.find('g:link', ns) is not None else "#"  # ✅ Corrected line

    with cols[i % 3]:
        if image_link:
            st.image(image_link, use_container_width=True)
        st.markdown(f"### {title}")
        st.markdown(f"💰 **Price:** {price}")
        st.markdown(description, unsafe_allow_html=True)
        st.markdown(
            f"<a href='{product_link}' target='_blank'>"
            f"<button style='background-color:#007bff;color:white;padding:8px 16px;border:none;border-radius:8px;cursor:pointer;'>"
            f"View on StyleThreadz</button></a>",
            unsafe_allow_html=True
        )
