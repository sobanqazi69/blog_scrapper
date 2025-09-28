# Dawn.com Scraper API Documentation

## 🌐 Base URL
```
https://blog-scrapper-teal.vercel.app
```

## 📋 Complete API Endpoints

### 🏠 **Root & Information**

#### `GET /`
- **Description:** Get API information and endpoint list
- **URL:** `https://blog-scrapper-teal.vercel.app/`
- **Response:** API status, version, and available endpoints

#### `GET /health`
- **Description:** Health check endpoint
- **URL:** `https://blog-scrapper-teal.vercel.app/health`
- **Response:** Service health status and timestamp

#### `GET /docs`
- **Description:** Interactive API documentation (Swagger UI)
- **URL:** `https://blog-scrapper-teal.vercel.app/docs`
- **Response:** Interactive API documentation interface

---

### 📰 **Article Management**

#### `GET /articles`
- **Description:** Get all articles with pagination
- **URL:** `https://blog-scrapper-teal.vercel.app/articles`
- **Query Parameters:**
  - `page` (optional): Page number (default: 1)
  - `page_size` (optional): Articles per page (default: 10, max: 100)
- **Example:** `https://blog-scrapper-teal.vercel.app/articles?page=1&page_size=20`

#### `GET /articles/{article_id}`
- **Description:** Get specific article by ID
- **URL:** `https://blog-scrapper-teal.vercel.app/articles/{article_id}`
- **Example:** `https://blog-scrapper-teal.vercel.app/articles/1`

#### `GET /articles/category/{category}`
- **Description:** Get articles by category
- **URL:** `https://blog-scrapper-teal.vercel.app/articles/category/{category}`
- **Query Parameters:**
  - `page` (optional): Page number (default: 1)
  - `page_size` (optional): Articles per page (default: 10)
- **Example:** `https://blog-scrapper-teal.vercel.app/articles/category/World?page=1&page_size=5`

#### `GET /articles/search`
- **Description:** Search articles by title or content
- **URL:** `https://blog-scrapper-teal.vercel.app/articles/search`
- **Query Parameters:**
  - `q` (required): Search term
  - `page` (optional): Page number (default: 1)
  - `page_size` (optional): Articles per page (default: 10)
- **Example:** `https://blog-scrapper-teal.vercel.app/articles/search?q=Pakistan&page=1&page_size=10`

---

### 🔧 **Scraping Operations**

#### `POST /scrape`
- **Description:** Trigger manual scraping
- **URL:** `https://blog-scrapper-teal.vercel.app/scrape`
- **Query Parameters:**
  - `max_articles` (optional): Maximum articles to scrape (default: 10)
- **Example:** `https://blog-scrapper-teal.vercel.app/scrape?max_articles=20`

#### `POST /scraper/run`
- **Description:** Run scraper immediately and return results
- **URL:** `https://blog-scrapper-teal.vercel.app/scraper/run`
- **Method:** POST
- **Response:** Scraping results with article counts

#### `POST /scraper/start`
- **Description:** Start background scraper (limited on serverless)
- **URL:** `https://blog-scrapper-teal.vercel.app/scraper/start`
- **Method:** POST

#### `POST /scraper/stop`
- **Description:** Stop background scraper
- **URL:** `https://blog-scrapper-teal.vercel.app/scraper/stop`
- **Method:** POST

#### `GET /scraper/status`
- **Description:** Check scraper status
- **URL:** `https://blog-scrapper-teal.vercel.app/scraper/status`
- **Response:** Scraper running status and thread information

---

### 📊 **Statistics & Monitoring**

#### `GET /stats`
- **Description:** Get scraping statistics and category counts
- **URL:** `https://blog-scrapper-teal.vercel.app/stats`
- **Response:** Total articles, category breakdown, and other statistics

---

### 🗄️ **Database Management**

#### `GET /db-test`
- **Description:** Test database connection
- **URL:** `https://blog-scrapper-teal.vercel.app/db-test`
- **Response:** Database connection status and test results

#### `GET /db-info`
- **Description:** Get detailed database information
- **URL:** `https://blog-scrapper-teal.vercel.app/db-info`
- **Response:** Database configuration, table status, and article count

#### `POST /db-activate`
- **Description:** Safely activate/initialize database without destroying existing data
- **URL:** `https://blog-scrapper-teal.vercel.app/db-activate`
- **Method:** POST
- **Response:** Database activation status and current article count

#### `GET /db-refresh`
- **Description:** Refresh database connection and show current status
- **URL:** `https://blog-scrapper-teal.vercel.app/db-refresh`
- **Response:** Database refresh status and current article count

---

### 🚫 **Error Handling Endpoints**

#### `GET /favicon.ico`
- **Description:** Handle favicon requests
- **URL:** `https://blog-scrapper-teal.vercel.app/favicon.ico`
- **Response:** 404 Not Found

#### `GET /favicon.png`
- **Description:** Handle favicon requests
- **URL:** `https://blog-scrapper-teal.vercel.app/favicon.png`
- **Response:** 404 Not Found

#### `GET /robots.txt`
- **Description:** Handle robots.txt requests
- **URL:** `https://blog-scrapper-teal.vercel.app/robots.txt`
- **Response:** 404 Not Found

---

## 🎯 **Quick Start Examples**

### Run Scraper
```bash
curl -X POST "https://blog-scrapper-teal.vercel.app/scraper/run"
```

### Get All Articles
```bash
curl "https://blog-scrapper-teal.vercel.app/articles"
```

### Get Articles with Pagination
```bash
curl "https://blog-scrapper-teal.vercel.app/articles?page=1&page_size=5"
```

### Search Articles
```bash
curl "https://blog-scrapper-teal.vercel.app/articles/search?q=Pakistan"
```

### Get Articles by Category
```bash
curl "https://blog-scrapper-teal.vercel.app/articles/category/World"
```

### Check Statistics
```bash
curl "https://blog-scrapper-teal.vercel.app/stats"
```

### Activate Database (if having issues)
```bash
curl -X POST "https://blog-scrapper-teal.vercel.app/db-activate"
```

### Check Scraper Status
```bash
curl "https://blog-scrapper-teal.vercel.app/scraper/status"
```

---

## 📝 **Response Format**

All endpoints return JSON responses with the following structure:

### Success Response
```json
{
  "status": "success",
  "message": "Operation completed successfully",
  "data": { ... },
  "timestamp": "2025-09-28T14:22:14.246178"
}
```

### Error Response
```json
{
  "status": "error",
  "message": "Error description",
  "detail": "Detailed error information",
  "timestamp": "2025-09-28T14:22:14.246178"
}
```

---

## 🔧 **Troubleshooting**

### Database Issues
If you're experiencing database issues (articles not showing), use:
1. `POST /db-activate` - Initialize database
2. `GET /db-refresh` - Check database status
3. `GET /db-info` - Get detailed database information

### Scraper Issues
If scraper is not working:
1. `GET /scraper/status` - Check scraper status
2. `POST /scraper/run` - Run scraper manually
3. `GET /stats` - Check if articles are being saved

---

## 📞 **Support**

For issues or questions:
- Check the interactive documentation at: `https://blog-scrapper-teal.vercel.app/docs`
- Use the health check endpoint: `https://blog-scrapper-teal.vercel.app/health`
- Monitor scraper status: `https://blog-scrapper-teal.vercel.app/scraper/status`
