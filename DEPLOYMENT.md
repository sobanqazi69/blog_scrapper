# Deployment Guide for Dawn.com Article Scraper

This guide provides step-by-step instructions for deploying the Dawn.com article scraper to Vercel.

## Prerequisites

1. **Python 3.8+** installed on your local machine
2. **Vercel CLI** installed globally
3. **Git** for version control
4. **Vercel account** (free tier available)

## Local Development Setup

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt
```

### 2. Test the Application

```bash
# Run the test script to verify everything works
python test_scraper.py

# Start the application locally
python run.py
```

### 3. Verify API Endpoints

Once the application is running, test the endpoints:

```bash
# Test health check
curl http://localhost:8000/health

# Test getting articles
curl http://localhost:8000/articles

# Test scraping (this will take a few minutes)
curl -X POST http://localhost:8000/scrape?max_articles=5
```

## Vercel Deployment

### 1. Install Vercel CLI

```bash
npm install -g vercel
```

### 2. Login to Vercel

```bash
vercel login
```

### 3. Initialize Vercel Project

```bash
# In your project directory
vercel
```

Follow the prompts:
- Set up and deploy? **Yes**
- Which scope? **Your account**
- Link to existing project? **No**
- What's your project's name? **dawn-scraper** (or your preferred name)
- In which directory is your code located? **./**

### 4. Configure Environment Variables

In the Vercel dashboard or via CLI:

```bash
vercel env add DATABASE_URL
# Enter: sqlite:///./dawn_articles.db

vercel env add SCHEDULER_ENABLED
# Enter: true

vercel env add SCHEDULER_MAX_ARTICLES
# Enter: 30

vercel env add LOG_LEVEL
# Enter: INFO
```

### 5. Deploy

```bash
vercel --prod
```

## Post-Deployment Configuration

### 1. Verify Deployment

Visit your Vercel URL and check:
- `https://your-app.vercel.app/health` - Should return health status
- `https://your-app.vercel.app/docs` - Should show API documentation

### 2. Test Scraping

```bash
# Trigger initial scraping
curl -X POST "https://your-app.vercel.app/scrape?max_articles=10"

# Check if articles were scraped
curl "https://your-app.vercel.app/articles"
```

### 3. Monitor Logs

```bash
# View deployment logs
vercel logs

# View function logs
vercel logs --follow
```

## API Usage Examples

### Get All Articles

```bash
curl "https://your-app.vercel.app/articles?page=1&page_size=10"
```

### Get Articles by Category

```bash
curl "https://your-app.vercel.app/articles/category/Pakistan"
```

### Search Articles

```bash
curl "https://your-app.vercel.app/articles/search?q=cricket"
```

### Get Article by ID

```bash
curl "https://your-app.vercel.app/articles/1"
```

### Get Statistics

```bash
curl "https://your-app.vercel.app/stats"
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Ensure `DATABASE_URL` is set correctly
   - Check if SQLite is supported in your Vercel plan

2. **Scraping Failures**
   - Check if Dawn.com is accessible
   - Verify request headers and timeouts
   - Check Vercel function timeout limits

3. **Memory Issues**
   - Reduce `max_articles` parameter
   - Check Vercel function memory limits

4. **Rate Limiting**
   - Increase `SCRAPING_DELAY` in environment variables
   - Reduce scraping frequency

### Debugging

1. **Check Logs**
   ```bash
   vercel logs --follow
   ```

2. **Test Locally**
   ```bash
   python test_scraper.py
   ```

3. **Verify Configuration**
   ```bash
   vercel env ls
   ```

## Performance Optimization

### 1. Database Optimization

- Consider upgrading to PostgreSQL for production
- Implement database indexing for better query performance
- Add connection pooling for high-traffic scenarios

### 2. Scraping Optimization

- Implement caching mechanisms
- Use async/await for concurrent requests
- Add retry logic for failed requests

### 3. API Optimization

- Implement response caching
- Add pagination for large datasets
- Use compression for API responses

## Monitoring and Maintenance

### 1. Health Monitoring

Set up monitoring for:
- API endpoint availability
- Database connection status
- Scraping success rates
- Error rates and response times

### 2. Regular Maintenance

- Monitor database size and performance
- Update dependencies regularly
- Review and optimize scraping patterns
- Monitor Dawn.com for structural changes

### 3. Backup Strategy

- Regular database backups
- Configuration backup
- Code version control

## Scaling Considerations

### 1. Database Scaling

- Migrate to PostgreSQL for better performance
- Implement read replicas for high read loads
- Consider database sharding for large datasets

### 2. API Scaling

- Implement rate limiting
- Add API authentication if needed
- Consider CDN for static content

### 3. Scraping Scaling

- Implement distributed scraping
- Add multiple scraping sources
- Implement queue-based processing

## Security Considerations

### 1. API Security

- Implement API authentication
- Add rate limiting
- Validate input parameters
- Sanitize output data

### 2. Data Security

- Encrypt sensitive data
- Implement access controls
- Regular security audits
- Monitor for suspicious activity

## Cost Optimization

### 1. Vercel Optimization

- Monitor function execution time
- Optimize cold start times
- Use appropriate function memory settings
- Monitor bandwidth usage

### 2. Database Optimization

- Implement data retention policies
- Optimize query performance
- Consider data archiving strategies

## Support and Maintenance

### 1. Documentation

- Keep API documentation updated
- Document configuration changes
- Maintain troubleshooting guides

### 2. Updates

- Regular dependency updates
- Monitor for security patches
- Test updates in staging environment

### 3. Monitoring

- Set up alerts for critical issues
- Monitor performance metrics
- Track usage patterns

## Conclusion

This deployment guide provides comprehensive instructions for deploying and maintaining the Dawn.com article scraper on Vercel. Follow the steps carefully and monitor the application after deployment to ensure optimal performance.

For additional support or questions, refer to the main README.md file or create an issue in the repository.
