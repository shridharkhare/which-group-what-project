from streamlit_js import st_js


# Function to navigate to a URL
def nav_to(url):
    js = f'window.open("{url}", "_blank");'
    st_js(js, key="nav_to")


def reload_page():
    js = "parent.window.location.reload();"
    st_js(js, key="reload_page")


# Function to get the Google session from the URL fragment
def get_session_from_fragment(fragment):
    if fragment is not None and len(fragment) > 10:
        fragment = fragment.replace("#", "")
        g_session = dict(x.split("=") for x in fragment.split("&"))
        # synatx of dict comprehension
        # dict_variable = {key:value for (key,value) in dictonary.items()}
        return g_session
