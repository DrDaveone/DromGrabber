import json, time, csv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

path = "result" + time.strftime('%d%m%y')
links, data = [], []


def csv_writer(data, path):
    with open(path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        for line in data:
            writer.writerow(line)


driver = webdriver.Chrome(
    executable_path=r"C:\Users\mark-\PycharmProjects\chromedriver.exe")
driver.get('https://baza.drom.ru/user/CarZilla/')
print('пролистывание до конца')
pages = int(driver.find_element_by_class_name(
    'pageCount').text.replace('Всего ', '').replace(' страниц', ''))
for r in pages:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
print('Пролистывание закончено')

topics = driver.find_elements_by_class_name("bull-item__self-link")
for num, item in enumerate(topics):
    links.append(item.get_attribute('href'))
    print(num)
# узнаем ценник
for num, link in enumerate(links):
    driver.get(link)
    print('делается', links.index(link) + 1, 'из', len(links))
    try:  # проверка на наличие цены
        price = driver.find_element_by_xpath(
            '//*[@id="fieldsetView"]/div/div[1]/div/div[1]/span')
        price = price.text.replace(' ', '')
    except NoSuchElementException:  # нет цены? мож это капча? проверяем
        try:
            driver.find_element_by_xpath(
                '/html/body/div[1]/div/div[3]/div[2]/div/h2')
            input()
            # ждем ответ от пользователя
            price = driver.find_element_by_xpath(
                '//*[@id="fieldsetView"]/div/div[1]/div/div[1]/span')
            price = price.text.replace(' ', '')
        except NoSuchElementException:  # не капча? ну точно цены нема
            price = '0'
            print('нет цены')
    #имя еще не забудем
    name = driver.find_elements_by_class_name('inplace')[0].text
    # ищем номера замен
    '''try:
        partsno = driver.find_element_by_class_name('oem-numbers__list').text+
                  driver.find_element_by_class_name('autoPartsOemNumber')
'''
    time.sleep(5)
    # объединяем данные
    tup = ('\t', num + 1,name, link, int(price.replace('₽', '')))
    data.append(tup)
    print(tup)

# save data
json.dump(data, open(path + ".json", "w"))
# sorted data dump
datamod = sorted(data, key=lambda adv: adv[3], reverse=True)
json.dump(datamod, open(path+'_sorted_by_price' + ".json", "w"))
# sorted data txt separated with tabs
f = open(path+'_sorted'+ ".txt", "w")
for num, item in enumerate(datamod):
    f.write(str(num + 1) + '\t' + str(item[1]) + '\t' + item[0] + '\n')
f.close()

csv_writer(datamod, path + ".csv")
driver.close()
