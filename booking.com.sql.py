import os
import sys
from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.service import Service
sys.stdout.reconfigure(encoding='utf-8')

# -*- coding: utf-8 -*-
def create_path():
    try:
        path = os.path.join('CITY', search_city)
        os.makedirs(path, exist_ok=True)

        path = f'{path}\\{sql_name}'

        create_table_sql = f'''CREATE TABLE Pricing_data (
            Hotel_ID INT NOT NULL, 
            Hotel_Name TEXT NOT NULL, 
            City TEXT NOT NULL, 
            Date TEXT NOT NULL, 
            Prices TEXT,
            );
            
            CREATE TABLE Hotel_Info(
            Hotel_ID INTEGER NOT NULL,
            Name VARCHAR(255) ,
            City TEXT,
            Address TEXT, 
            Type TEXT,      
            Images TEXT,                        
            Latitude FLOAT,
            Longitude FLOAT ,
            Stars TEXT,                        
            Sustainable TEXT,
            Restaurants TEXT,
            Restaurants_More_details TEXT,              
            Point_Fort TEXT,
            Comment_Rating TEXT,
            PRIMARY KEY (Hotel_ID),
            
            );
            CREATE TABLE Equipement_Hotel(
            id INTEGER NOT NULL,
            PRIMARY KEY (Id),
            Type TEXT,
            Details TEXT,
            Hotel_ID INT NOT NULL,
            FOREIGN KEY (Hotel_ID) REFERENCES Hotel_Info(Hotel_ID)
            );
            CREATE TABLE Environs_Hotel(
            id INTEGER NOT NULL,
            PRIMARY KEY (Id),
            Type TEXT,
            Details TEXT,
            Hotel_ID INT NOT NULL,
            FOREIGN KEY (Hotel_ID) REFERENCES Hotel_Info(Hotel_ID)
            );
            CREATE TABLE Comments_Client(
            id INTEGER NOT NULL,
            PRIMARY KEY (Id),
            Categorie TEXT,
            Note TEXT,
            Hotel_ID INT NOT NULL,
            FOREIGN KEY (Hotel_ID) REFERENCES Hotel_Info(Hotel_ID)
            );
            
            '''
        if not os.path.exists(path):
            with open(path, 'w') as sql:
                sql.write(create_table_sql + '\n')
            print(f'"{path}" created...')
        else:
            print(f'"{path}"already exist...')

        return path

    except Exception as ex:
        print("Error ->>", ex)


def get_driver(headless=False):
    chrome_driver_path = 'C:\\chromedriver.exe'
    # agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/116.0.1216.0 Safari/537.2'
    agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    # s = Service(executable_path=ChromeDriverManager().install())
    # s = Service(executable_path='chromedriver.exe')
    options = webdriver.FirefoxOptions()
    
    if headless:
        options.add_argument('--headless')
        options.add_argument(f'user-agent={agent}')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    web_driver =webdriver.Firefox(options=options)
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
        sleep(5)
        search_bar.send_keys(search_city)
        
        driver.execute_script('''return document.querySelector('[data-testid="autocomplete-result"]').click();''')
        driver.execute_script('''return document.querySelector('[type="submit"]').click();''')
        return True

    except:
        print('Unable to search city...')
        
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


