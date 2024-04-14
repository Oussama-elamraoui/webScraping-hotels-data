import os
import sys
from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

sys.stdout.reconfigure(encoding='utf-8')


# -*- coding: utf-8 -*-


def create_path():
    try:
        path = os.path.join('CITY', search_city)
        os.makedirs(path, exist_ok=True)

        path = f'{path}\\{sql_name}'

        create_table_sql = f'''CREATE TABLE {table_name} (
            Hotel_ID INT NOT NULL, 
            Lat TEXT NOT NULL,
            Long TEXT NOT NULL,
            Hotel_Name TEXT NOT NULL, 
            City TEXT NOT NULL, 
            Date TEXT NOT NULL, 
            Prices TEXT);'''

        if not os.path.exists(path):
            with open(path, 'w') as sql:
                sql.write(create_table_sql + '\n')
            print(f'"{path}" created...')
        else:
            print(f'"{path}" already exist...')

        return path

    except Exception as ex:
        print("Error ->>", ex)


def get_driver(headless=False):
    agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/116.0.1216.0 Safari/537.2'
    # s = Service(executable_path=ChromeDriverManager().install())
    # s = Service(executable_path='chromedriver.exe')
    chrome_option = webdriver.ChromeOptions()
    if headless:
        chrome_option.add_argument('--headless')
        chrome_option.add_argument(f'user-agent={agent}')
    chrome_option.add_argument("--no-sandbox")
    chrome_option.add_argument("--disable-dev-shm-usage")
    web_driver = webdriver.Chrome(options=chrome_option)
    web_driver.set_window_position(325, 30)
    return web_driver


def city_search_action():
    try:
        driver.execute_script('''return document.querySelector('[aria-label="Dismiss sign-in info."]').click();''')
    except:
        pass
    try:
        search_bar = driver.find_element(By.ID, ':re:')
        search_bar.clear()
        sleep(1)
        search_bar.send_keys(search_city)
        sleep(2)
        driver.execute_script('''return document.querySelector('[data-testid="autocomplete-result"]').click();''')
        driver.execute_script('''return document.querySelector('[type="submit"]').click();''')

        return True

    except:
        print('Unable to search city...')
        sleep(5)
        exit()


def check_month_year_name(month_year):
    # -*- coding: utf-8 -*-
    month_name = month_year.split(' ')[0].capitalize()
    print(f'\n{" " * 25}[ {month_name} ]')
    month_year_data = {
        'Janvier': 'January',
        'Février': 'February',
        'Mars': 'March',
        'Avril': 'April',
        'Mai': 'May',
        'Juin': 'June',
        'Juillet': 'July',
        'Août': 'August',
        'Septembre': 'September',
        'Octobre': 'October',
        'Novembre': 'November',
        'Décembre': 'December'
    }

    if month_name in month_year_data:
        result = month_year_data[month_name] + ' ' + month_year.split(' ')[1]
    else:
        result = month_year

    return result


def file_format(data_format_list):
    print('Data Formatting.')
    try:
        
        with open(sql_path, 'a',encoding='utf-8') as sql_file:
            for data in data_format_list:
                print(data)
                insert_query = (f"INSERT INTO {table_name} (Hotel_ID,Lat, Long,Hotel_Name, City, Date, Prices) "
                                f"VALUES {tuple(data)};\n")
                sql_file.write(insert_query)
        print(f'Data save in "{sql_path}" successfully...')

    except Exception as ex:
        print("An error occurred:", ex)


