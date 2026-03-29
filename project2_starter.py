# SI 201 HW4 (Library Checkout System)
# Your name: Ashka Patel and Lynn Van
# Your student id: 53816807, 15287597
# Your email: ashkap@umich.edu, lynnvan@umich.edu
# Who or what you worked with on this homework (including generative AI like ChatGPT):
# If you worked with generative AI also add a statement for how you used it.
# e.g.: ashka patel, lynn van
# Asked ChatGPT for hints on debugging and for suggestions on overall code structure
# yes
# Did your use of GenAI on this assignment align with your goals and guidelines in your Gen AI contract? If not, why?
# yes
# --- ARGUMENTS & EXPECTED RETURN VALUES PROVIDED --- #
# --- SEE INSTRUCTIONS FOR FULL DETAILS ON METHOD IMPLEMENTATION --- #

from bs4 import BeautifulSoup
import re
import os
import csv
import unittest
import requests  # kept for extra credit parity


# IMPORTANT NOTE:
"""
If you are getting "encoding errors" while trying to open, read, or write from a file, add the following argument to any of your open() functions:
    encoding="utf-8-sig"
"""


def load_listing_results(html_path) -> list[tuple]:
    """
    Load file data from html_path and parse through it to find listing titles and listing ids.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples containing (listing_title, listing_id)
    """
    # TODO: Implement checkout logic following the instructions
    with open(html_path, 'r', encoding='utf-8-sig') as f:
        soup = BeautifulSoup(f, 'html.parser')
        
    listings_list = []
    titles = soup.find_all('div', class_='t1jojoys dir dir-ltr')
    #print("titles: ", titles)

    #  <div class="t1jojoys dir dir-ltr" data-testid="listing-card-title" id="title_49043049">Home in Mission District</div>,
        
    for i in range(len(titles)):
        title_text = titles[i].text.strip()
        #print("individual titles: ", title_text)
        # link_url = links[i]['href']
        # listing_id = link_url.split('/')[-1].split('?')[0]
        listing_id = titles[i].get('id')
        listing_id = listing_id.split('_')[1].strip()
        listings_list.append((title_text, listing_id))
    
    return listings_list
    

def get_listing_details(listing_id) -> dict:
    """
    Parse through listing_<id>.html to extract listing details.

    Args:
        listing_id (str): The listing id of the Airbnb listing

    Returns:
        dict: Nested dictionary in the format:
        {
            "<listing_id>": {
                "policy_number": str,
                "host_type": str,
                "host_name": str,
                "room_type": str,
                "location_rating": float
            }
        }
    """
    html_path = f"html_files/listing_{listing_id}.html"
    with open(html_path, 'r') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')

    # finding policy number 

    policy_number = soup.find_all("li", class_="f19phm7j dir dir-ltr")[0].text.split(":")[1].strip()

    #finding host type 

    host_type = soup.find('span', class_='_1mhorg9')
    if host_type and "Superhost" in host_type.text:
        host_type = "Superhost"
    else:
        host_type = "Regular Host"

    # finding host name
    host_name = soup.find_all("h2", class_="_14i3z6h")[0].text.split("hosted by")[-1].strip()

    # finding room type

    room_type = soup.find("h2", class_="_14i3z6h").text.lower()
    if "private" in room_type:
        room_type = "Private Room"
    elif "shared" in room_type:
        room_type = "Shared Room"
    else:
        room_type = "Entire Room"

    #finding the location rating
    
    try: 
        rating = float(soup.find_all("span", class_="_4oybiu")[3].text)
    except: 
        rating = 0.0

    details = {
            "policy_number": policy_number,
            "host_type": host_type,
            "host_name": host_name,
            "room_type": room_type,
            "location_rating": rating
        }

    return {listing_id: details}


def create_listing_database(html_path) -> list[tuple]:
    """
    Use prior functions to gather all necessary information and create a database of listings.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples. Each tuple contains:
        (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)
    """

    base_listings = load_listing_results(html_path)
    
    final_database = []
    
    for title, listing_id in base_listings:
        details_dict = get_listing_details(listing_id)
        info = details_dict[listing_id]
        
        listing_tuple = (
            title, 
            listing_id, 
            info["policy_number"], 
            info["host_type"], 
            info["host_name"], 
            info["room_type"], 
            info["location_rating"]
        )
        
        final_database.append(listing_tuple)
        
    return final_database


def output_csv(data, filename) -> None:
    """
    Write data to a CSV file with the provided filename.

    Sort by Location Rating (descending).

    Args:
        data (list[tuple]): A list of tuples containing listing information
        filename (str): The name of the CSV file to be created and saved to

    Returns:
        None
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================

    sorted_data = sorted(data, key=lambda x: x[6], reverse=True)

    with open (filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
    
        header = [ "Listing Title", "Listing ID", "Policy Number", "Host Type", "Host Name", "Room Type", "Location Rating"]
        writer.writerow(header)
        for row in sorted_data:
            writer.writerow(row)
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def avg_location_rating_by_room_type(data) -> dict:
    """
    Calculate the average location_rating for each room_type.

    Excludes rows where location_rating == 0.0 (meaning the rating
    could not be found in the HTML).

    Args:
        data (list[tuple]): The list returned by create_listing_database()

    Returns:
        dict: {room_type: average_location_rating}
    """
    d = {}
    for listing in data: 
        room = listing[5]
        rating = float(listing[6])
        if rating == 0.0:
            continue

        if room not in d: 
            d[room] = [rating]
        else: 
            d[room].append(rating)
    
    avg_dict = {}
    for room, ratings in d.items():
        avg_dict[room] = sum(ratings) / len(ratings)
        
    return avg_dict
        



def validate_policy_numbers(data) -> list[str]:
    """
    Validate policy_number format for each listing in data.
    Ignore "Pending" and "Exempt" listings.

    Args:
        data (list[tuple]): A list of tuples returned by create_listing_database()

    Returns:
        list[str]: A list of listing_id values whose policy numbers do NOT match the valid format
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    invalid_ids = []
    pattern1 = r'^20\d{2}-00\d{4}STR$'
    pattern2 = r'^STR-000\d{4}$'

    for listing in data:
        listing_id = listing[1]
        policy_num = listing[2]

        policy_num_lower = policy_num.lower()
        if "pending" in policy_num_lower or "exempt" in policy_num_lower:
            continue

        match1 = re.match(pattern1, policy_num)
        match2 = re.match(pattern2, policy_num)

        if not (match1 or match2):
            invalid_ids.append(listing_id)

    return invalid_ids
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