def file_format(data_format):
    print('Data Formatting.')

    try:
        data_format_list=data_format[0]
        details_hotel=data_format[1]
        environs_hotel=data_format[2]
        equipement_hotel=data_format[3]
        comments_categorie=data_format[4]
        print('###############data price #################""')
        with open(sql_path, 'a',encoding='utf-8') as sql_file:
            print(sql_path)
            insert_query=("INSERT INTO Hotel_Info(Hotel_ID, Name,City, Address,Type ,Images, Latitude, Longitude, Stars, Sustainable,Restaurants ,Restaurants_More_details ,Point_Fort, Comment_Rating)"
                              f"VALUES {tuple(details_hotel)};\n")
            sql_file.write(insert_query)
            for item in environs_hotel:
                insert_query=('INSERT INTO  Environs_Hotel (id,Type, Details, Hotel_ID)'
                              f"VALUES{tuple(item)};\n")
                sql_file.write(insert_query)
            for item in equipement_hotel:
                insert_query=('INSERT INTO Equipement_Hotel(id,Type,Details,Hotel_ID)'
                              f"VALUES{tuple(item)};\n")
                sql_file.write(insert_query)
            for item in comments_categorie:
                insert_query=('INSERT INTO Comments_Client(id,Categorie, Note, Hotel_ID)'
                              f'VALUES{tuple(item)};\n')
                sql_file.write(insert_query)
            for data in data_format_list:
                insert_query = (f"INSERT INTO Pricing_data (Hotel_ID, Hotel_Name, City, Date, Prices)"
                                f"VALUES {tuple(data)};\n")
                sql_file.write(insert_query)
        print(f'Data save in "{sql_path}" successfully...')

    except Exception as ex:
        print("An error occurred:", ex)


