'''
список объявлений получать через селениум
а данные из объявления получать через bs4
'''
import json
import time
from selenium import webdriver

driver = webdriver.Chrome(
    executable_path=r"C:\Users\mark-\PycharmProjects\chromedriver.exe")
driver.get('https://baza.drom.ru/user/CarZilla/')

print('пролистывание до конца')
for r in range(10):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
print('Пролистывание закончено')
links = []
topics = driver.find_elements_by_class_name("bull-item__self-link")
for num, item in enumerate(topics):
    links.append(item.get_attribute('href'))
'''f = open("dromlist.txt", "w+")
for items in links:
    f.write(items + '\n')
f.close()'''
priceF, partnoF, partreplaceF, suitsFF = [], [], [], []
check = ''
print('добываем данные с объявления')
''' список ссылок отсортированный
структура базы:
список из списков,
main - главный список объявлений
далее список объявления - offer
1) ссылка
2) название лота
3) цена
4) список парт.номеров и замен в одном
5) левый, правый
6) перед, зад
7) производитель авто
8) модель авто
9) номер кузова
10) модель двигателя
11) текст объявления'''
for link in links:
    driver.get(link)
    time.sleep(2)
    check = driver.find_element_by_xpath(
        '//*[@id="breadcrumbs"]/ol/li[3]/a/span')
    if check.text == 'Автозапчасти':
        print('делается', links.index(link) + 1, 'из', len(links))
        price = driver.find_element_by_xpath(
            '//*[@id="fieldsetView"]/div/div[1]/div/div[1]/span')
        priceF.append(price.text.replace('₽', ''))
        print('цена найдена')
        print('Номер запчасти')
            try:
                partno = driver.find_element_by_xpath(
                    '//*[@id="fieldsetView"]/div/div[6]/div[2]/span')
                partReplace = ''
            except:
                print('чото не нашлось')
        try:
            print('ищем номер замены')
            partReplace = driver.find_element_by_class_name('oem-numbers')
            partno = partno.text + ' ' + partReplace.text
        except:
            print('номер замены не найден')
        finally:
            partno = partno.text
        partnoF.append(partno)
        try:
            print('ищем текст объявы')
            textpost = driver.find_element_by_class_name('bulletinText')
            textpost = textpost.text
        except:
            print('текст объявы не найден')
        print('ищем номера замен')
        try:
            suitsFor = driver.find_element_by_class_name(
                's-exact-compatibility')
            suitsFF.append(suitsFor.text.replace('Для моделей\n', ''))
        except:
            print('номера замен не обнаружены')
        print('выполнено объявление', links.index(link) + 1, 'из', len(links))

# Второй вариант через BS4
from bs4 import BeautifulSoup
import requests as req

db = []
for link in links:
    a = []
    resp = req.get(link)
    soup = BeautifulSoup(resp.text, 'html5lib')
    partnoF.append(soup.find(
        attrs={'data-field': 'autoPartsOemNumber'}))  # номер запчасти
    partnoF.append(soup.find_all(
    attrs={'class': 'oem-numbers__item auto-shy'}))  # номер замены
    soup.next_element(partnoF[0])
    images = soup.find_all(attrs={'class': 'bulletinImages'}) #фотографии
    driver.find_all(attrs={'class': 'bulletinText'})
