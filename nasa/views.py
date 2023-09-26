from django.shortcuts import render
from datetime import datetime

import requests

NASA_API_URL = 'https://api.nasa.gov/planetary/apod'
NASA_API_KEY = 'KTdaeJLDK6HtAmgkhwrmLOjFcSSQ4JrPLHiCowdk'
GOOGLE_API_KEY = 'AIzaSyA7nZQ0wIBQ8O7f3DAsNl6vavUpaSqW6JE'
GOOGLE_CX_ID = '84525eb695ea54e03'

def index(request):
    # Get NASA APOD data
    nasa_data = get_nasa_apod()

    # Extract relevant information
    title = nasa_data["title"]
    img_url = nasa_data["url"]

    # Format the date for readability
    date_object = datetime.strptime(nasa_data["date"], "%Y-%m-%d")
    formatted_date = date_object.strftime("%B %d, %Y")

    # Get Google search results based on the APOD title
    google_data = get_google_info(title)

    # Prepare the context dictionary
    context = {
        "url": img_url,
        "date": formatted_date,
        "title": title,
        "google_results": google_data
    }

    print(context)
    return render(request, "index.html", context)
    
# Get Astronomy Picture of the Day from NASA API
def get_nasa_apod():
    response = requests.get(NASA_API_URL, params={"api_key": NASA_API_KEY})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Error: Failed to retrieve Astronomy Picture of the Day")

# Get Google Search results
def get_google_info(query):
    # Build the Google Search API URL
    query_param = '+'.join(query.split())
    google_url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={GOOGLE_CX_ID}&q={query_param}"

    # Send a GET request to the Google Search API
    response = requests.get(google_url)

    # Check that status is 200 (OK)
    if response.status_code == 200:
        data = response.json()
        total_results = data.get("searchInformation", {}).get("totalResults", 0)

        # Check if there are search results
        if int(total_results) > 0:
            search_results = data.get("items", [])

            clean_results = {item["title"]: item["snippet"] for item in search_results}
            return clean_results
    return None