import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urljoin, urlparse
import os
from typing import List, Dict, Set

class WebsiteScraper:
    def __init__(self, base_url: str, max_pages: int = 50):
        self.base_url = base_url
        self.max_pages = max_pages
        self.visited_urls: Set[str] = set()
        self.scraped_content: List[Dict] = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def is_valid_url(self, url: str) -> bool:
        """Check if URL belongs to the target domain"""
        parsed_base = urlparse(self.base_url)
        parsed_url = urlparse(url)
        return parsed_url.netloc == parsed_base.netloc
    
    def extract_text_content(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract meaningful text content from the page"""
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Extract title
        title = soup.find('title')
        title_text = title.get_text().strip() if title else ""
        
        # Extract main content
        main_content = ""
        
        # Try to find main content areas
        content_selectors = [
            'main', 'article', '.content', '#content', 
            '.main-content', '.page-content', '.post-content'
        ]
        
        content_found = False
        for selector in content_selectors:
            content_area = soup.select_one(selector)
            if content_area:
                main_content = content_area.get_text(separator=' ', strip=True)
                content_found = True
                break
        
        # If no main content area found, extract from body
        if not content_found:
            body = soup.find('body')
            if body:
                main_content = body.get_text(separator=' ', strip=True)
        
        # Extract meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        description = meta_desc.get('content', '') if meta_desc else ""
        
        # Extract headings for structure
        headings = []
        for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            headings.append(h.get_text().strip())
        
        return {
            'title': title_text,
            'description': description,
            'content': main_content,
            'headings': headings
        }
    
    def get_page_links(self, soup: BeautifulSoup, current_url: str) -> List[str]:
        """Extract all internal links from the page"""
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(current_url, href)
            
            # Clean URL (remove fragments and query params for deduplication)
            clean_url = full_url.split('#')[0].split('?')[0]
            
            if self.is_valid_url(clean_url) and clean_url not in self.visited_urls:
                links.append(clean_url)
        
        return links
    
    def scrape_page(self, url: str) -> Dict:
        """Scrape a single page"""
        try:
            print(f"Scraping: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            content = self.extract_text_content(soup)
            
            # Get links for further crawling
            links = self.get_page_links(soup, url)
            
            return {
                'url': url,
                'status': 'success',
                'content': content,
                'links': links,
                'scraped_at': time.time()
            }
            
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return {
                'url': url,
                'status': 'error',
                'error': str(e),
                'scraped_at': time.time()
            }
    
    def scrape_website(self) -> List[Dict]:
        """Scrape the entire website"""
        urls_to_visit = [self.base_url]
        
        while urls_to_visit and len(self.visited_urls) < self.max_pages:
            current_url = urls_to_visit.pop(0)
            
            if current_url in self.visited_urls:
                continue
            
            self.visited_urls.add(current_url)
            result = self.scrape_page(current_url)
            
            if result['status'] == 'success':
                self.scraped_content.append(result)
                
                # Add new links to visit
                for link in result['links']:
                    if link not in self.visited_urls and link not in urls_to_visit:
                        urls_to_visit.append(link)
            
            # Be respectful - add delay between requests
            time.sleep(1)
        
        return self.scraped_content
    
    def save_content(self, filename: str = 'scraped_content.json'):
        """Save scraped content to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.scraped_content, f, indent=2, ensure_ascii=False)
        print(f"Content saved to {filename}")

