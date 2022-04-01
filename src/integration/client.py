import requests
from requests.auth import HTTPBasicAuth
import re
import os
import io
import json

from datawrapper import Datawrapper

def read_integrations():
    """ Reads integration.json, if the file not exists it will be created
        
        Return 
            (dict): [integration_id] => {
                            "author": Who created the integration
                            "title": Title
                            "url": The url to use in CMS
                            "external_id": id in Multimedia tool
                             extra_meta: different key/vals that is handy to have 
                            }
    """
    if os.path.isfile("integrations.json") and os.access("integrations.json", os.R_OK):
        with io.open("integrations.json") as json_file:
            data = json.load(json_file)
        
    else:
        print ("Either file is missing or is not readable, creating file...")
        with io.open("integrations.json", 'w') as json_file:
            json_file.write(json.dumps({}))
        data = {}
            
    return data

def exists_on_server(integration_id):
    """Checks if the integration exists in integration.json
    
        integration_id (string): Integration id used
        
        Return
            (bool): True if id exists in integration.json
    """
    integrations = read_integrations()
    return integration_id in integrations and "url" in integrations[integration_id] and "external_id" in integrations[integration_id]


def get_request_verb_and_url(integration_id):
    """Checks if the integration should be updated or created
    
        integration_id (string): Integration id used
        
        Return
            (array): verb and url for updating/creating integration
    """
    integrations = read_integrations()
    
    if integration_id in integrations and "external_id" in integrations[integration_id]:
        return ["PUT", "%s/%s" % (os.getenv("MM_API_BASE_URL"), integrations[integration_id]["external_id"])]
    
    return ["POST", os.getenv("MM_API_BASE_URL")]

def get_mm_data(integration_id):
    """Get the url and external id for the integration in MM-tools
    
        integration_id (string): Integration id used
        
        Return
            (dict): external_id: id in Multimedia tool
                    external_url: URL to use in the CMS
    """
    integrations = read_integrations()
    
    if integration_id in integrations:
        return {
            "url": integrations[integration_id]["url"], 
            "external_id": integrations[integration_id]["external_id"]
        }
    
    return None

def get_integration_id(search_key, search_value):
    """Get the integration_id base on key/value pair
    
        search_key (string): the key to search for
        search_value (string): the value to search for
        
        Return
            (string): the integration id, None if not found
    """
    integrations = read_integrations()
    
    for key, val in integrations.items():
        if search_key in val:
            if val[search_key] == search_value:
                return key
    
    return None
            

def save_integration_meta(integration_id, title, author, external_url, external_id, extra_meta):
    """Save the new integration in itegation.json
    
        integration_id (str): Integration id used
        title (str): title
        author (str): Who created this masterpiece?
        external_url (str): URL returned from MM-tools
        extra_meta (dict): extra meta information that is nice to have
    """
    integrations = read_integrations()
    
    meta = {
            "author": author,
            "title": title,
            "url": external_url,
            "external_id": external_id
        }
    
    for key, val in extra_meta.items():
        meta[key] = val
    
    integrations[integration_id] = meta
    
    try:
        with io.open("integrations.json", 'w') as json_file:
            json_file.write(json.dumps(integrations))
    except Exception as ex:
        raise Exception("Could not write file, due to: %s" % ex)
        return False
    
    return True
    
def create_integration(integration_id, title, author, body, extra_meta={}):
    """Create a new integration in MM-tools
    
        integration_id (string): Integration id used
        title: title
        author: Who created this masterpiece?
        body: HTML
        
        Return
            (dict): external_id: id in Multimedia tool
                    external_url: URL to use in the CMS
    """

    if os.getenv('INTEGRATIONS_ENABLED', 'False') == 'False':
        raise Exception("Integrations disabled in env file. Set INTEGRATIONS_ENABLED=True and restart Jupyter")

    re_http = re.compile(r"^http:")
    
    response = requests.request(
        *get_request_verb_and_url(integration_id),
        auth=HTTPBasicAuth(os.getenv("MM_API_PROD_USERNAME"), os.getenv("MM_API_PROD_PASSWORD")),
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": os.getenv("MM_API_PROD_USERNAME"),
        },
        data=json.dumps(
            {
                "title": title or "",
                "author": author or "Bord4",
                "body": body or "",
            }
        )
    )

    if not (200 <= response.status_code <= 201):
        raise Exception("Unexpected status code: %s" % response.status_code)
        return None

    # If this was just an update, there's nothing left for us to do
    # and the API won't give us any interesting information anyway.
    if exists_on_server(integration_id):
        return get_mm_data(integration_id)

    result = response.json()["body"]
    if not result["id"] or not result["url"]:
        raise Exception("Did not receive ID and URL from Multimedia API")
        return None

    external_id = result["id"]
    # The URLs returned by the API will be HTTP, which causes problems in
    # production where articles are served over HTTPS.
    # It seems that these used to be rewritten at run-time, but apparently
    # this is no longer the case.
    external_url = re_http.sub("https:", result["url"])
    
    saved = save_integration_meta(integration_id, title, author, external_url, external_id, extra_meta)
    if not saved:
        return None
    
    print(integration_id, external_url)
    
    return {
        "url": external_url, 
        "external_id": external_id
    }


    
def create_dw_integration(dw, integration_id, chart_id):
    """Creates an MM integration for Datawrapper
    
        dw: (Datawrapper class): An instance of the Datawrapper class
        integration_id (str): id to the integration
        chart_id (str): id for Datawrapper chart
        
        Return:
            (bool): Success
    """
    chart_props = dw.chart_properties(chart_id)

    if not chart_props:
        raise Exception("Did not receive chart props code from Datawrapper API")
        return False
        
    title = chart_props["title"] or ""

    try:
        byline = chart_props["metadata"]["describe"]["byline"]
    except KeyError:
        byline = ""

    try:
        iframe_code = chart_props["metadata"]["publish"]["embed-codes"]["embed-method-responsive"]
        iframe_code = iframe_code.replace('height="undefined"', 'height="400"')
    except TypeError:
        raise Exception("Did not receive iframe code from Datawrapper API")
        return False

    if iframe_code:
        created = create_integration(integration_id, title, byline, iframe_code, {"chart_id": chart_id})
        if not created:
            raise Exception("Could not create integration")
            return False

    return True

def get_or_create_chart(dw, key, title='Ny grafikk', chart_type = 'd3-maps-choropleth', folder_id = None, copy_from=None):

    """
    Searches integrations.json for given key and if it exists, returns the chart_id. If not, it will create a new chart and return the id or create 
    a new based on an existing chart. 
        
        dw: (Datawrapper class): An instance of the Datawrapper class
        key: string: The integration key to search for
        title: string: Title of new chart if created
        chart_type: string: Chart type of new chart. Defaults to d3-maps-choropleth
        folder_id: int: ID number of DW folder to place chart in
        copy_from: string: If given will copy another graf as template and return the ned id, instead of creating a new from scratch. Chart type and folder will be the same.
    Returns:
        str: Chart id
    """

    chart_id = ''
    integrations = read_integrations()

    if key in integrations:
        chart_id = integrations[key]['chart_id']
        print(f'Chart and integration exists with DW id: {chart_id}')
    else:

        if copy_from:
            chart_id = dw.copy_chart(copy_from)
            
        else:
            chart = dw.create_chart(title = title, chart_type=chart_type, folder_id=folder_id)
            chart_id = chart['id']
            print(f'Chart and integration does not exist. Creating with DW id: {chart_id}')
    return chart_id