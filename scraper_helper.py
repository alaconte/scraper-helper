import streamlit as st
from undetected_chromedriver import Chrome
import urllib.parse
import os

# ... (Function for generating filename - no changes needed)

def web_downloader_page():
    st.title("Web Page Downloader")
    url = st.text_input("Enter the URL to scrape:")

    # Function to create a formatted filename from the URL
    def generate_filename(url):
        save_dir = "./scraped_sites/"
        parsed_url = urllib.parse.urlparse(url)
        domain = parsed_url.netloc  # Get domain name
        domain = ".".join(domain.split(".")[:-1]) # Remove the top level domain
        path_parts = parsed_url.path.strip("/").split("/")[-2:]  # Get last two parts of path

        # Join parts and handle empty path_parts
        if len(path_parts) == 2:
            filename = f"{domain}-{path_parts[0]}-{path_parts[1]}.html"
        elif len(path_parts) == 1:
            filename = f"{domain}-{path_parts[0]}.html"
        else:
            filename = f"{domain}.html"

        return save_dir + filename

    # Scrape and save website if URL is entered
    if url:
        try:
            # Create a Chrome instance using undetected-chromedriver
            driver = Chrome()
            driver.get(url)

            # Get the HTML content of the webpage
            html_content = driver.page_source

            # Generate a safe filename
            filename = generate_filename(url)
            safe_filename = os.path.join(".", os.path.basename(filename))

            # Save the HTML content to a local file
            with open(safe_filename, "w", encoding="utf-8") as f:
                f.write(html_content)

            st.success("Website scraped and saved as: " + safe_filename)

            # Close the Chrome window
            driver.quit()

        except Exception as e:
            st.error("An error occurred: " + str(e))

# Homepage of the app
def homepage():
    st.title("Web Scraping Tool")
    st.write("This tool offers various web scraping functionalities:")
    st.markdown("""
    - **Download Web Page:** Download the HTML content of a web page.
    - *(Other features you plan to add)*
    """)

# Sidebar with buttons
st.sidebar.title("Navigation")

# Use a session state to remember which button was pressed
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"  # Set a default page

if st.sidebar.button("Home"):
    st.session_state.current_page = "Home"
if st.sidebar.button("Web Page Downloader"):
    st.session_state.current_page = "Web Page Downloader"

# Display the selected page based on session state
if st.session_state.current_page == "Home":
    homepage()
elif st.session_state.current_page == "Web Page Downloader":
    web_downloader_page()
