import asyncio
import json
import re
from typing import Optional, List, Dict, Any
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
import httpx
from app.core.config import settings
from app.schemas.brand import BrandInsights, ProductInfo, ContactDetails, SocialHandles, FAQ, ImportantLinks


class ShopifyScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': settings.USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        self.timeout = settings.REQUEST_TIMEOUT

    async def scrape_brand_insights(self, website_url: str) -> BrandInsights:
        """Main method to scrape all brand insights from a Shopify store"""
        try:
            # Normalize URL
            if not website_url.startswith(('http://', 'https://')):
                website_url = 'https://' + website_url
            
            # Initialize insights object
            insights = BrandInsights(website_url=website_url)
            
            # Scrape different components
            insights.brand_name = await self._get_brand_name(website_url)
            insights.product_catalog = await self._get_product_catalog(website_url)
            insights.hero_products = await self._get_hero_products(website_url)
            insights.privacy_policy = await self._get_privacy_policy(website_url)
            insights.return_refund_policy = await self._get_return_policy(website_url)
            insights.faqs = await self._get_faqs(website_url)
            insights.social_handles = await self._get_social_handles(website_url)
            insights.contact_details = await self._get_contact_details(website_url)
            insights.brand_context = await self._get_brand_context(website_url)
            insights.important_links = await self._get_important_links(website_url)
            
            return insights
            
        except Exception as e:
            raise Exception(f"Failed to scrape brand insights: {str(e)}")

    async def _get_brand_name(self, website_url: str) -> Optional[str]:
        """Extract brand name from the website"""
        try:
            response = self.session.get(website_url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to get brand name from title tag
            title = soup.find('title')
            if title:
                return title.get_text().strip().split('|')[0].strip()
            
            # Try to get from meta property
            brand_meta = soup.find('meta', property='og:site_name')
            if brand_meta:
                return brand_meta.get('content', '').strip()
                
            return None
            
        except Exception:
            return None

    async def _get_product_catalog(self, website_url: str) -> Optional[List[ProductInfo]]:
        """Get complete product catalog using /products.json endpoint"""
        try:
            products_url = urljoin(website_url, '/products.json')
            response = self.session.get(products_url, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                products = []
                
                for product in data.get('products', []):
                    product_info = ProductInfo(
                        id=str(product.get('id')),
                        title=product.get('title'),
                        handle=product.get('handle'),
                        vendor=product.get('vendor'),
                        product_type=product.get('product_type'),
                        tags=product.get('tags', '').split(',') if product.get('tags') else [],
                        available=product.get('available'),
                        images=[img.get('src') for img in product.get('images', [])],
                        variants=product.get('variants', [])
                    )
                    
                    # Get price from first variant
                    if product.get('variants'):
                        variant = product['variants'][0]
                        product_info.price = variant.get('price')
                        product_info.compare_at_price = variant.get('compare_at_price')
                    
                    products.append(product_info)
                
                return products
                
        except Exception:
            pass
            
        return None

    async def _get_hero_products(self, website_url: str) -> Optional[List[ProductInfo]]:
        """Get hero products from homepage"""
        try:
            response = self.session.get(website_url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            hero_products = []
            
            # Look for product links on homepage
            product_links = soup.find_all('a', href=re.compile(r'/products/'))
            seen_products = set()
            
            for link in product_links[:10]:  # Limit to first 10 found
                href = link.get('href')
                if href and href not in seen_products:
                    seen_products.add(href)
                    
                    # Try to extract product info from the link element
                    title_elem = link.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                    if not title_elem:
                        title_elem = link.find(class_=re.compile(r'title|name|product'))
                    
                    price_elem = link.find(class_=re.compile(r'price|cost|amount'))
                    img_elem = link.find('img')
                    
                    product_info = ProductInfo(
                        title=title_elem.get_text().strip() if title_elem else None,
                        price=price_elem.get_text().strip() if price_elem else None,
                        images=[img_elem.get('src')] if img_elem else None
                    )
                    
                    if product_info.title:  # Only add if we found a title
                        hero_products.append(product_info)
            
            return hero_products if hero_products else None
            
        except Exception:
            return None

    async def _get_privacy_policy(self, website_url: str) -> Optional[str]:
        """Get privacy policy content"""
        try:
            # Common privacy policy URLs
            privacy_urls = [
                '/pages/privacy-policy',
                '/policies/privacy-policy',
                '/privacy-policy',
                '/privacy'
            ]
            
            for path in privacy_urls:
                try:
                    url = urljoin(website_url, path)
                    response = self.session.get(url, timeout=self.timeout)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Remove script and style elements
                        for script in soup(["script", "style"]):
                            script.decompose()
                        
                        # Get text content
                        text = soup.get_text()
                        lines = (line.strip() for line in text.splitlines())
                        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                        text = ' '.join(chunk for chunk in chunks if chunk)
                        
                        if len(text) > 100:  # Only return if substantial content
                            return text[:5000]  # Limit to 5000 chars
                            
                except Exception:
                    continue
                    
            return None
            
        except Exception:
            return None

    async def _get_return_policy(self, website_url: str) -> Optional[str]:
        """Get return/refund policy content"""
        try:
            # Common return policy URLs
            return_urls = [
                '/pages/return-policy',
                '/pages/refund-policy',
                '/policies/refund-policy',
                '/return-policy',
                '/refund-policy',
                '/pages/returns',
                '/returns'
            ]
            
            for path in return_urls:
                try:
                    url = urljoin(website_url, path)
                    response = self.session.get(url, timeout=self.timeout)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Remove script and style elements
                        for script in soup(["script", "style"]):
                            script.decompose()
                        
                        # Get text content
                        text = soup.get_text()
                        lines = (line.strip() for line in text.splitlines())
                        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                        text = ' '.join(chunk for chunk in chunks if chunk)
                        
                        if len(text) > 100:  # Only return if substantial content
                            return text[:5000]  # Limit to 5000 chars
                            
                except Exception:
                    continue
                    
            return None
            
        except Exception:
            return None

    async def _get_faqs(self, website_url: str) -> Optional[List[FAQ]]:
        """Get FAQ content"""
        try:
            # Common FAQ URLs
            faq_urls = [
                '/pages/faq',
                '/pages/faqs',
                '/faq',
                '/faqs',
                '/pages/frequently-asked-questions',
                '/help'
            ]
            
            for path in faq_urls:
                try:
                    url = urljoin(website_url, path)
                    response = self.session.get(url, timeout=self.timeout)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        faqs = []
                        
                        # Look for FAQ patterns
                        # Pattern 1: Question-Answer pairs in specific elements
                        qa_pairs = soup.find_all(['div', 'section'], class_=re.compile(r'faq|question|qa'))
                        
                        for qa in qa_pairs:
                            question_elem = qa.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'b'])
                            if question_elem:
                                question = question_elem.get_text().strip()
                                
                                # Look for answer after question
                                answer_elem = question_elem.find_next_sibling(['p', 'div', 'span'])
                                if answer_elem:
                                    answer = answer_elem.get_text().strip()
                                    if question and answer and len(question) > 10:
                                        faqs.append(FAQ(question=question, answer=answer))
                        
                        # Pattern 2: Look for structured FAQ data
                        if not faqs:
                            questions = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'], string=re.compile(r'\?'))
                            for q in questions[:10]:  # Limit to 10
                                question = q.get_text().strip()
                                answer_elem = q.find_next_sibling(['p', 'div'])
                                if answer_elem:
                                    answer = answer_elem.get_text().strip()
                                    if question and answer:
                                        faqs.append(FAQ(question=question, answer=answer))
                        
                        if faqs:
                            return faqs[:20]  # Limit to 20 FAQs
                            
                except Exception:
                    continue
                    
            return None
            
        except Exception:
            return None

    async def _get_social_handles(self, website_url: str) -> Optional[SocialHandles]:
        """Extract social media handles"""
        try:
            response = self.session.get(website_url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            social_handles = SocialHandles()
            
            # Find all social media links
            social_links = soup.find_all('a', href=re.compile(r'(instagram|facebook|twitter|tiktok|youtube|linkedin)'))
            
            for link in social_links:
                href = link.get('href', '')
                
                if 'instagram.com' in href:
                    social_handles.instagram = href
                elif 'facebook.com' in href:
                    social_handles.facebook = href
                elif 'twitter.com' in href or 'x.com' in href:
                    social_handles.twitter = href
                elif 'tiktok.com' in href:
                    social_handles.tiktok = href
                elif 'youtube.com' in href:
                    social_handles.youtube = href
                elif 'linkedin.com' in href:
                    social_handles.linkedin = href
            
            # Check if any social handles were found
            if any([social_handles.instagram, social_handles.facebook, social_handles.twitter, 
                   social_handles.tiktok, social_handles.youtube, social_handles.linkedin]):
                return social_handles
                
            return None
            
        except Exception:
            return None

    async def _get_contact_details(self, website_url: str) -> Optional[ContactDetails]:
        """Extract contact details"""
        try:
            response = self.session.get(website_url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            contact_details = ContactDetails()
            
            # Get all text content
            text_content = soup.get_text()
            
            # Extract emails using regex
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = list(set(re.findall(email_pattern, text_content)))
            
            # Filter out common non-contact emails
            filtered_emails = [email for email in emails if not any(
                skip in email.lower() for skip in ['example', 'test', 'noreply', 'no-reply']
            )]
            
            if filtered_emails:
                contact_details.emails = filtered_emails[:5]  # Limit to 5 emails
            
            # Extract phone numbers using regex
            phone_pattern = r'(\+?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4})'
            phones = list(set(re.findall(phone_pattern, text_content)))
            
            if phones:
                contact_details.phone_numbers = phones[:3]  # Limit to 3 phones
            
            # Try to get address from contact page
            contact_urls = ['/pages/contact', '/contact', '/pages/contact-us', '/contact-us']
            
            for path in contact_urls:
                try:
                    url = urljoin(website_url, path)
                    contact_response = self.session.get(url, timeout=self.timeout)
                    
                    if contact_response.status_code == 200:
                        contact_soup = BeautifulSoup(contact_response.content, 'html.parser')
                        
                        # Look for address patterns
                        address_elem = contact_soup.find(string=re.compile(r'\d+.*(?:street|st|avenue|ave|road|rd|drive|dr|lane|ln)', re.IGNORECASE))
                        if address_elem:
                            contact_details.address = address_elem.strip()[:200]
                            break
                            
                except Exception:
                    continue
            
            # Check if any contact details were found
            if any([contact_details.emails, contact_details.phone_numbers, contact_details.address]):
                return contact_details
                
            return None
            
        except Exception:
            return None

    async def _get_brand_context(self, website_url: str) -> Optional[str]:
        """Get brand context/about information"""
        try:
            # Try about page first
            about_urls = ['/pages/about', '/about', '/pages/about-us', '/about-us', '/pages/our-story', '/our-story']
            
            for path in about_urls:
                try:
                    url = urljoin(website_url, path)
                    response = self.session.get(url, timeout=self.timeout)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Remove script and style elements
                        for script in soup(["script", "style"]):
                            script.decompose()
                        
                        # Get text content
                        text = soup.get_text()
                        lines = (line.strip() for line in text.splitlines())
                        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                        text = ' '.join(chunk for chunk in chunks if chunk)
                        
                        if len(text) > 100:  # Only return if substantial content
                            return text[:3000]  # Limit to 3000 chars
                            
                except Exception:
                    continue
            
            # If no about page, try to get from homepage
            try:
                response = self.session.get(website_url, timeout=self.timeout)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for brand description in meta tags
                description_meta = soup.find('meta', attrs={'name': 'description'})
                if description_meta:
                    description = description_meta.get('content', '').strip()
                    if len(description) > 50:
                        return description
                
            except Exception:
                pass
                
            return None
            
        except Exception:
            return None

    async def _get_important_links(self, website_url: str) -> Optional[ImportantLinks]:
        """Get important links like order tracking, contact, blogs"""
        try:
            response = self.session.get(website_url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            important_links = ImportantLinks()
            
            # Find all links
            all_links = soup.find_all('a', href=True)
            
            for link in all_links:
                href = link.get('href', '').lower()
                text = link.get_text().lower().strip()
                
                # Make absolute URL
                full_url = urljoin(website_url, link.get('href'))
                
                # Order tracking
                if any(keyword in href or keyword in text for keyword in ['track', 'order', 'tracking']):
                    if not important_links.order_tracking:
                        important_links.order_tracking = full_url
                
                # Contact us
                elif any(keyword in href or keyword in text for keyword in ['contact', 'support']):
                    if not important_links.contact_us:
                        important_links.contact_us = full_url
                
                # Blogs
                elif any(keyword in href or keyword in text for keyword in ['blog', 'news', 'article']):
                    if not important_links.blogs:
                        important_links.blogs = full_url
                
                # About us
                elif any(keyword in href or keyword in text for keyword in ['about', 'story']):
                    if not important_links.about_us:
                        important_links.about_us = full_url
                
                # Shipping info
                elif any(keyword in href or keyword in text for keyword in ['shipping', 'delivery']):
                    if not important_links.shipping_info:
                        important_links.shipping_info = full_url
            
            # Check if any important links were found
            if any([important_links.order_tracking, important_links.contact_us, important_links.blogs,
                   important_links.about_us, important_links.shipping_info]):
                return important_links
                
            return None
            
        except Exception:
            return None