def get_hotel_calendar_info(hotel_count,id_environ,id_equipement,id_comment):
    data_format_list = []  # main list
    hotel_info_data = []  # sub list
    data_Environs=[]
    equipementList=[]
    cat_infoFinal=[]
    id_environ_hotel=id_environ
    id_equipement_hotel=id_equipement
    id_comment_hotel=id_comment
    hotel_details=[]
    try:
        # Hotel name
        try:
            hotel_name = driver.find_element(By.CLASS_NAME, 'pp-header__title').text
        except:
            hotel_name = na
        
        # Hotel Idc
        hotel_info_data.append(hotel_count)

        # Hotel Name
        hotel_info_data.append(hotel_name)

        # Hotel City
        hotel_info_data.append(search_city)
        ####################################Details
        hotel_details.append(hotel_count)
        hotel_details.append(hotel_name)
        hotel_details.append(search_city)
        Address='None'
        try:
            Address=driver.find_element(By.CSS_SELECTOR,'.hp_address_subtitle.js-hp_address_subtitle.jq_tooltip').text
        except:
            pass
        hotel_details.append(Address)
        
        typeOfHotel='autre'
        if(hotel_name.lower().find('hotel')!=-1):
            typeOfHotel='hotel'
        elif(hotel_name.lower().find('riad')!=-1):
            typeOfHotel='riad'
        elif(hotel_name.lower().find('palais')!=-1):
            typeOfHotel='palais'
        elif(hotel_name.lower().find('house')!=-1 or hotel_name.lower().find('maison')!=-1 or hotel_name.lower().find('der')!=-1 or hotel_name.lower().find('dar')!=-1  ):
            typeOfHotel='house'
        elif(hotel_name.lower().find('résidence')!=-1 or hotel_name.lower().find('residence')!=-1):
            typeOfHotel='residence'
        elif(hotel_name.lower().find('appartement')!=-1 or hotel_name.lower().find('appartements')!=-1):
            typeOfHotel='appartement'
        elif(hotel_name.lower().find('ferme')!=-1 ):
            typeOfHotel='ferme'
        elif(hotel_name.lower().find('villa')!=-1 ):
            typeOfHotel='villa'
        elif(hotel_name.lower().find('auberge')!=-1):
            typeOfHotel='auberge'
        elif(hotel_name.lower().find('chalet')!=-1):
            typeOfHotel='chalet'
        elif(hotel_name.lower().find('bed')!=-1 or hotel_name.lower().find('lit')!=-1):
            typeOfHotel='bed'
        elif(hotel_name.lower().find('hostel')!=-1):
            typeOfHotel='hostel'
        else:
            typeOfHotel='autre'
        hotel_details.append(typeOfHotel)
        
        # Scroll to calendar view

        allImagesDb='None'
        try:
            Images1=driver.find_elements(By.CSS_SELECTOR,'.bh-photo-grid-item.bh-photo-grid-side-photo.active-image')
        ##### All images
            allImages=[]
            for img in Images1:
                urlimg=img.get_attribute('data-thumb-url')
                print('image 1: '+urlimg)
                allImages.append(urlimg)
            Images2=driver.find_element(By.CSS_SELECTOR,'.bh-photo-grid-item.bh-photo-grid-photo1.active-image').get_attribute('data-thumb-url')
            print('image 2: '+Images2)
            allImages.append(Images2)
            Images3=driver.find_elements(By.CSS_SELECTOR,'.bh-photo-grid-item.bh-photo-grid-thumb')
            for item in Images3[:-1]:
                imag = item.find_element(By.CSS_SELECTOR, '.hide')
                if imag:
                    path = imag.get_attribute('src')
                    print('image path: ' + path)
                    allImages.append(path)
                
            allImagesDb=' | '.join(allImages)
        except:
            pass   
        ###############add Images
        hotel_details.append(allImagesDb)
        try:
            location=driver.find_element(By.ID,'hotel_address').get_attribute('data-atlas-latlng').split(',')
            latitude = float(location[0])
            longitude = float(location[1])
            hotel_details.append(latitude)
            hotel_details.append(longitude)
        except:
            hotel_details.append(0)
            hotel_details.append(0)
            
        print('++++++++++++++++++++++Stars+++++++++++++++++++++++++')
        #Adress  
        stars=0
        try:
            containerStar=driver.find_element(By.CSS_SELECTOR,'.a455730030.d542f184f1')
            typeStar=containerStar.get_attribute('data-testid')
            if typeStar=='rating-squares':
                print('rating-squares')
                squareElement=containerStar.find_elements(By.CSS_SELECTOR,'.fcd9eec8fb.d31eda6efc.c25361c37f')
                stars=f"square:{len(squareElement)}"
            elif typeStar=='rating-stars':
                print('rating-stars')
                starsElement=containerStar.find_elements(By.CSS_SELECTOR,'.fcd9eec8fb.d31eda6efc.c25361c37f')
                stars=len(starsElement)
        except:
            pass
        print(stars)
        hotel_details.append(stars)
        sustainable='None'
        try:
            sustainableContainer=driver.find_elements(By.CSS_SELECTOR,'.fe89d69493')
            if sustainableContainer:
                temp=sustainableContainer.find_element(By.CSS_SELECTOR,'.abf093bdfe.d068504c75.f68ecd98ea')
                sustainable=temp.text
        except:
            pass
        hotel_details.append(sustainable)
        print(sustainable)
        
        restaurants='None'
        restaurant_Details='None'
        try:
            if driver.find_elements(By.CSS_SELECTOR,'.bcdcb105b3.f45d8e4c32.df64fda51b')!=0:
                restaurants=driver.find_element(By.CSS_SELECTOR,'.bcdcb105b3.f45d8e4c32.df64fda51b').text
                print('restau Name: '+restaurants)
                if restaurants.find('restaurants')!=-1 or restaurants.find('restaurant')!=-1:
                    
                    restau_ul=driver.find_element(By.CSS_SELECTOR,'.c807d72881.c843d0df03.e10711a42e')
                    restau_li=restau_ul.find_elements(By.CSS_SELECTOR,'.a8b57ad3ff.d50c412d31.fb9a5438f9.eaa02c469d.c7a5a1307a')
                    restaurant_list = []
                    
                    if len(driver.find_elements(By.CSS_SELECTOR,'.c807d72881.c843d0df03.e10711a42e'))!=0:
                        for item  in restau_li:
                            bigTitle=item.find_element(By.CSS_SELECTOR,'.a3332d346a').text
                            details= item.find_element(By.CSS_SELECTOR,'.a53cbfa6de.f45d8e4c32').text
                            restaurant_list.append(f'{bigTitle}({details})')
                        restaurant_Details=','.join(restaurant_list)
                        print(restaurant_Details)
                else:
                    restaurants='None'  
                    restaurant_Details='None'  
        except:
            pass
        hotel_details.append(restaurants)
        hotel_details.append(restaurant_Details)
        # Calendar_view and next calendar button
       
        # next_calendar_btn = calendar_view.find_elements(By.XPATH, '//button[@type="button"]')
        
        try:
            Cat_Name=driver.find_elements(By.CSS_SELECTOR,'.be887614c2')
            Cat_Rate=driver.find_elements(By.CSS_SELECTOR,'.ccb65902b2.efcd70b4c4')
            cat_info=[]
            for cat_name, cat_rate in zip( Cat_Name, Cat_Rate):
                cat_name_text = cat_name.text.strip()
                cat_rate_text = cat_rate.text.strip()
                cat_info.append([id_comment_hotel,cat_name_text,cat_rate_text,hotel_count])
                id_comment_hotel+=1
            cat_infoFinal=[item for item in cat_info if all(subitem != '' for subitem in item)]
        except:
            pass
        print(cat_infoFinal)
        ###### restautrant

      
        calender_value_ex = 1
        next_calendar_click = 1
       
        
        ##### sustainable
        
        
        pointfortDB='None'
        try:
            PoinFortS=driver.find_elements(By.CSS_SELECTOR,'.c807d72881.d1a624a1cc.e10711a42e')
            PoinFort=PoinFortS[0]
            poinfortList=[]
            PoinFortLi=PoinFort.find_elements(By.CSS_SELECTOR,'.a8b57ad3ff.d50c412d31.fb9a5438f9.c7a5a1307a')
            for test in PoinFortLi:
                temp=test.find_element(By.CSS_SELECTOR,'.a5a5a75131')
                print('point fort: '+ temp.text)
                poinfortList.append(temp.text)
            pointfortDB=','.join(poinfortList)
        except:
            pass
        #########################add point fort
        hotel_details.append(pointfortDB)
        
        
        try:
            equipements=driver.find_element(By.CSS_SELECTOR,'.e50d7535fa')
            equipementDetails=equipements.find_elements(By.CSS_SELECTOR,'.f1e6195c8b')
            for equi in equipementDetails:
                title=equi.find_element(By.CSS_SELECTOR,'.d1ca9115fe')
                print('-----------------------------------Title : '+title.text+'---------------------')
                list_item=[]
                if title.text=='Internet':
                    try:

                        print('text: ')
                        test=equi.find_element(By.CSS_SELECTOR,'.a53cbfa6de.f45d8e4c32.df64fda51b')
                        print(test.text)
                        list_item.append(test.text)
                    except:
                        pass
                elif title.text=='Parking':
                    try:

                        print('text: ')
                        test=equi.find_element(By.CSS_SELECTOR,'.a53cbfa6de.f45d8e4c32.df64fda51b')
                        print(test.text)
                        list_item.append(test.text)
                    except:
                        pass
                elif title.text=='Animaux domestiques':
                    try:
                        print('text: ')
                        test=equi.find_element(By.CSS_SELECTOR,'.a53cbfa6de.f45d8e4c32.df64fda51b')
                        print(test.text)
                        list_item.append(test.text)
                    except:
                        pass
                else :
                    try:
                        ul=equi.find_element(By.CSS_SELECTOR,'.c807d72881.da08adf9d2.e10711a42e')
                        lis=ul.find_elements(By.CSS_SELECTOR,'.a8b57ad3ff.d50c412d31.fb9a5438f9.c7a5a1307a')
                        for item in lis:
                            content=item.find_element(By.CSS_SELECTOR,'.a5a5a75131')
                            print('li: '+content.text)
                            list_item.append(content.text)
                    except:
                        pass
                equipementList.append([id_equipement_hotel,title.text,','.join(list_item),hotel_count])
                id_equipement_hotel+=1
        except:
            pass
        # for tpe in equipements:
        #     typeLo=tpe.find_element(By.CSS_SELECTOR,'#room_type_id_30985508')
        #     test=typeLo.find_element(By.CSS_SELECTOR,'.hprt-roomtype-icon-link').text
        #     print('type de logement: '+test)
        
        # tpeLog= driver.find_element(By.CSS_SELECTOR,'.hprt-table.hprt-table-long-language')
        # print('type logement : '+len(tpeLog ))
        
        try:
            environs=driver.find_element(By.CSS_SELECTOR,'.f1bc79b259')
            environsDiv=environs.find_elements(By.CSS_SELECTOR,'.d31796cb42')
            data_list=[]
            
            for env in environsDiv:
                div=env.find_element(By.CSS_SELECTOR,'.c38a8359ed')
                ul=env.find_element(By.CSS_SELECTOR,'.c807d72881.c3b290dbba.be7182ad14.e10711a42e')
                title=div.find_element(By.CSS_SELECTOR,'.e1eebb6a1e.e6208ee469.d0caee4251').text
                li=ul.find_elements(By.CSS_SELECTOR,'.a8b57ad3ff.d50c412d31.fb9a5438f9.c7a5a1307a')
                print('################'+title+'#################')
                print(len(li))
                listDetail=[]
                for item in li:
                    text=item.find_element(By.CSS_SELECTOR,'.aaee4e7cd3.e7a57abb1e.fb60b9836d').text
                    metrage=item.find_element(By.CSS_SELECTOR,'.a53cbfa6de.f45d8e4c32').text
                    print('text : '+text+'     Metrage: '+metrage)
                    listDetail.append(text)
                listString=','.join(listDetail)
                data_list.append([id_environ_hotel,title,listString,hotel_count])
                id_environ_hotel+=1
            data_Environs=data_list
        except:
            pass
        
        Note='None'
        try:
            Note=driver.find_element(By.CSS_SELECTOR,'.a3b8729ab1.d86cee9b25').text
            print(Note)
        except:
            pass
        #####################add Comment_Rating #############################
        hotel_details.append(Note)
        # while True:
        #     try:
        #         scroll_to_calendar_view = driver.find_element(By.XPATH, '//div[@data-testid="searchbox-dates-container"]')
        #         driver.execute_script("arguments[0].scrollIntoView();", scroll_to_calendar_view)
        #         scroll_to_calendar_view.click()
        #         calendar_view = driver.find_element(By.XPATH, '//div[@data-testid="searchbox-datepicker-calendar"]')
        #         try:
        #             sleep(1)
        #             # get Month-Year text and checked by language
        #             month_year_name = calendar_view.find_element(By.XPATH, '//h3[@aria-live="polite"]').text
        #             checked_month_year_name = check_month_year_name(month_year_name)

        #             # Calendar date and price
        #             calendar_date_price_cels = driver.execute_script('''return arguments[0].querySelector('[role="grid"]')
        #                                 .querySelectorAll('[role="gridcell"]');''', calendar_view)
        #             for i, cel in enumerate(calendar_date_price_cels):

        #                 calendar_days_prices = driver.execute_script(
        #                     '''return arguments[0].querySelector('[role="checkbox"]').childNodes;''', cel)

        #                 date_price_list = []
        #                 try:
        #                     date = calendar_days_prices[0].text
        #                     price_rate = calendar_days_prices[-1].text
        #                     # -*- coding: utf-8 -*-
        #                     if price_rate == '':
        #                         price_rate = na
        #                     elif price_rate == '—':
        #                         price_rate = '--'
        #                 except:
        #                     date = str(i + 1)
        #                     price_rate = na

        #                 try:
        #                     date_format = date + ' ' + checked_month_year_name
        #                     parsed_date = datetime.strptime(date_format, '%d %B %Y')
        #                     formatted_date = parsed_date.strftime('%d-%m-%Y')

        #                     date_price_list.append(formatted_date)
        #                     date_price_list.append(price_rate)

        #                     df_list = hotel_info_data + date_price_list
        #                     print(df_list)
        #                     if len(df_list) == 5:
        #                         data_format_list.append(df_list)
        #                     else:
        #                         continue

        #                 except Exception as ex:
        #                     print(ex)
        #                     data_format_list.append('%d-%m-%Y')

        #         except Exception as ex:
        #             print('Error ->>', ex)
        #             calender_value_ex += 1
        #             if calender_value_ex < 2:
        #                 continue

        #         next_calendar_btn = driver.execute_script(
        #             '''return arguments[0].querySelectorAll('[type="button"]');''', calendar_view)
        #         next_calendar_btn[-1].click()
        #         next_calendar_click += 1

        #         if next_calendar_click > 12:
        #             break
        #     except:
        #         pass
    except Exception as ex:
        print('Error ->>', ex)
    
    finally:
        return [data_format_list,hotel_details,data_Environs,equipementList,cat_infoFinal,id_environ_hotel,id_equipement_hotel,id_comment_hotel]