def scrape_specific_urls(urls_list):
    """Scrape specific URLs instead of crawling"""
    scraped_content = []
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    for i, url in enumerate(urls_list, 1):
        print(f"Scraping {i}/{len(urls_list)}: {url}")
        
        try:
            response = session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Extract title
            title = soup.find('title')
            title_text = title.get_text().strip() if title else ""
            
            # Extract main content
            main_content = ""
            
            # Try to find main content areas
            content_selectors = [
                'main', 'article', '.content', '#content', 
                '.main-content', '.page-content', '.post-content',
                '.entry-content', '.site-content'
            ]
            
            content_found = False
            for selector in content_selectors:
                content_area = soup.select_one(selector)
                if content_area:
                    main_content = content_area.get_text(separator=' ', strip=True)
                    content_found = True
                    break
            
            # If no main content area found, extract from body
            if not content_found:
                body = soup.find('body')
                if body:
                    main_content = body.get_text(separator=' ', strip=True)
            
            # Extract meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            description = meta_desc.get('content', '') if meta_desc else ""
            
            # Extract headings for structure
            headings = []
            for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                headings.append(h.get_text().strip())
            
            scraped_content.append({
                'url': url,
                'status': 'success',
                'content': {
                    'title': title_text,
                    'description': description,
                    'content': main_content,
                    'headings': headings
                },
                'scraped_at': time.time()
            })
            
            print(f"✓ Successfully scraped: {title_text}")
            
        except Exception as e:
            print(f"✗ Error scraping {url}: {str(e)}")
            scraped_content.append({
                'url': url,
                'status': 'error',
                'error': str(e),
                'scraped_at': time.time()
            })
        
        # Be respectful - add delay between requests
        time.sleep(1)
    
    return scraped_content

def main():
    # All Real Estate IoT website URLs
    urls_to_scrape = [
        "https://realestateiot.com/",
        "https://realestateiot.com/iot-efficiency-automation/",
        "https://realestateiot.com/iot-efficiency-automation/smart-access-control-systems/",
        "https://realestateiot.com/iot-efficiency-automation/smart-parking-management/",
        "https://realestateiot.com/iot-efficiency-automation/hvac-automation/",
        "https://realestateiot.com/iot-efficiency-automation/lighting-automation/",
        "https://realestateiot.com/iot-efficiency-automation/occupancy-space-utilization-sensors/",
        "https://realestateiot.com/iot-safety-security/",
        "https://realestateiot.com/iot-safety-security/surveillance-cctv-integration/",
        "https://realestateiot.com/iot-safety-security/intrusion-detection-alarms/",
        "https://realestateiot.com/iot-safety-security/environmental-health-monitoring/",
        "https://realestateiot.com/iot-safety-security/remote-lockdown-emergency-response/",
        "https://realestateiot.com/iot-safety-security/fire-safety-emergency-systems/",
        "https://realestateiot.com/iot-sustainability-monitoring/",
        "https://realestateiot.com/iot-sustainability-monitoring/energy-monitoring-systems/",
        "https://realestateiot.com/iot-sustainability-monitoring/water-management-systems/",
        "https://realestateiot.com/iot-sustainability-monitoring/air-quality-monitoring/",
        "https://realestateiot.com/iot-sustainability-monitoring/solar-energy-monitoring/",
        "https://realestateiot.com/iot-sustainability-monitoring/waste-management-systems/",
        "https://realestateiot.com/iot-sustainability-monitoring/sustainable-asset-tracking/",
        "https://realestateiot.com/careers/",
        "https://realestateiot.com/careers/internships/",
        "https://realestateiot.com/careers/internships-for-masters-mba/",
        "https://realestateiot.com/careers/ai-enhanced-internship-opportunities/",
        "https://realestateiot.com/about-us/",
        "https://realestateiot.com/contact-us/",
        "https://gaorfid.com/teksummit/",
        "https://gaotek.com/teksummit/"
    ]
    
    print(f"Starting to scrape {len(urls_to_scrape)} URLs from Real Estate IoT website...")
    
    # Scrape all specified URLs
    content = scrape_specific_urls(urls_to_scrape)
    
    print(f"\nScraping completed!")
    print(f"Total pages scraped: {len(content)}")
    
    # Save the content
    with open('data/scraped_content.json', 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=2, ensure_ascii=False)
    print(f"Content saved to data/scraped_content.json")
    
    # Print summary
    successful = 0
    failed = 0
    for item in content:
        if item['status'] == 'success':
            print(f"✓ {item['url']} - {item['content']['title']}")
            successful += 1
        else:
            print(f"✗ {item['url']} - Error: {item.get('error', 'Unknown')}")
            failed += 1
    
    print(f"\nSummary: {successful} successful, {failed} failed")

if __name__ == "__main__":
    # Create data directory
    os.makedirs('data', exist_ok=True)
    main()