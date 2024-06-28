import requests
from bs4 import BeautifulSoup
import time
import concurrent.futures
import csv
import os

def save_to_csv(blog_details, filename=r'filename.csv'):
    # Specify the CSV file header
    header = ['Title', 'Date', 'Image URL', 'Likes Count']

    # Check if the file already exists
    if os.path.exists(filename):
        # If the file exists, create a new file with a unique name
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(f"{base}_{counter}{ext}"):
            counter += 1
        filename = f"{base}_{counter}{ext}"

    # Write the data to the CSV file
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write the header
        csv_writer.writerow(header)

        # Write the blog details
        for blog in blog_details:
            csv_writer.writerow([blog['blog_title'], blog['blog_date'], blog['image_url'], blog['likes_count']])


def crawl_blog_website(url):
    # Use a Session to persist cookies
    session = requests.Session()

    # Add headers to simulate a legitimate browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        # Send an HTTP request to the website
        response = session.get(url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract blog details
            blog_details = []

            # Find all the blog posts on the page
            blog_posts = soup.find_all('div', class_='wrap')
            
            for post in blog_posts:
                  # Extract image URL
                  image_url = post.find('div',class_='img')
                  if image_url:
                       a=image_url.find('a')
                       image_url=a['data-bg']
                  else:
                      image_url='Not found'
                  
                  # Extract blog title
                  blog_title = post.find('h6').text  # Update the tag based on the actual HTML structure
                  
                  # Extract blog date
                  blog_date = post.find('div', class_='blog-detail')
                  blog_date=blog_date.find('span').text
                  
                  # Extract blog likes count
                  likes_count = post.find('a', class_='zilla-likes').text
                  
                  # Create a dictionary to store the blog details
                  blog_details.append({
                    'image_url': image_url,
                    'blog_title': blog_title,
                    'blog_date': blog_date,
                    'likes_count': likes_count
                })

            return blog_details

        else:
            # Print an error message if the request was unsuccessful
            print(f"Error: Unable to fetch the page (Status code: {response.status_code})")
            return None

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def main():
    # List of URLs to crawl
    urls = []
    for x in range(1,46):
        urls.append("https://rategain.com/blog/page/" + str(x) + "/")
    
    # Set up a ThreadPoolExecutor with 100 worker threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        # Submit each URL to the executor for crawling concurrently
        futures = [executor.submit(crawl_blog_website, url) for url in urls]

        # Wait for all the tasks to complete
        concurrent.futures.wait(futures)

        # Get the results from the completed tasks
        results = [future.result() for future in futures]
        
        
        # Process the results
        all_blog_details = []
        for result in results:
            if result:
                all_blog_details.extend(result)

        # Save the blog details to a CSV file
        save_to_csv(all_blog_details)
        
        
if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Total execution time: {end_time - start_time} seconds")