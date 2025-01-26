import time
import os
from data import ameegoData
from navigation import clearviewScrapper, ameegoScrapper


data = ameegoData.load_data('employee_shifts_2025-01-24.csv')
ameegoScrapper.ameegoScrap()

