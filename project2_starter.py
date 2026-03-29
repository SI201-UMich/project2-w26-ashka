# SI 201 HW4 (Library Checkout System)
# Your name: Ashka Patel and Lynn Van
# Your student id: 53816807, 15287597
# Your email: ashkap@umich.edu, lynnvan@umich.edu
# Who or what you worked with on this homework (including generative AI like ChatGPT):
# If you worked with generative AI also add a statement for how you used it.
# e.g.: ashka patel, lynn van
# Asked ChatGPT for hints on debugging and for suggestions on overall code structure
#
# Did your use of GenAI on this assignment align with your goals and guidelines in your Gen AI contract? If not, why?
#
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
    titles = soup.find_all('div', class_='t1jojoys')
    print("titles: ", titles)

    # <div class="t1jojoys dir dir-ltr" data-testid="listing-card-title" id="title_49043049">Home in Mission District</div>,

    links = soup.find_all('a', class_='cy5jw6o')
        
    for i in range(len(titles)):
        title_text = titles[i].text.strip()
        link_url = links[i]['href']
        listing_id = link_url.split('/')[-1].split('?')[0]
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
    with open(html_path, 'r', encoding='utf-8-sig') as f:
        soup = BeautifulSoup(f, 'html.parser')

        superhost_tag = soup.find(text="Superhost")
        if superhost_tag: 
            host_type = "Superhost"
        else: 
            host_type = "Regular"
        
        host_tag = soup.find('h2', class_='_147n6cc')
        if host_tag:
            raw_text = host_tag.text
            host_name = raw_text.replace("Hosted by ", "")
        else:
            host_name = ""  

        policy_tag = soup.find('li', class_='f19phm70')
        policy_raw = policy_tag.text if policy_tag else ""
        
        if "pending" in policy_raw.lower():
            policy = "Pending"
        elif "not needed" in policy_raw.lower() or "exempt" in policy_raw.lower():
            policy = "Exempt"
        else:
            policy = policy_raw.strip()
        
        rating_tag = soup.find('span', class_='_17p698z')
        if rating_tag: 
            location_rating = float(rating_tag.text)
        else: 
            location_rating = 0.0

        if "private room" in soup.text.lower():
            room_type = "Private Room"
        elif "shared room" in soup.text.lower():
            room_type = "Shared Room"
        else:
            room_type = "Entire Room"
        
    return {listing_id: {"policy_number": policy, "host_type": host_type, "host_name": host_name, "room_type": room_type, "location_rating": location_rating}}


def create_listing_database(html_path) -> list[tuple]:
    """
    Use prior functions to gather all necessary information and create a database of listings.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples. Each tuple contains:
        (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


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
    pass
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
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


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
    pass
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
    pass
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

        # TODO: Spot-check a few known values by opening the corresponding listing_<id>.html files.
        # 1) Check that listing 467507 has the correct policy number "STR-0005349".
        # 2) Check that listing 1944564 has the correct host type "Superhost" and room type "Entire Room".
        # 3) Check that listing 1944564 has the correct location rating 4.9.
        pass

    def test_create_listing_database(self):
        # TODO: Check that each tuple in detailed_data has exactly 7 elements:
        # (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)

        # TODO: Spot-check the LAST tuple is ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8).
        pass

    def test_output_csv(self):
        out_path = os.path.join(self.base_dir, "test.csv")

        # TODO: Call output_csv() to write the detailed_data to a CSV file.
        # TODO: Read the CSV back in and store rows in a list.
        # TODO: Check that the first data row matches ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"].

        os.remove(out_path)

    def test_avg_location_rating_by_room_type(self):
        # TODO: Call avg_location_rating_by_room_type() and save the output.
        # TODO: Check that the average for "Private Room" is 4.9.
        pass

    def test_validate_policy_numbers(self):
        # TODO: Call validate_policy_numbers() on detailed_data and save the result into a variable invalid_listings.
        # TODO: Check that the list contains exactly "16204265" for this dataset.
        pass


def main():
    detailed_data = create_listing_database(os.path.join("html_files", "search_results.html"))
    output_csv(detailed_data, "airbnb_dataset.csv")


if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)