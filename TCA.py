import time
import os
from data import ameegoData
from navigation import clearviewScrapper, ameegoScrapper
import tkinter as tk

# Function to close the application
def close_app():
    # Close the drivers if they are running
    if 'clearviewScrapper' in globals() and hasattr(clearviewScrapper, 'driver'):
        clearviewScrapper.driver.quit()
    if 'ameegoScrapper' in globals() and hasattr(ameegoScrapper, 'driver'):
        ameegoScrapper.driver.quit()
    # Send 'q' to the terminal as a keyboard input
    os.system('echo q')
    root.destroy()
def scrap_clearview():
    clearviewScrapper.clearviewScrap()
    result_label.config(text="Clearview scraping completed.")

def scrap_ameego():
    ameegoScrapper.ameegoScrap()
    result_label.config(text="Ameego scraping completed.")
 # Create the main window
root = tk.Tk()
root.title("Scraping Interface")

# Create a button to start scraping
scrap_button = tk.Button(root, text="Scrap Ameego", command=scrap_ameego)
scrap_button.pack(pady=20)

# Create a button to start Clearview scraping
scrap_clearview_button = tk.Button(root, text="Scrap Clearview", command=scrap_clearview)
scrap_clearview_button.pack(pady=20)

# Create a button to close the application
close_button = tk.Button(root, text="Close", command=close_app)
close_button.pack(pady=20)

# Create a label to display the result
result_label = tk.Label(root, text="")
result_label.pack(pady=20)

# Ensure the application closes when the close button is pressed
root.protocol("WM_DELETE_WINDOW", close_app)

# Run the application
root.mainloop()

