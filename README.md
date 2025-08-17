# Shopify Store Insights Fetcher

A robust Python FastAPI application that scrapes and analyzes Shopify store data to extract comprehensive brand insights without using the official Shopify API.

## Features

### Mandatory Requirements ✅
- **Complete Product Catalog**: Fetches all products using `/products.json` endpoint
- **Hero Products**: Extracts featured products from homepage
- **Privacy Policy**: Scrapes privacy policy content
- **Return/Refund Policies**: Extracts return and refund policy information
- **Brand FAQs**: Collects frequently asked questions and answers
- **Social Media Handles**: Discovers Instagram, Facebook, Twitter, TikTok, YouTube, LinkedIn profiles
- **Contact Details**: Extracts emails, phone numbers, and addresses
- **Brand Context**: Gets "About Us" information and brand story
- **Important Links**: Finds order tracking, contact, blog, and shipping information

### Bonus Features 🎯
- **Database Persistence**: SQLite database for storing scraped data
- **Structured Data Models**: Pydantic schemas for clean data validation
- **Error Handling**: Comprehensive error handling with appropriate HTTP status codes
- **RESTful API Design**: Clean, well-documented API endpoints
- **Extensible Architecture**: Modular design following SOLID principles

## API Endpoints

### Main Endpoint
```
POST /api/v1/shopify/fetch-insights
```

**Request Body:**
```json
{
  "website_url": "https://example-store.com"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "website_url": "https://example-store.com",
    "brand_name": "Example Store",
    "product_catalog": [...],
    "hero_products": [...],
    "privacy_policy": "...",
    "return_refund_policy": "...",
    "faqs": [...],
    "social_handles": {...},
    "contact_details": {...},
    "brand_context": "...",
    "important_links": {...},
    "scraped_at": "2024-01-01T00:00:00Z",
    "scraping_status": "completed"
  },
  "status_code": 200
}
```

### Additional Endpoints
- `GET /health` - Health check
- `GET /api/v1/shopify/health` - Scraper service health
- `GET /api/v1/shopify/test-scraper/{url}` - Quick connectivity test
- `GET /docs` - Interactive API documentation (Swagger UI)

## Installation & Setup

1. **Clone and navigate to project:**
```bash
cd shopify-insights-fetcher
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

4. **Access the API:**
- API Base URL: `http://localhost:8001`
- Interactive Docs: `http://localhost:8001/docs`
- Health Check: `http://localhost:8001/health`

## Usage Examples

### Using cURL
```bash
curl -X POST "http://localhost:8001/api/v1/shopify/fetch-insights" \
     -H "Content-Type: application/json" \
     -d '{"website_url": "https://memy.co.in"}'
```

### Using Python requests
```python
import requests

response = requests.post(
    "http://localhost:8001/api/v1/shopify/fetch-insights",
    json={"website_url": "https://memy.co.in"}
)

data = response.json()
print(data)
```

### Test Script
Run the included test script:
```bash
python test_api.py
```


### Key Components

1. **ShopifyScraper**: Core scraping engine with intelligent extraction methods
2. **Pydantic Models**: Type-safe data validation and serialization
3. **SQLAlchemy Models**: Database persistence layer
4. **FastAPI Endpoints**: RESTful API with automatic documentation
5. **Error Handling**: Comprehensive exception management

## Data Extraction Strategy

### Products
- Primary: `/products.json` endpoint for complete catalog
- Secondary: Homepage scraping for hero products

### Policies & Content
- Multiple URL patterns for privacy/return policies
- Smart text extraction and cleaning
- Content length validation

### Contact Information
- Regex-based email and phone extraction
- Social media link discovery
- Address pattern matching

### FAQ Extraction
- Multiple pattern recognition approaches
- Question-answer pairing algorithms
- Structured data organization

## Error Handling

The API returns appropriate HTTP status codes:
- `200` - Success
- `404` - Website not found
- `408` - Request timeout
- `500` - Internal server error
- `503` - Service unavailable

## Testing

### Reference Shopify Stores
- `memy.co.in`
- `hairoriginals.com`
- See: https://webinopoly.com/blogs/news/top-100-most-successful-shopify-stores

### Performance
- Request timeout: 30 seconds
- Retry mechanism: 3 attempts
- Concurrent request handling
- Memory-efficient data processing

## Security & Best Practices

- User-Agent rotation for ethical scraping
- Rate limiting compliance
- Clean data sanitization
- Input validation
- SQL injection prevention
- CORS configuration

## Future Enhancements

- Competitor analysis implementation
- Advanced caching mechanisms
- Batch processing capabilities
- Real-time monitoring
- Machine learning insights
- Export functionality (CSV, Excel)

## License

This project is for educational and development purposes. Please ensure compliance with website terms of service and robots.txt when scraping.
