import os
import sys
from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.service import Service
import json
sys.stdout.reconfigure(encoding='utf-8')
# -*- coding: utf-8 -*-
def create_path():
    try:
        path = os.path.join('Successful_meetings', search_city)
        os.makedirs(path, exist_ok=True)

        path = f'{path}\\{sql_name}'

        create_table_sql = f'''CREATE TABLE Info_Hotels_details (
                Hotel_ID INT NOT NULL, 
                Hotel_Name TEXT, 
                Lat FLOAT,
                `Long` FLOAT,
                Address TEXT,
                Phone TEXT,
                Fax TEXT,
                Web TEXT,
                Email TEXT,
                COVID_19_Policies TEXT,
                Year_Built TEXT,
                Check_in_time TEXT,
                Check_out_Time TEXT,
                Number_of_Floors TEXT,
                Total_Number_of_Rooms TEXT,
                Chain TEXT,
                Chain_Website TEXT,
                Total_number_of_meeting_rooms TEXT,
                Total_event_space TEXT,
                Total_meeting_room_capacity TEXT,
                Meeting_Facilities TEXT,
                Guest_Services TEXT,
                Security TEXT,
                Amenities TEXT,
                PRIMARY KEY (Hotel_ID)
            );

            CREATE TABLE Meeting_Rooms (
                Id INTEGER PRIMARY KEY,
                Hotel_ID INT,
                Nom TEXT,
                Dimensions TEXT,
                Area TEXT,
                Floor_Number TEXT,
                Floor_Cover TEXT,
                Portable_Walls TEXT,
                Auditorium TEXT,
                Classroom TEXT,
                U_Shape TEXT,
                Reception TEXT,
                Banquet TEXT,
                FOREIGN KEY (Hotel_ID) REFERENCES Info_Hotels_details(Hotel_ID)
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
    agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0'
    # s = Service(executable_path=ChromeDriverManager().install())
    # s = Service(executable_path='chromedriver.exe')
    options = webdriver.EdgeOptions()
    options = webdriver.EdgeOptions()
    service=Service(executable_path='C:\msedgedriver.exe')
    if headless:
        options.add_argument('--headless')
        options.add_argument(f'user-agent={agent}')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    web_driver =webdriver.Edge(service=service, options=options)
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
        search_bar.send_keys(search_city)
        sleep(1)
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


def file_format(data_format):
    print('Data Formatting.')

    try:
        data_format_list=data_format[0]
        data=data_format[1]
        with open(sql_path, 'a') as sql_file:
            print(sql_path)
            insert_query = ("INSERT INTO Info_Hotels_details (Hotel_ID, Hotel_Name, Lat,`Long`,Address, Phone, Fax, Web, Email, COVID_19_Policies,Year_Built, Check_in_time, Check_out_Time, Number_of_Floors, Total_Number_of_Rooms,Chain, Chain_Website, Total_number_of_meeting_rooms, Total_event_space,Total_meeting_room_capacity, Meeting_Facilities, Guest_Services, Security, Amenities)"
                f"VALUES {tuple(data_format_list)};\n")
            sql_file.write(insert_query)
            for dt in data:
                insert_query=("INSERT INTO Meeting_Rooms (Id,Hotel_ID, Nom, Dimensions, Area, Floor_Number, Floor_Cover, Portable_Walls,Auditorium, Classroom, U_Shape, Reception, Banquet)"
               f"VALUES{tuple(dt)};\n")
                sql_file.write(insert_query)
        print(f'Data save in "{sql_path}" successfully...')
      
    except Exception as ex:
        print("An error occurred:", ex)


def get_hotel_info(hotel_count,meeting_rooms_count):  # main list
    hotel_info_data = []  # sub list
    service_security=[]
    MeetingsRoomTable=[]
    Ameneties='None'
    meeting_rooms_local=0
    Lat=0.0
    Long=0.0
    
    try:
        # Hotel name
        try:
            hotel_name = driver.find_element(By.CSS_SELECTOR, '.heading-2').text
            print(hotel_name)
        except:
            hotel_name = na
            print(hotel_name)
        hotel_info_data.append(hotel_count)
        hotel_info_data.append(hotel_name)
        Address='None'
        Phone='None'
        Fax='None'
        Web='None'
        Email='None'
        COVID_19_Policies='None'
        result_list = []
        try:
            #get Adress
            key_facts=driver.find_element(By.CSS_SELECTOR,'.venue-section.venue-section--facts')
            dls=key_facts.find_elements(By.CSS_SELECTOR,'dl')
            print('Len dls : ')
            print(len(dls))
            for index,item in enumerate(dls):
                if index==0:
                    dts=item.find_elements(By.CSS_SELECTOR,'dt')
                    dds=item.find_elements(By.CSS_SELECTOR,'dd')
                    for dt, dd in zip(dts, dds):
                        print('i am in dls')
                        dt_text_modified = dt.text.replace(' ', '_').replace('-', '_')
                        if dt_text_modified=='Address':
                            Address=dd.text
                        elif dt_text_modified=='Phone':
                            Phone=dd.text
                        elif dt_text_modified=='Fax':
                            Fax=dd.text
 
                        # Append [modified_dt, dd] to the result_list
                        result_list.append([dt_text_modified, dd.text])
                else:
                    dds=item.find_elements(By.CSS_SELECTOR,'dd')
                    dts=item.find_elements(By.CSS_SELECTOR,'dt')
                    for dt,dd in zip(dts,dds):
                        dt_modified=dt.text.replace(' ', '_').replace('-', '_')
                        if dt_modified=='Web':
                            Web=dd.text
                        elif dt_modified=='COVID_19_Policies:':
                            COVID_19_Policies=dd.text
                        elif dt_modified=='Email':
                            Email=dd.text
                        result_list.append([dt_modified,dd.text])

        except:
            pass
        try :
            locationContainer=driver.find_element(By.CSS_SELECTOR,'.venue-section.venue-section--location')
            scriptElement=locationContainer.find_element(By.XPATH,'//*[@id="map-init-pins"]').get_attribute('text')
            json_data = json.loads(scriptElement)
            marker_data = list(json_data['markers'].values())[0]
            print(marker_data)
            Lat = marker_data['latitude']
            Long = marker_data['longitude']
        except:
            pass 
        hotel_info_data.append(Lat)
        hotel_info_data.append(Long)
        hotel_info_data.append(Address)
        hotel_info_data.append(Phone)
        hotel_info_data.append(Fax)
        hotel_info_data.append(Web)
        hotel_info_data.append(Email)
        hotel_info_data.append(COVID_19_Policies)
        print('New data')
        print(result_list)
        OverviewGuestService=[]
        Year_Built='None'
        Check_in_time='None'
        Check_out_Time='None'
        Number_of_Floors='None'
        Total_Number_of_Rooms='None'
        Chain='None'
        Chain_Website='None'
        try:
            Overview_service=driver.find_element(By.CSS_SELECTOR,'.venue-section.venue-section--overview')

            dts=Overview_service.find_elements(By.CSS_SELECTOR,'dt')
            dds=Overview_service.find_elements(By.CSS_SELECTOR,'dd')
            for dt,dd in zip(dts,dds):
                dt_modified=dt.text.replace(' ', '_').replace('-', '_')
                if dt_modified=='Year_Built':
                    Year_Built=dd.text
                elif dt_modified=='Check_in_Time':
                    Check_in_time=dd.text
                elif dt_modified=='Check_out_Time':
                    Check_out_Time=dd.text
                elif dt_modified=='Number_of_Floors':
                    Number_of_Floors=dd.text
                elif dt_modified=='Total_Number_of_Rooms':
                    Total_Number_of_Rooms=dd.text
                elif dt_modified=='Chain':
                    Chain=dd.text
                elif dt_modified=='Chain_Website':
                    
                    Chain_Website=dd.text
                OverviewGuestService.append([dt_modified,dd.text])             
        except: 
            pass
        hotel_info_data.append(Year_Built)
        hotel_info_data.append(Check_in_time)
        hotel_info_data.append(Check_out_Time)
        hotel_info_data.append(Number_of_Floors)
        hotel_info_data.append(Total_Number_of_Rooms)
        hotel_info_data.append(Chain)
        hotel_info_data.append(Chain_Website)

        #####Guest Services
        
        
        try:
            guest_service_security=driver.find_element(By.CSS_SELECTOR,'.venue-section.venue-section--overview-list')
            dl=guest_service_security.find_elements(By.CSS_SELECTOR,'dl')
            ddTable=[]
            for item in dl:
                dt=item.find_element(By.CSS_SELECTOR,'dt')
                dd=item.find_elements(By.CSS_SELECTOR,'dd')
                for it in dd:
                    ddTable.append(it.text)
                service_security.append([dt.text,','.join(ddTable)])
        except:
            pass

            
        ######Event Space
        Total_number_of_meeting_rooms='None'
        Total_event_space='None'
        Total_meeting_room_capacity='None'
        Meeting_Facilities="None"
        try:
            Event_space=driver.find_element(By.CSS_SELECTOR,'.venue-section.venue-section--meeting-space')
            dls=Event_space.find_elements(By.CSS_SELECTOR,'dl')
            firstEvent=[]
            for index,item in enumerate(dls):
                if index==0:
                    dts=item.find_elements(By.CSS_SELECTOR,'dt')
                    dds=item.find_elements(By.CSS_SELECTOR,'dd')
                    for dt,dd in zip(dts,dds):
                        dt_modified=dt.text.replace(' ', '_').replace('-', '_')
                        if dt_modified=='Total_number_of_meeting_rooms': 
                            Total_number_of_meeting_rooms =dd.text
                        elif dt_modified=='Total_event_space':
                            Total_event_space=dd.text
                        elif dt_modified=='Total_meeting_room_capacity':
                            Total_meeting_room_capacity=dd.text    
                        firstEvent.append([dt_modified,dd.text])
                else:
                    d_list=[]
                    dts=item.find_element(By.CSS_SELECTOR,'dt')
                    dds=item.find_elements(By.CSS_SELECTOR,'dd') 
                    for d in dds:
                        d_list.append(d.text)
                    if dts.text.replace(' ', '_').replace('-', '_')=='Meeting_Facilities':
                        Meeting_Facilities=','.join(d_list)
                    firstEvent.append([dts.text.replace(' ', '_').replace('-', '_'),','.join(d_list)])  
        except:
            pass           
        ################ 

        hotel_info_data.append(Total_number_of_meeting_rooms)
        hotel_info_data.append(Total_event_space)
        hotel_info_data.append(Total_meeting_room_capacity)
        hotel_info_data.append(Meeting_Facilities)
        ########Amenities 
        dds_list=[]
        try:
            AmenetiesTag=driver.find_element(By.CSS_SELECTOR,'.venue-section.venue-section--amenities')
            dds=AmenetiesTag.find_elements(By.CSS_SELECTOR,'dd')
            for item in dds:
                dds_list.append(item.text)
            Ameneties=','.join(dds_list)
            print('Ameneties : '+Ameneties)
        except:
            pass
        
        
        try:
            table_Container=driver.find_element(By.CSS_SELECTOR,'.venue-section.venue-section--meeting-table')
            div=table_Container.find_element(By.CSS_SELECTOR,'.scroll-table--content')
            table=div.find_element(By.CSS_SELECTOR,'.table')
            thead=table.find_element(By.CSS_SELECTOR,'thead')
            tr=thead.find_element(By.CSS_SELECTOR,'tr') 
            th=tr.find_elements(By.CSS_SELECTOR,'th')
            tbody=table.find_element(By.CSS_SELECTOR,'tbody')
            tr=tbody.find_elements(By.CSS_SELECTOR,'tr')
            print('len of th:')
            print(len(th))
            for index,item in enumerate(th[1:]):
                
                MeetingsRoom=[]
                MeetingsRoom.append(meeting_rooms_count)
                meeting_rooms_count+=1
                meeting_rooms_local+=1
                MeetingsRoom.append(hotel_count)
                name=item.text
                print('the name of Room :')
                print(name)
                print(index)
                MeetingsRoom.append(name)
                for it in  tr:
                    td=it.find_elements(By.CSS_SELECTOR,'td')
                    td_text = td[index+1].text
                    if not td_text:
                        td_text = 'none'
                    MeetingsRoom.append(td_text)
                MeetingsRoomTable.append(MeetingsRoom)  
        except:
            pass

    except Exception as ex:
        print('Error ->>', ex)
    
    finally:
        Guest_Services='None'
        security='None'

        for item in service_security:
            if item[0]=='Guest Services':
                Guest_Services=item[1]
            elif item[0]=='Security':
                security=item[1]
        hotel_info_data.append(Guest_Services)
        hotel_info_data.append(security)
        hotel_info_data.append(Ameneties)
        print('last data')
        print(hotel_info_data)                    
        return [hotel_info_data,MeetingsRoomTable,meeting_rooms_local]


def main():
    
    page_counter = 1
    hotel_counter = 1
    meeting_rooms_count=1
    # skip_it = 0
    rabat='https://www.successfulmeetings.com/Meeting-Event-Venues/Rabat-Morocco/Hotels?cls=0&rm=0&mspc=0&pg='
    casablanca='https://www.successfulmeetings.com/Meeting-Event-Venues/Casablanca-Morocco/Hotels?acg=1&rm=0&cls=0&mspc=0&ff=1&pg='
    agadir='https://www.successfulmeetings.com/Meeting-Event-Venues/Agadir-Morocco/Hotels?cls=0&rm=0&mspc=0&pg='
    marrakech='https://www.successfulmeetings.com/Meeting-Event-Venues/Marrakech-Morocco/Hotels?cls=0&rm=0&mspc=0&pg='
    Ville=[rabat,casablanca,agadir,marrakech]
    try:   
        while True:
            base_url=f'https://www.successfulmeetings.com/Meeting-Event-Venues/Marrakech-Morocco/Hotels?cls=0&rm=0&mspc=0&pg={page_counter}'
            driver.get(base_url)
            # search_city
            print('Searching...')
            # city_search_action()
            # get hotel links
            hotels = driver.find_elements(By.CSS_SELECTOR, '#resList > article')
            print(len(hotels))
            if len(hotels)==0:
                break
            cmpt=0
           
            #map-init-pins
            while True:
                for hotel in hotels:
                    cmpt+=1
                    driver.execute_script("arguments[0].scrollIntoView();", hotel)
                    globalElement = hotel.find_element(By.CSS_SELECTOR, '.venue-name')
                    hotel_link = globalElement.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    print('the first : '+driver.current_window_handle)
                    print(hotel_link)
                    print(f'\n[{hotel_counter}] ->> {hotel_link}\n')
                    # Open hotel link in new tab
                    driver.execute_script("window.open(arguments[0], '_blank');", hotel_link)
                    driver.switch_to.window(driver.window_handles[1])
                    print('current : '+driver.current_url)
                    # get calender info
                    # calendar_info = get_hotel_calendar_info(hotel_counter)
                    data=get_hotel_info(hotel_counter,meeting_rooms_count)
                    # file formatting
                    file_format(data)
                    meeting_rooms_count+=data[2]
                    # Close hotel link
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

                    hotel_counter += 1
                if len(hotels)<=cmpt:
                    break
            page_counter += 1
            # ------------------------------<<pagination>>
            
            # try:
            #     next_page_button = driver.find_element(By.XPATH, '//button[@aria-label="Next page"]')
            #     if next_page_button.is_enabled():
            #         driver.execute_script("arguments[0].click();", next_page_button)
            #         page_counter += 1

            #         print("Next Page...")
            #         sleep(15)
            #         hotels = driver.find_elements(By.XPATH, '//div[@data-testid="property-card"]')
            #     else:
            #         print("End Page...")
            #         break
            # except:
            #     pass

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

    # driver
    print('Chrome-Driver opening...')
    driver = get_driver()
    driver.implicitly_wait(15)
    wait = WebDriverWait(driver, 15)
    main()
