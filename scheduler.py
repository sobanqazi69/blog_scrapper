"""
Scheduler module for periodic Dawn.com article scraping.
This module handles automated scraping at regular intervals.
"""

import logging
import schedule
import time
import threading
from datetime import datetime
from typing import Optional

from scraper import run_dawn_scraper

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ScrapingScheduler:
    """
    Scheduler class for managing periodic article scraping.
    """
    
    def __init__(self, max_articles: int = 50):
        """
        Initialize the scheduler.
        
        Args:
            max_articles: Maximum number of articles to scrape per run
        """
        self.max_articles = max_articles
        self.is_running = False
        self.scheduler_thread: Optional[threading.Thread] = None
        self.stop_event = threading.Event()
        
    def scraping_job(self):
        """
        Job function to run scraping.
        This is called by the scheduler at regular intervals.
        """
        try:
            logger.info("Starting scheduled scraping job")
            start_time = datetime.utcnow()
            
            # Run the scraper
            stats = run_dawn_scraper(self.max_articles)
            
            end_time = datetime.utcnow()
            duration = (end_time - start_time).total_seconds()
            
            logger.info(
                f"Scheduled scraping completed in {duration:.2f} seconds. "
                f"Stats: {stats}"
            )
            
        except Exception as e:
            logger.error(f"Error in scheduled scraping job: {e}")
    
    def setup_schedule(self):
        """
        Set up the scraping schedule.
        Configure when and how often to run the scraping job.
        """
        try:
            # Clear any existing schedules
            schedule.clear()
            
            # Schedule scraping every hour
            schedule.every().hour.do(self.scraping_job)
            
            # Schedule scraping every 30 minutes during peak hours (8 AM to 10 PM)
            schedule.every(30).minutes.do(self.scraping_job)
            
            # Schedule scraping every 15 minutes during very active hours (9 AM to 6 PM)
            schedule.every(15).minutes.do(self.scraping_job)
            
            # Schedule a daily cleanup job at 2 AM
            schedule.every().day.at("02:00").do(self.daily_cleanup)
            
            logger.info("Scraping schedule configured successfully")
            
        except Exception as e:
            logger.error(f"Error setting up schedule: {e}")
            raise
    
    def daily_cleanup(self):
        """
        Daily cleanup job.
        This can be used for maintenance tasks like cleaning old data.
        """
        try:
            logger.info("Running daily cleanup job")
            
            # Add any cleanup tasks here
            # For example: remove old articles, optimize database, etc.
            
            logger.info("Daily cleanup completed")
            
        except Exception as e:
            logger.error(f"Error in daily cleanup: {e}")
    
    def start_scheduler(self):
        """
        Start the scheduler in a separate thread.
        """
        try:
            if self.is_running:
                logger.warning("Scheduler is already running")
                return
            
            # Set up the schedule
            self.setup_schedule()
            
            # Create and start the scheduler thread
            self.scheduler_thread = threading.Thread(
                target=self._run_scheduler,
                daemon=True,
                name="ScrapingScheduler"
            )
            
            self.is_running = True
            self.stop_event.clear()
            self.scheduler_thread.start()
            
            logger.info("Scheduler started successfully")
            
        except Exception as e:
            logger.error(f"Error starting scheduler: {e}")
            raise
    
    def stop_scheduler(self):
        """
        Stop the scheduler.
        """
        try:
            if not self.is_running:
                logger.warning("Scheduler is not running")
                return
            
            self.is_running = False
            self.stop_event.set()
            
            if self.scheduler_thread and self.scheduler_thread.is_alive():
                self.scheduler_thread.join(timeout=5)
            
            schedule.clear()
            logger.info("Scheduler stopped successfully")
            
        except Exception as e:
            logger.error(f"Error stopping scheduler: {e}")
    
    def _run_scheduler(self):
        """
        Main scheduler loop.
        This runs in a separate thread.
        """
        try:
            logger.info("Scheduler thread started")
            
            while self.is_running and not self.stop_event.is_set():
                try:
                    # Run pending jobs
                    schedule.run_pending()
                    
                    # Sleep for 1 minute before checking again
                    time.sleep(60)
                    
                except Exception as e:
                    logger.error(f"Error in scheduler loop: {e}")
                    time.sleep(60)  # Wait before retrying
            
            logger.info("Scheduler thread stopped")
            
        except Exception as e:
            logger.error(f"Fatal error in scheduler thread: {e}")
    
    def get_next_run_times(self) -> dict:
        """
        Get information about when the next jobs will run.
        
        Returns:
            Dictionary with next run times for each job
        """
        try:
            jobs = schedule.get_jobs()
            next_runs = {}
            
            for job in jobs:
                job_name = str(job.job_func)
                next_run = job.next_run
                if next_run:
                    next_runs[job_name] = next_run.isoformat()
            
            return next_runs
            
        except Exception as e:
            logger.error(f"Error getting next run times: {e}")
            return {}
    
    def is_scheduler_running(self) -> bool:
        """
        Check if the scheduler is currently running.
        
        Returns:
            True if scheduler is running, False otherwise
        """
        return self.is_running and self.scheduler_thread and self.scheduler_thread.is_alive()


# Global scheduler instance
_scheduler: Optional[ScrapingScheduler] = None


def get_scheduler() -> ScrapingScheduler:
    """
    Get the global scheduler instance.
    
    Returns:
        ScrapingScheduler instance
    """
    global _scheduler
    if _scheduler is None:
        _scheduler = ScrapingScheduler()
    return _scheduler


def start_scheduled_scraping(max_articles: int = 50):
    """
    Start scheduled scraping.
    
    Args:
        max_articles: Maximum number of articles to scrape per run
    """
    try:
        scheduler = get_scheduler()
        scheduler.max_articles = max_articles
        scheduler.start_scheduler()
        logger.info("Scheduled scraping started")
        
    except Exception as e:
        logger.error(f"Error starting scheduled scraping: {e}")
        raise


def stop_scheduled_scraping():
    """
    Stop scheduled scraping.
    """
    try:
        scheduler = get_scheduler()
        scheduler.stop_scheduler()
        logger.info("Scheduled scraping stopped")
        
    except Exception as e:
        logger.error(f"Error stopping scheduled scraping: {e}")
        raise


def get_scheduler_status() -> dict:
    """
    Get scheduler status information.
    
    Returns:
        Dictionary with scheduler status
    """
    try:
        scheduler = get_scheduler()
        
        return {
            "is_running": scheduler.is_scheduler_running(),
            "max_articles": scheduler.max_articles,
            "next_runs": scheduler.get_next_run_times(),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting scheduler status: {e}")
        return {
            "is_running": False,
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }


if __name__ == "__main__":
    # Example usage
    try:
        # Start scheduled scraping
        start_scheduled_scraping(max_articles=30)
        
        # Keep the main thread alive
        while True:
            time.sleep(60)
            
    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
        stop_scheduled_scraping()
        logger.info("Scheduler stopped")