def get_hotel_calendar_info(hotel_count):
    data_format_list = []  # main list
    data_hotel=[]
   # sub list

    try:
        # Hotel name
        try:
            hotel_name = driver.find_element(By.CLASS_NAME, 'pp-header__title').text

        except:
            hotel_name = na

        # Hotel Id
        data_format_list.append(hotel_count)
        try:
            location=driver.find_element(By.ID,'hotel_address').get_attribute('data-atlas-latlng').split(',')
            latitude = float(location[0])
            longitude = float(location[1])
            data_format_list.append(latitude)
            data_format_list.append(longitude)
        except:
            data_format_list.append(0)
            data_format_list.append(0)
        # Hotel Name
        data_format_list.append(hotel_name)

        # Hotel City
        data_format_list.append(search_city)

        # Scroll to calendar view
        sleep(1)
        scroll_to_calendar_view = driver.find_element(By.XPATH, '//div[@data-testid="searchbox-dates-container"]')
        driver.execute_script("arguments[0].scrollIntoView();", scroll_to_calendar_view)
        scroll_to_calendar_view.click()

        # Calendar_view and next calendar button
        calendar_view = driver.find_element(By.XPATH, '//div[@data-testid="searchbox-datepicker-calendar"]')
        # next_calendar_btn = calendar_view.find_elements(By.XPATH, '//button[@type="button"]')

        # get calendar value
        calender_value_ex = 1
        next_calendar_click = 1
        while True:
            
            try:
                # get Month-Year text and checked by language
                month_year_name = calendar_view.find_element(By.XPATH, '//h3[@aria-live="polite"]').text
                checked_month_year_name = check_month_year_name(month_year_name)

                # Calendar date and price
                calendar_date_price_cels = driver.execute_script('''return arguments[0].querySelector('[role="grid"]')
                                    .querySelectorAll('[role="gridcell"]');''', calendar_view)
                for i, cel in enumerate(calendar_date_price_cels):

                    calendar_days_prices = driver.execute_script(
                        '''return arguments[0].querySelector('[role="checkbox"]').childNodes;''', cel)

                    date_price_list = []
                    try:
                        date = calendar_days_prices[0].text
                        price_rate = calendar_days_prices[-1].text
                        # -*- coding: utf-8 -*-
                        if price_rate == '':
                            price_rate = na
                        elif price_rate == '—':
                            price_rate = '--'
                    except:
                        date = str(i + 1)
                        price_rate = na

                    try:
                        date_format = date + ' ' + checked_month_year_name
                        parsed_date = datetime.strptime(date_format, '%d %B %Y')
                        formatted_date = parsed_date.strftime('%d-%m-%Y')
                        
                        date_price_list.append(formatted_date)
                        date_price_list.append(price_rate)
                        
                        df_list = data_format_list + date_price_list
                        
                        print(df_list)
                  
                        if len(df_list) == 7:
                            data_hotel.append(df_list)
                        else:
                            continue

                    except Exception as ex:
                        print(ex)
                        data_hotel.append('%d-%m-%Y')

            except Exception as ex:
                print('Error ->>', ex)
                calender_value_ex += 1
                if calender_value_ex < 2:
                    continue

            next_calendar_btn = driver.execute_script(
                '''return arguments[0].querySelectorAll('[type="button"]');''', calendar_view)
            next_calendar_btn[-1].click()
            next_calendar_click += 1

            if next_calendar_click > 12:
                break

    except Exception as ex:
        print('Error ->>', ex)

    finally:
        return data_hotel


def main():
    page_counter = 1
    hotel_counter = 1
    # skip_it = 0
    try:
        driver.get(base_url)
        # search_city
        print('Searching...')
        city_search_action()
        OtherPage=False
        while True:
            i=0
            # hotels = driver.find_elements(By.XPATH, '//div[@data-testid="property-card"]')
            # print(len(hotels))
            NextPage=False
            while True:
                hotels = driver.find_elements(By.XPATH, '//div[@data-testid="property-card"]')
                
                i+=1
                if i>=len(hotels):
                    NextPage=True
                    break
                # driver.execute_script("arguments[0].scrollIntoView();",hotels[i] )
                hotels =driver.find_elements(By.XPATH, '//div[@data-testid="property-card"]')
                hotel=hotels[i]
                print(len(hotels))
                hotel_title = hotel.find_element(By.TAG_NAME, 'h3').text.split('\n')[0]
                hotel_link = hotel.find_element(By.TAG_NAME, 'a').get_attribute('href')
                print('#######################################################################hotel_link')
                print(hotel_link)
                print(f'\n[{page_counter}:{hotel_counter}] ->> {hotel_title}\n{hotel_link}\n')
                driver.execute_script("window.open(arguments[0], '_blank');", hotel_link)
                driver.switch_to.window(driver.window_handles[1])
                sleep(1)
                    # get calender info
                calendar_info = get_hotel_calendar_info(hotel_counter)
                    # file formatting
                file_format(calendar_info)
                    # Close hotel link
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

                hotel_counter += 1
            try:
                if NextPage:
                    print('######################################Next Page ######################################')
                    buttonitems=driver.find_elements(By.CSS_SELECTOR,'.a83ed08757.c21c56c305.f38b6daa18.d691166b09.ab98298258.deab83296e.bb803d8689.a16ddf9c57')
                    if len(buttonitems)==1 and OtherPage==False:
                        buttonitems[0].click()
                        OtherPage=True
                    else:
                        buttonitems[1].click()
            except:
                quit()
    except KeyboardInterrupt:
        print('Program closed by forced...')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # global variable
    search_city = input('Enter what you want to search for: ').upper()
    print(f'You are searching for: "{search_city}"')

    columns = ["Hotel_ID", "Hotel_Name", "City", "Date", "Prices"]
    na = 'N/A'
    driver_refresh = 0

    sql_name = f'{search_city}.sql'
    table_name = f'HotelPricing{search_city}'
    sql_path = create_path()

    base_url = 'https://www.booking.com'

    # driver
    print('Chrome-Driver opening...')
    driver = get_driver()
    driver.implicitly_wait(15)
    wait = WebDriverWait(driver, 15)
    main()
