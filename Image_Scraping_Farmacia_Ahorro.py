import requests, io, random
from time import sleep
from PIL import Image
# SELENIUM
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def saving_photo(directory_path, img_online_location, image_number=1):
    """This function saves a photo that comes from internet."""

    # Requesting the image:
    image_content = requests.get(img_online_location).content
    # Image processing:
    image_file = io.BytesIO(image_content)
    image = Image.open(image_file).convert('RGB')
    # Saving the image:
    file_path = f"{directory_path}/product_{image_number}.jpg"
    with open(file_path, 'wb') as f:
        image.save(f, "JPEG")


def creating_drivers(website_url):
    """This function allow us to create a new driver whenever it's necessary."""

    # Removes navigator.webdriver flag TO AVOID THE DRIVER TO BE DECTED AS A BOT (This works just for Chrome):
    opts = Options()
    opts.add_argument('--disable-blink-features=AutomationControlled')

    # Creating our driver:
    driver = webdriver.Chrome("./chromedriver.exe", options=opts)
    driver.get(website_url)

    return driver


# We will extract images from 5 pages, even though the pagination is longer:
urls_to_extract_images = [f"https://www.fahorro.com/belleza/derma.html?p={i}" for i in range(1,5+1,1)]
driver = creating_drivers("https://www.fahorro.com/belleza/derma.html")  # We initialize the driver.
image_number = 1
for i,page in enumerate(urls_to_extract_images, start=1):
    driver.get(page)
    sleep(random.uniform(1.5,2.5))
    product_images = driver.find_elements_by_xpath("//img[@class='product-image-photo']")
    for image in product_images:
        saving_photo("images_from_Farm_Ahorro", image.get_attribute("src"), image_number)
        image_number += 1
    print(f"Images from page {i} successfully downloaded and saved.")
driver.close()  # We close the driver session.
print("TOTAL IMAGES DOWNLOADED AND SAVED!")
