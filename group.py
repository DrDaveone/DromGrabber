import vk_api
import PIL
from PIL import Image
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def main():
    driver = webdriver.Chrome(
        executable_path=r"C:\Users\mark-\PycharmProjects\chromedriver.exe")
    driver.get('https://baza.drom.ru/user/CarZilla/')
    id = 160890783

    # def getPostLinks():
    print('пролистывание до конца')
    for r in range(10):
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    print('Пролистывание закончено')
    links = []
    topics = driver.find_elements_by_class_name("bull-item__self-link")
    for num, item in enumerate(topics):
        links.append(item.get_attribute('href'))
    f = open("dromlist.txt", "w+")
    for items in links:
        f.write(items + '\n')
    f.close()
    price = []
    # def GetInfoFromPage():
    for link in links:
        driver.get(link)
        time.sleep(2)
        pp = driver.find_element_by_xpath(
            '//*[@id="fieldsetView"]/div/div[1]/div/div[1]/span')
        price.append(pp.text)


def VkAuth():
    login, password = "mark-kraevskijj@rambler.ru", "Dr.Dave_one208559911"
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    tools = vk_api.VkTools(vk_session)
    vk = vk_session.get_api()


"""
Name - название товара, description - описание, price = цена,
main_photo_id - главная фотка в вк с обрезом, photo_ids - доп фотки
"""


def photo():
    image = Image.open
    x, y = image.size
    crop = 0
    if x > y:
        crop = y
    else:
        crop = x
    vk.photos.getMarketUploadServer(group_id=id, main_photo=1, crop_x=crop,
                                    crop_y=crop, crop_width=crop)


''' banned for now
def MarketPost():
    vk.market.add(owner_id=-id, name=name, price=price.get_attribute(text), category_id=404,
                  main_photo_id=main_photo_id, url=)
'''

VkAuth()
# getPostLinks()
# GetInfoFromPage()

if __name__ == '__main__':
    main()