# EXTRA CREDIT
def google_scholar_searcher(query):
    """
    EXTRA CREDIT

    Args:
        query (str): The search query to be used on Google Scholar
    Returns:
        List of titles on the first page (list)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    url = "https://scholar.google.com/scholar"
    params = {'q': query}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    }

    try:

        response = requests.get(url, params=params, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title_tags = soup.find_all('h3', class_='gs_rt')
        
        titles = []
        
        for tag in title_tags:
            titles.append(tag.text.strip())
        
        return titles
    
    except Exception as e:
        print(f'An error occured: {e}')
        return []

    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


class TestCases(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.search_results_path = os.path.join(self.base_dir, "html_files", "search_results.html")

        self.listings = load_listing_results(self.search_results_path)
        self.detailed_data = create_listing_database(self.search_results_path)

    def test_load_listing_results(self):
        # TODO: Check that the number of listings extracted is 18.
        # TODO: Check that the FIRST (title, id) tuple is  ("Loft in Mission District", "1944564").

        filename = "html_files/search_results.html"
        # "project2-w26-ashka/html_files/search_results.html" 
        
        with open(filename, 'r', encoding='utf-8-sig') as f:
            content = f.read()
            self.assertTrue(len(content) > 0, "The HTML file is empty.")
        
        results = load_listing_results(filename)

        self.assertEqual(len(results), 18, "The function should extract exactly 18 listings.")

        expected_first_tuple = ("Loft in Mission District", "1944564")
        self.assertEqual(results[0], expected_first_tuple, f"Expected {expected_first_tuple} but got {results[0]}")


    def test_get_listing_details(self):
        html_list = ["467507", "1550913", "1944564", "4614763", "6092596"]

        # TODO: Call get_listing_details() on each listing id above and save results in a list.
        results = {}
        for listing_id in html_list:
            results.update(get_listing_details(listing_id))



        # TODO: Spot-check a few known values by opening the corresponding listing_<id>.html files.
        # 1) Check that listing 467507 has the correct policy number "STR-0005349".
        self.assertEqual(results["467507"]["policy_number"], "STR-0005349")
        # 2) Check that listing 1944564 has the correct host type "Superhost" and room type "Entire Room".
        self.assertEqual(results["1944564"]["host_type"], "Superhost")
        self.assertEqual(results["1944564"]["room_type"], "Entire Room")        
        # 3) Check that listing 1944564 has the correct location rating 4.9.
        self.assertEqual(results["1944564"]["location_rating"], 4.9)
        

    def test_create_listing_database(self):
        # TODO: Check that each tuple in detailed_data has exactly 7 elements:
        # (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)

        # TODO: Spot-check the LAST tuple is ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8).
        for listing in self.detailed_data: 
            self.assertEqual(len(listing), 7)


        last_listing = self.detailed_data[-1]
        expected_output = ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8)
        self.assertEqual(last_listing, expected_output)



    def test_output_csv(self):
        out_path = os.path.join(self.base_dir, "test.csv")

        # TODO: Call output_csv() to write the detailed_data to a CSV file.
        # TODO: Read the CSV back in and store rows in a list.
        # TODO: Check that the first data row matches ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"].
        out_path = os.path.join(self.base_dir, "test.csv")
        output_csv(self.detailed_data, out_path)
        self.assertTrue(os.path.exists(out_path), "The CSV file was not created.")
        rows = []
        with open(out_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append(row)
        expected_first_row = ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"]
        self.assertEqual(rows[1], expected_first_row, f"Expected {expected_first_row} but got {rows[1]}")

        os.remove(out_path)

    def test_avg_location_rating_by_room_type(self):
        # TODO: Call avg_location_rating_by_room_type() and save the output.
        # TODO: Check that the average for "Private Room" is 4.9.
        result = avg_location_rating_by_room_type(self.detailed_data)
        self.assertAlmostEqual(result["Private Room"], 4.9, places=1)        

    def test_validate_policy_numbers(self):
        # TODO: Call validate_policy_numbers() on detailed_data and save the result into a variable invalid_listings.
        # TODO: Check that the list contains exactly "16204265" for this dataset.
        invalid_num = validate_policy_numbers(self.detailed_data)
        self.assertEqual(len(invalid_num), 1, "There should be exactly one invalid policy number.")
        self.assertEqual(invalid_num[0], "16204265", "The invalid listing ID should be '16204265'.")


def main():
    detailed_data = create_listing_database(os.path.join("html_files", "search_results.html"))
    output_csv(detailed_data, "airbnb_dataset.csv")


if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)