def main(sql_path):
    page_counter = 1
    hotel_counter = 1
    # skip_it = 0
    id_environ_hotel=1
    id_equipement_hotel=1
    id_comment_hotel=1
    cities=['agadir','fez','tangier','rabat','marrakech','casablanca']
    try:
        driver.get(base_url)
            # search_city
        print('Searching...')
        city_search_action()
            # get hotel links
        hotels = driver.find_elements(By.CSS_SELECTOR, '.c82435a4b8.a178069f51.a6ae3c2b40.a18aeea94d.d794b7a0f7.f53e278e95.c6710787a4')
        print('#################################################################################')
        print(len(hotels))
        sleep(3)
        
       
        while True:
            cmpt=1
            for index,hotel in enumerate(hotels):
                cmpt+=1
                print('hotel_title')
                # sleep(3)
                hh=driver.find_elements(By.CSS_SELECTOR,'.aab71f8e4e')
                driver.execute_script("arguments[0].scrollIntoView();", hh[index])
                print('hotel_title')
                
                h3 = hh[index]
                print(len(hh))
                hotel_title=h3.find_element(By.CSS_SELECTOR,'.f6431b446c.a15b38c233').text.split('\n')[0]
                
                hotel_link = h3.find_element(By.CSS_SELECTOR, '.a78ca197d0').get_attribute('href')
                print(f'\n[{page_counter}:{hotel_counter}] ->> {hotel_title}\n{hotel_link}\n')
                sleep(1)
                    # Open hotel link in new tab
                driver.execute_script("window.open(arguments[0], '_blank');", hotel_link)
                driver.switch_to.window(driver.window_handles[1])
                    # get calender info
                calendar_info = get_hotel_calendar_info(hotel_counter,id_environ_hotel,id_equipement_hotel,id_comment_hotel)
                id_environ_hotel=calendar_info[5]
                id_equipement_hotel=calendar_info[6]
                id_comment_hotel=calendar_info[7]
                    # file formatting
                file_format(calendar_info)
                    # Close hotel link
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

                hotel_counter += 1
                # ------------------------------<<pagination>>
            try:

                if cmpt>=len(hotels):
                    print('###################################### Next Page ######################################')
                
                    buttonitems=driver.find_elements(By.CSS_SELECTOR,'.a83ed08757.c21c56c305.f38b6daa18.d691166b09.ab98298258.deab83296e.bb803d8689.a16ddf9c57')
                    if len(buttonitems)==1:
                        buttonitems[0].click()
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

    columns = ["Hotel_ID", "Hotel_Name", "City","latitude","longitude", "Date", "Prices"]
    na = 'N/A'
    driver_refresh = 0

    sql_name = f'{search_city}.sql'
    table_name = f'HotelPricing{search_city}'
    sql_path = create_path()
    print('path sql'+sql_path)
    base_url = 'https://www.booking.com/index.fr.html'

    # driver
    print('Chrome-Driver opening...')
    driver = get_driver()
    driver.implicitly_wait(15)
    wait = WebDriverWait(driver, 15)
    main(sql_path)
