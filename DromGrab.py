import json, time, csv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

path = "Drom" + time.strftime('%d%m%y') + ".csv"
links, data = [], []


def csv_writer(data, path):
    with open(path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            writer.writerow(line)


driver = webdriver.Chrome(
    executable_path=r"C:\Users\mark-\PycharmProjects\chromedriver.exe")
driver.get('https://baza.drom.ru/user/CarZilla/')
print('пролистывание до конца')
for r in range(8):
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
            price = driver.find_element_by_xpath(
                '//*[@id="fieldsetView"]/div/div[1]/div/div[1]/span')
            price = price.text.replace(' ', '')
        except NoSuchElementException:  # не капча? ну точно цены нема
            price = '0'
            print('нет цены')
    time.sleep(5)
    # объединяем данные
    tup = ('\t', num + 1, link, int(price.replace('₽', '')))
    data.append(tup)
    print(tup)

# save data
json.dump(data, open("Drom" +
                     time.strftime('%d%m%y') + ".json", "w"))
# sorted data dump
datamod = sorted(data, key=lambda adv: adv[3], reverse=True)
json.dump(datamod, open("DromSortedByPrice" +
                        time.strftime('%d%m%y') + ".json", "w"))
# sorted data txt separated with tabs
f = open("dromlistSortedByprice" + time.strftime('%d%m%y') + ".txt", "w")
for num, item in enumerate(datamod):
    f.write(str(num + 1) + '\t' + str(item[1]) + '\t' + item[0] + '\n')
f.close()

csv_writer(datamod, path)
driver.close()
