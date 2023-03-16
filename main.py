import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
import time
import requests
import json
import math
import base64


def get_filters(id_category, city_from_message):
    desired_city = ''
    file_city_ids = open('city_id.json', 'r')
    city_ids = json.load(file_city_ids)
    for i in range(len(city_ids)):
        if city_ids[i]["cityNameRu"] == city_from_message:
            desired_city = city_ids[i]["cityId"]

    cookies = {
        'MVID_ACTOR_API_AVAILABILITY': 'true',
        'MVID_BLACK_FRIDAY_ENABLED': 'true',
        'MVID_CART_AVAILABILITY': 'true',
        'MVID_CATALOG_STATE': '1',
        'MVID_CITY_ID': f'\'{desired_city}\'',
        'MVID_COOKIE': '3500',
        'MVID_CREDIT_AVAILABILITY': 'true',
        'MVID_CRITICAL_GTM_INIT_DELAY': '3000',
        'MVID_FILTER_CODES': 'true',
        'MVID_FILTER_TOOLTIP': '1',
        'MVID_FLOCKTORY_ON': 'true',
        'MVID_GEOLOCATION_NEEDED': 'true',
        'MVID_GIFT_KIT': 'true',
        'MVID_GLC': 'true',
        'MVID_GLP': 'true',
        'MVID_GTM_ENABLED': '011',
        'MVID_IMG_RESIZE': 'true',
        'MVID_INTERVAL_DELIVERY': 'true',
        'MVID_IS_NEW_BR_WIDGET': 'true',
        'MVID_KLADR_ID': '7800000000000',
        'MVID_LAYOUT_TYPE': '1',
        'MVID_LP_SOLD_VARIANTS': '3',
        'MVID_MCLICK': 'true',
        'MVID_MCLICK_NEW': 'true',
        'MVID_MINDBOX_DYNAMICALLY': 'true',
        'MVID_MINI_PDP': 'true',
        'MVID_NEW_ACCESSORY': 'true',
        'MVID_NEW_LK_CHECK_CAPTCHA': 'true',
        'MVID_NEW_LK_OTP_TIMER': 'true',
        'MVID_NEW_MBONUS_BLOCK': 'true',
        'MVID_PROMO_CATALOG_ON': 'true',
        'MVID_REGION_ID': '6',
        'MVID_REGION_SHOP': 'S904',
        'MVID_SERVICES': '111',
        'MVID_TIMEZONE_OFFSET': '3',
        'MVID_TYP_CHAT': 'true',
        'MVID_WEB_SBP': 'true',
        'SENTRY_ERRORS_RATE': '0.1',
        'SENTRY_TRANSACTIONS_RATE': '0.5',
        '_gid': 'GA1.2.19773447.1676576416',
        '_ym_uid': '1676576416123405199',
        '_ym_d': '1676576416',
        '__SourceTracker': 'google__organic',
        'admitad_deduplication_cookie': 'google__organic',
        'gdeslon.ru.__arc_domain': 'gdeslon.ru',
        'gdeslon.ru.user_id': '1a77c54e-73db-4470-9d49-50397b073712',
        'tmr_lvid': '6827ac7662087918a8d764c23da85cf5',
        'tmr_lvidTS': '1676576419112',
        'advcake_track_id': '44e79641-8443-4501-9943-b3c7f70bc6ef',
        'advcake_session_id': '0e937b29-63d8-6556-0fb6-7db0c3c6af64',
        'flocktory-uuid': '8bc994f0-c843-4a81-bf80-bb7de5516145-5',
        'uxs_uid': 'bef59730-ae31-11ed-b314-6902a30f5395',
        'afUserId': 'd1866e7d-34f8-4cf9-9779-79ae544d1920-p',
        'adrcid': 'Aa8XqtNYpNCzn3KyYjYqNpw',
        'MVID_GUEST_ID': '22299143724',
        'MVID_VIEWED_PRODUCTS': '',
        'wurfl_device_id': 'generic_web_browser',
        'MVID_CALC_BONUS_RUBLES_PROFIT': 'true',
        'NEED_REQUIRE_APPLY_DISCOUNT': 'true',
        'MVID_CART_MULTI_DELETE': 'true',
        'PROMOLISTING_WITHOUT_STOCK_AB_TEST': '2',
        'MVID_GET_LOCATION_BY_DADATA': 'DaData',
        'PRESELECT_COURIER_DELIVERY_FOR_KBT': 'false',
        'HINTS_FIO_COOKIE_NAME': '1',
        'searchType2': '1',
        'COMPARISON_INDICATOR': 'false',
        'MVID_NEW_OLD': 'eyJjYXJ0IjpmYWxzZSwiZmF2b3JpdGUiOnRydWUsImNvbXBhcmlzb24iOnRydWV9',
        'MVID_OLD_NEW': 'eyJjb21wYXJpc29uIjogdHJ1ZSwgImZhdm9yaXRlIjogdHJ1ZSwgImNhcnQiOiB0cnVlfQ==',
        'deviceType': 'desktop',
        'flacktory': 'no',
        'BIGipServeratg-ps-prod_tcp80': '1929698314.20480.0000',
        'bIPs': '2118529862',
        'MVID_GTM_BROWSER_THEME': '1',
        'SMSError': '',
        'authError': '',
        'BIGipServeratg-ps-prod_tcp80_clone': '1929698314.20480.0000',
        'PHPSESSID': 'ds8cbt6opbtuurbl3t6mfe0e9p',
        'cookie_ip_add': '217.197.11.61',
        'JSESSIONID': '2GLxj2cWQXL0KmrwvhCFMr8yQnQrQYQ7vPZv2GtNW87pJLjk0qw8!655022204',
        'CACHE_INDICATOR': 'true',
        #'__zzatgib-w-mvideo': 'MDA0dC0cTApcfEJcdGswPi17CT4VHThHKHIzd2UrUgllIUkURmR9aXlAVlNGOVtiHSglRRIWOUp9DkYITic/bSNPGGk3OH9yY2kjRR49Cjx7GkFqIl9JWyFDWT56KyAYeGspUQoLXkBGX28beyJfKggkYzVfGUNqTg1pN1wUPHVlPkd0eio7ax9jS18nR1E/SF5dSRIyYhJAQE1HDTdAXjdXYTAPFhFNRxU9VlJPQyhrG3FYMA==Xw3cmA==',
        #'__zzatgib-w-mvideo': 'MDA0dC0cTApcfEJcdGswPi17CT4VHThHKHIzd2UrUgllIUkURmR9aXlAVlNGOVtiHSglRRIWOUp9DkYITic/bSNPGGk3OH9yY2kjRR49Cjx7GkFqIl9JWyFDWT56KyAYeGspUQoLXkBGX28beyJfKggkYzVfGUNqTg1pN1wUPHVlPkd0eio7ax9jS18nR1E/SF5dSRIyYhJAQE1HDTdAXjdXYTAPFhFNRxU9VlJPQyhrG3FYMA==Xw3cmA==',
        '__lhash_': '42d4609bde895c0f8ca5a027332cfb40',
        #'cfidsgib-w-mvideo': 'O6VA+/Gt8NRjKbsSBacwFjDmomFWvPckpeqxUWFxPV9l2yJtPvdeDIG8M8b5ZHhrLgIBCMoe+r60kYXY5PTqNBqoZjUdh5KeLpaXu/3VBZul6lxGnlGVasrXacZyy50dNqdQHI42VHdgsEr0R6jC90WNoK+4P3uJBKvkqw==',
        #'cfidsgib-w-mvideo': 'O6VA+/Gt8NRjKbsSBacwFjDmomFWvPckpeqxUWFxPV9l2yJtPvdeDIG8M8b5ZHhrLgIBCMoe+r60kYXY5PTqNBqoZjUdh5KeLpaXu/3VBZul6lxGnlGVasrXacZyy50dNqdQHI42VHdgsEr0R6jC90WNoK+4P3uJBKvkqw==',
        #'gsscgib-w-mvideo': '05TBa6F1YIHoEgGua3E3TpQBkETSL2BlmDwufUxVB4ErZlDGjttZWqr26/uY+A+8WrDmyjsSRfcWJUQXWXXcO27kxDdm+KdueZ4ggfIpZKc+C653J6IW7m6XNUXNqkFrsUB3YdqzbvcpiqvTWtnby9O9ltyT+OxgasRO565gCL/yajO1IONWtf4LzKRXN80BWKAErgXlDc34YAallrEsL5Ufs1BXwmUVe2NqlIo1LJikiGLoDgnoB7Z3nrdOdw==',
        #'gsscgib-w-mvideo': '05TBa6F1YIHoEgGua3E3TpQBkETSL2BlmDwufUxVB4ErZlDGjttZWqr26/uY+A+8WrDmyjsSRfcWJUQXWXXcO27kxDdm+KdueZ4ggfIpZKc+C653J6IW7m6XNUXNqkFrsUB3YdqzbvcpiqvTWtnby9O9ltyT+OxgasRO565gCL/yajO1IONWtf4LzKRXN80BWKAErgXlDc34YAallrEsL5Ufs1BXwmUVe2NqlIo1LJikiGLoDgnoB7Z3nrdOdw==',
        #'fgsscgib-w-mvideo': 'nMHG7560803e05e51d5a7135ad72e86920b356a5',
        #'fgsscgib-w-mvideo': 'nMHG7560803e05e51d5a7135ad72e86920b356a5',
        'cfidsgib-w-mvideo': 'P9RMHnV6ZraZVKbWzWckbu2bSe3HUgTKIwNJ9Wt/traWORRvoCok5Q20AhzF7UGs7tqehG0O//Gbjbu6b0idC2iJYwgvLlrSgMlX/rAs76GDhw0V+0uPWahIOlydd2+46aNvTub+/crPSto9i6X7Vv5TGRjfv9RtZvmcMA==',
        '_ym_isad': '2',
        'AF_SYNC': '1677185997805',
        #'__hash_': '3c7098d8b60667da90ee6293a1bb5355',
        '_sp_ses.d61c': '*',
        'mindboxDeviceUUID': '2777081e-2b5c-459c-b470-7c455e608a7c',
        'directCrm-session': '%7B%22deviceGuid%22%3A%222777081e-2b5c-459c-b470-7c455e608a7c%22%7D',
        '_ga': 'GA1.2.439832334.1676576415',
        'tmr_detect': '0%7C1677254281482',
        '_dc_gtm_UA-1873769-1': '1',
        '_dc_gtm_UA-1873769-37': '1',
        'MVID_ENVCLOUD': 'prod1',
        '_sp_id.d61c': '4b8037c8-e766-49a0-85d3-f6a2cf196b55.1676576416.27.1677254376.1677186937.1a86e98f-5b14-4631-a07b-65d00468e796.2b483b1d-5085-49b7-91c7-26f5841f01ef.a2836e7d-993d-4dd6-93af-589a5a38a3d4.1677253749041.31',
        '_ga_CFMZTSS5FM': 'GS1.1.1677253752.25.1.1677254378.0.0.0',
        '_ga_BNX5WPP3YK': 'GS1.1.1677253752.25.1.1677254378.55.0.0',
    }

    headers = {
        'authority': 'www.mvideo.ru',
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
        'baggage': 'sentry-transaction=%2F,sentry-public_key=1e9efdeb57cf4127af3f903ec9db1466,sentry-trace_id=86bbb9cf8cfc4e54979105653833a121,sentry-sample_rate=0.5',
        # 'cookie': 'MVID_ACTOR_API_AVAILABILITY=true; MVID_BLACK_FRIDAY_ENABLED=true; MVID_CART_AVAILABILITY=true; MVID_CATALOG_STATE=1; MVID_CITY_ID=CityCZ_1638; MVID_COOKIE=3500; MVID_CREDIT_AVAILABILITY=true; MVID_CRITICAL_GTM_INIT_DELAY=3000; MVID_FILTER_CODES=true; MVID_FILTER_TOOLTIP=1; MVID_FLOCKTORY_ON=true; MVID_GEOLOCATION_NEEDED=true; MVID_GIFT_KIT=true; MVID_GLC=true; MVID_GLP=true; MVID_GTM_ENABLED=011; MVID_IMG_RESIZE=true; MVID_INTERVAL_DELIVERY=true; MVID_IS_NEW_BR_WIDGET=true; MVID_KLADR_ID=7800000000000; MVID_LAYOUT_TYPE=1; MVID_LP_SOLD_VARIANTS=3; MVID_MCLICK=true; MVID_MCLICK_NEW=true; MVID_MINDBOX_DYNAMICALLY=true; MVID_MINI_PDP=true; MVID_NEW_ACCESSORY=true; MVID_NEW_LK_CHECK_CAPTCHA=true; MVID_NEW_LK_OTP_TIMER=true; MVID_NEW_MBONUS_BLOCK=true; MVID_PROMO_CATALOG_ON=true; MVID_REGION_ID=6; MVID_REGION_SHOP=S904; MVID_SERVICES=111; MVID_TIMEZONE_OFFSET=3; MVID_TYP_CHAT=true; MVID_WEB_SBP=true; SENTRY_ERRORS_RATE=0.1; SENTRY_TRANSACTIONS_RATE=0.5; _gid=GA1.2.19773447.1676576416; _ym_uid=1676576416123405199; _ym_d=1676576416; __SourceTracker=google__organic; admitad_deduplication_cookie=google__organic; gdeslon.ru.__arc_domain=gdeslon.ru; gdeslon.ru.user_id=1a77c54e-73db-4470-9d49-50397b073712; tmr_lvid=6827ac7662087918a8d764c23da85cf5; tmr_lvidTS=1676576419112; advcake_track_id=44e79641-8443-4501-9943-b3c7f70bc6ef; advcake_session_id=0e937b29-63d8-6556-0fb6-7db0c3c6af64; flocktory-uuid=8bc994f0-c843-4a81-bf80-bb7de5516145-5; uxs_uid=bef59730-ae31-11ed-b314-6902a30f5395; afUserId=d1866e7d-34f8-4cf9-9779-79ae544d1920-p; adrcid=Aa8XqtNYpNCzn3KyYjYqNpw; MVID_GUEST_ID=22299143724; MVID_VIEWED_PRODUCTS=; wurfl_device_id=generic_web_browser; MVID_CALC_BONUS_RUBLES_PROFIT=true; NEED_REQUIRE_APPLY_DISCOUNT=true; MVID_CART_MULTI_DELETE=true; PROMOLISTING_WITHOUT_STOCK_AB_TEST=2; MVID_GET_LOCATION_BY_DADATA=DaData; PRESELECT_COURIER_DELIVERY_FOR_KBT=false; HINTS_FIO_COOKIE_NAME=1; searchType2=1; COMPARISON_INDICATOR=false; MVID_NEW_OLD=eyJjYXJ0IjpmYWxzZSwiZmF2b3JpdGUiOnRydWUsImNvbXBhcmlzb24iOnRydWV9; MVID_OLD_NEW=eyJjb21wYXJpc29uIjogdHJ1ZSwgImZhdm9yaXRlIjogdHJ1ZSwgImNhcnQiOiB0cnVlfQ==; deviceType=desktop; flacktory=no; BIGipServeratg-ps-prod_tcp80=1929698314.20480.0000; bIPs=2118529862; MVID_GTM_BROWSER_THEME=1; SMSError=; authError=; BIGipServeratg-ps-prod_tcp80_clone=1929698314.20480.0000; PHPSESSID=ds8cbt6opbtuurbl3t6mfe0e9p; cookie_ip_add=217.197.11.61; JSESSIONID=2GLxj2cWQXL0KmrwvhCFMr8yQnQrQYQ7vPZv2GtNW87pJLjk0qw8!655022204; CACHE_INDICATOR=true; __zzatgib-w-mvideo=MDA0dC0cTApcfEJcdGswPi17CT4VHThHKHIzd2UrUgllIUkURmR9aXlAVlNGOVtiHSglRRIWOUp9DkYITic/bSNPGGk3OH9yY2kjRR49Cjx7GkFqIl9JWyFDWT56KyAYeGspUQoLXkBGX28beyJfKggkYzVfGUNqTg1pN1wUPHVlPkd0eio7ax9jS18nR1E/SF5dSRIyYhJAQE1HDTdAXjdXYTAPFhFNRxU9VlJPQyhrG3FYMA==Xw3cmA==; __zzatgib-w-mvideo=MDA0dC0cTApcfEJcdGswPi17CT4VHThHKHIzd2UrUgllIUkURmR9aXlAVlNGOVtiHSglRRIWOUp9DkYITic/bSNPGGk3OH9yY2kjRR49Cjx7GkFqIl9JWyFDWT56KyAYeGspUQoLXkBGX28beyJfKggkYzVfGUNqTg1pN1wUPHVlPkd0eio7ax9jS18nR1E/SF5dSRIyYhJAQE1HDTdAXjdXYTAPFhFNRxU9VlJPQyhrG3FYMA==Xw3cmA==; __lhash_=42d4609bde895c0f8ca5a027332cfb40; cfidsgib-w-mvideo=O6VA+/Gt8NRjKbsSBacwFjDmomFWvPckpeqxUWFxPV9l2yJtPvdeDIG8M8b5ZHhrLgIBCMoe+r60kYXY5PTqNBqoZjUdh5KeLpaXu/3VBZul6lxGnlGVasrXacZyy50dNqdQHI42VHdgsEr0R6jC90WNoK+4P3uJBKvkqw==; cfidsgib-w-mvideo=O6VA+/Gt8NRjKbsSBacwFjDmomFWvPckpeqxUWFxPV9l2yJtPvdeDIG8M8b5ZHhrLgIBCMoe+r60kYXY5PTqNBqoZjUdh5KeLpaXu/3VBZul6lxGnlGVasrXacZyy50dNqdQHI42VHdgsEr0R6jC90WNoK+4P3uJBKvkqw==; gsscgib-w-mvideo=05TBa6F1YIHoEgGua3E3TpQBkETSL2BlmDwufUxVB4ErZlDGjttZWqr26/uY+A+8WrDmyjsSRfcWJUQXWXXcO27kxDdm+KdueZ4ggfIpZKc+C653J6IW7m6XNUXNqkFrsUB3YdqzbvcpiqvTWtnby9O9ltyT+OxgasRO565gCL/yajO1IONWtf4LzKRXN80BWKAErgXlDc34YAallrEsL5Ufs1BXwmUVe2NqlIo1LJikiGLoDgnoB7Z3nrdOdw==; gsscgib-w-mvideo=05TBa6F1YIHoEgGua3E3TpQBkETSL2BlmDwufUxVB4ErZlDGjttZWqr26/uY+A+8WrDmyjsSRfcWJUQXWXXcO27kxDdm+KdueZ4ggfIpZKc+C653J6IW7m6XNUXNqkFrsUB3YdqzbvcpiqvTWtnby9O9ltyT+OxgasRO565gCL/yajO1IONWtf4LzKRXN80BWKAErgXlDc34YAallrEsL5Ufs1BXwmUVe2NqlIo1LJikiGLoDgnoB7Z3nrdOdw==; fgsscgib-w-mvideo=nMHG7560803e05e51d5a7135ad72e86920b356a5; fgsscgib-w-mvideo=nMHG7560803e05e51d5a7135ad72e86920b356a5; cfidsgib-w-mvideo=P9RMHnV6ZraZVKbWzWckbu2bSe3HUgTKIwNJ9Wt/traWORRvoCok5Q20AhzF7UGs7tqehG0O//Gbjbu6b0idC2iJYwgvLlrSgMlX/rAs76GDhw0V+0uPWahIOlydd2+46aNvTub+/crPSto9i6X7Vv5TGRjfv9RtZvmcMA==; _ym_isad=2; AF_SYNC=1677185997805; __hash_=3c7098d8b60667da90ee6293a1bb5355; _sp_ses.d61c=*; mindboxDeviceUUID=2777081e-2b5c-459c-b470-7c455e608a7c; directCrm-session=%7B%22deviceGuid%22%3A%222777081e-2b5c-459c-b470-7c455e608a7c%22%7D; _ga=GA1.2.439832334.1676576415; tmr_detect=0%7C1677254281482; _dc_gtm_UA-1873769-1=1; _dc_gtm_UA-1873769-37=1; MVID_ENVCLOUD=prod1; _sp_id.d61c=4b8037c8-e766-49a0-85d3-f6a2cf196b55.1676576416.27.1677254376.1677186937.1a86e98f-5b14-4631-a07b-65d00468e796.2b483b1d-5085-49b7-91c7-26f5841f01ef.a2836e7d-993d-4dd6-93af-589a5a38a3d4.1677253749041.31; _ga_CFMZTSS5FM=GS1.1.1677253752.25.1.1677254378.0.0.0; _ga_BNX5WPP3YK=GS1.1.1677253752.25.1.1677254378.55.0.0',
        'referer': 'https://www.mvideo.ru/noutbuki-planshety-komputery-8/noutbuki-118/f/tolko-v-nalichii=da',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sentry-trace': '86bbb9cf8cfc4e54979105653833a121-817af3222825c26b-1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'x-set-application-id': '8d494b7a-a94b-4166-b49e-eb738a7deb72',
    }

    params = {
        'categoryId': f'{id_category}',
        'offset': '0',
        'limit': '24',
        #'filterParams': 'WyJ0b2xrby12LW5hbGljaGlpIiwiIiwiZGEiXQ==',
        'doTranslit': 'true',
    }

    response = requests.get('https://www.mvideo.ru/bff/products/listing', params=params, cookies=cookies,
                            headers=headers).json()
    filters = response.get('body').get('filters')
    with open('filters.json', 'w') as file:
        json.dump(filters, file, indent=5, ensure_ascii=True)


def get_city_id():

    cookies = {
        'MVID_ACTOR_API_AVAILABILITY': 'true',
        'MVID_BLACK_FRIDAY_ENABLED': 'true',
        'MVID_CART_AVAILABILITY': 'true',
        'MVID_CATALOG_STATE': '1',
        'MVID_CITY_ID': 'CityCZ_1638',
        'MVID_COOKIE': '3500',
        'MVID_CREDIT_AVAILABILITY': 'true',
        'MVID_CRITICAL_GTM_INIT_DELAY': '3000',
        'MVID_FILTER_CODES': 'true',
        'MVID_FILTER_TOOLTIP': '1',
        'MVID_FLOCKTORY_ON': 'true',
        'MVID_GEOLOCATION_NEEDED': 'true',
        'MVID_GIFT_KIT': 'true',
        'MVID_GLC': 'true',
        'MVID_GLP': 'true',
        'MVID_GTM_ENABLED': '011',
        'MVID_IMG_RESIZE': 'true',
        'MVID_INTERVAL_DELIVERY': 'true',
        'MVID_IS_NEW_BR_WIDGET': 'true',
        'MVID_KLADR_ID': '7800000000000',
        'MVID_LAYOUT_TYPE': '1',
        'MVID_LP_SOLD_VARIANTS': '3',
        'MVID_MCLICK': 'true',
        'MVID_MCLICK_NEW': 'true',
        'MVID_MINDBOX_DYNAMICALLY': 'true',
        'MVID_MINI_PDP': 'true',
        'MVID_NEW_ACCESSORY': 'true',
        'MVID_NEW_LK_CHECK_CAPTCHA': 'true',
        'MVID_NEW_LK_OTP_TIMER': 'true',
        'MVID_NEW_MBONUS_BLOCK': 'true',
        'MVID_PROMO_CATALOG_ON': 'true',
        'MVID_REGION_ID': '6',
        'MVID_REGION_SHOP': 'S904',
        'MVID_SERVICES': '111',
        'MVID_TIMEZONE_OFFSET': '3',
        'MVID_TYP_CHAT': 'true',
        'MVID_WEB_SBP': 'true',
        'SENTRY_ERRORS_RATE': '0.1',
        'SENTRY_TRANSACTIONS_RATE': '0.5',
        '_gid': 'GA1.2.19773447.1676576416',
        '_ym_uid': '1676576416123405199',
        '_ym_d': '1676576416',
        '__SourceTracker': 'google__organic',
        'admitad_deduplication_cookie': 'google__organic',
        'gdeslon.ru.__arc_domain': 'gdeslon.ru',
        'gdeslon.ru.user_id': '1a77c54e-73db-4470-9d49-50397b073712',
        'tmr_lvid': '6827ac7662087918a8d764c23da85cf5',
        'tmr_lvidTS': '1676576419112',
        'advcake_track_id': '44e79641-8443-4501-9943-b3c7f70bc6ef',
        'advcake_session_id': '0e937b29-63d8-6556-0fb6-7db0c3c6af64',
        'flocktory-uuid': '8bc994f0-c843-4a81-bf80-bb7de5516145-5',
        'uxs_uid': 'bef59730-ae31-11ed-b314-6902a30f5395',
        'afUserId': 'd1866e7d-34f8-4cf9-9779-79ae544d1920-p',
        'adrcid': 'Aa8XqtNYpNCzn3KyYjYqNpw',
        'MVID_GUEST_ID': '22299143724',
        'MVID_VIEWED_PRODUCTS': '',
        'wurfl_device_id': 'generic_web_browser',
        'MVID_CALC_BONUS_RUBLES_PROFIT': 'true',
        'NEED_REQUIRE_APPLY_DISCOUNT': 'true',
        'MVID_CART_MULTI_DELETE': 'true',
        'PROMOLISTING_WITHOUT_STOCK_AB_TEST': '2',
        'MVID_GET_LOCATION_BY_DADATA': 'DaData',
        'PRESELECT_COURIER_DELIVERY_FOR_KBT': 'false',
        'HINTS_FIO_COOKIE_NAME': '1',
        'searchType2': '1',
        'COMPARISON_INDICATOR': 'false',
        'MVID_NEW_OLD': 'eyJjYXJ0IjpmYWxzZSwiZmF2b3JpdGUiOnRydWUsImNvbXBhcmlzb24iOnRydWV9',
        'MVID_OLD_NEW': 'eyJjb21wYXJpc29uIjogdHJ1ZSwgImZhdm9yaXRlIjogdHJ1ZSwgImNhcnQiOiB0cnVlfQ==',
        'deviceType': 'desktop',
        'flacktory': 'no',
        'BIGipServeratg-ps-prod_tcp80': '1929698314.20480.0000',
        'bIPs': '2118529862',
        'MVID_GTM_BROWSER_THEME': '1',
        'SMSError': '',
        'authError': '',
        'BIGipServeratg-ps-prod_tcp80_clone': '1929698314.20480.0000',
        'PHPSESSID': 'ds8cbt6opbtuurbl3t6mfe0e9p',
        'JSESSIONID': '2GLxj2cWQXL0KmrwvhCFMr8yQnQrQYQ7vPZv2GtNW87pJLjk0qw8!655022204',
        'CACHE_INDICATOR': 'true',
        #'__zzatgib-w-mvideo': 'MDA0dC0cTApcfEJcdGswPi17CT4VHThHKHIzd2UrUgllIUkURmR9aXlAVlNGOVtiHSglRRIWOUp9DkYITic/bSNPGGk3OH9yY2kjRR49Cjx7GkFqIl9JWyFDWT56KyAYeGspUQoLXkBGX28beyJfKggkYzVfGUNqTg1pN1wUPHVlPkd0eio7ax9jS18nR1E/SF5dSRIyYhJAQE1HDTdAXjdXYTAPFhFNRxU9VlJPQyhrG3FYMA==Xw3cmA==',
        #'__zzatgib-w-mvideo': 'MDA0dC0cTApcfEJcdGswPi17CT4VHThHKHIzd2UrUgllIUkURmR9aXlAVlNGOVtiHSglRRIWOUp9DkYITic/bSNPGGk3OH9yY2kjRR49Cjx7GkFqIl9JWyFDWT56KyAYeGspUQoLXkBGX28beyJfKggkYzVfGUNqTg1pN1wUPHVlPkd0eio7ax9jS18nR1E/SF5dSRIyYhJAQE1HDTdAXjdXYTAPFhFNRxU9VlJPQyhrG3FYMA==Xw3cmA==',
        '__lhash_': '42d4609bde895c0f8ca5a027332cfb40',
        #'cfidsgib-w-mvideo': 'O6VA+/Gt8NRjKbsSBacwFjDmomFWvPckpeqxUWFxPV9l2yJtPvdeDIG8M8b5ZHhrLgIBCMoe+r60kYXY5PTqNBqoZjUdh5KeLpaXu/3VBZul6lxGnlGVasrXacZyy50dNqdQHI42VHdgsEr0R6jC90WNoK+4P3uJBKvkqw==',
        #'cfidsgib-w-mvideo': 'O6VA+/Gt8NRjKbsSBacwFjDmomFWvPckpeqxUWFxPV9l2yJtPvdeDIG8M8b5ZHhrLgIBCMoe+r60kYXY5PTqNBqoZjUdh5KeLpaXu/3VBZul6lxGnlGVasrXacZyy50dNqdQHI42VHdgsEr0R6jC90WNoK+4P3uJBKvkqw==',
        #'gsscgib-w-mvideo': '05TBa6F1YIHoEgGua3E3TpQBkETSL2BlmDwufUxVB4ErZlDGjttZWqr26/uY+A+8WrDmyjsSRfcWJUQXWXXcO27kxDdm+KdueZ4ggfIpZKc+C653J6IW7m6XNUXNqkFrsUB3YdqzbvcpiqvTWtnby9O9ltyT+OxgasRO565gCL/yajO1IONWtf4LzKRXN80BWKAErgXlDc34YAallrEsL5Ufs1BXwmUVe2NqlIo1LJikiGLoDgnoB7Z3nrdOdw==',
        #'gsscgib-w-mvideo': '05TBa6F1YIHoEgGua3E3TpQBkETSL2BlmDwufUxVB4ErZlDGjttZWqr26/uY+A+8WrDmyjsSRfcWJUQXWXXcO27kxDdm+KdueZ4ggfIpZKc+C653J6IW7m6XNUXNqkFrsUB3YdqzbvcpiqvTWtnby9O9ltyT+OxgasRO565gCL/yajO1IONWtf4LzKRXN80BWKAErgXlDc34YAallrEsL5Ufs1BXwmUVe2NqlIo1LJikiGLoDgnoB7Z3nrdOdw==',
        #'fgsscgib-w-mvideo': 'nMHG7560803e05e51d5a7135ad72e86920b356a5',
        #'fgsscgib-w-mvideo': 'nMHG7560803e05e51d5a7135ad72e86920b356a5',
        #'cfidsgib-w-mvideo': 'P9RMHnV6ZraZVKbWzWckbu2bSe3HUgTKIwNJ9Wt/traWORRvoCok5Q20AhzF7UGs7tqehG0O//Gbjbu6b0idC2iJYwgvLlrSgMlX/rAs76GDhw0V+0uPWahIOlydd2+46aNvTub+/crPSto9i6X7Vv5TGRjfv9RtZvmcMA==',
        'AF_SYNC': '1677185997805',
        'mindboxDeviceUUID': '2777081e-2b5c-459c-b470-7c455e608a7c',
        'directCrm-session': '%7B%22deviceGuid%22%3A%222777081e-2b5c-459c-b470-7c455e608a7c%22%7D',
        '_sp_ses.d61c': '*',
        '_ym_isad': '2',
        'cookie_ip_add': '188.162.64.183',
        #'__hash_': 'bc6ad6dbfc51e5966c5f70465787322c',
        '_dc_gtm_UA-1873769-1': '1',
        '_ga': 'GA1.2.439832334.1676576415',
        '_dc_gtm_UA-1873769-37': '1',
        'MVID_ENVCLOUD': 'prod2',
        'tmr_detect': '0%7C1677279221080',
        '_sp_id.d61c': '4b8037c8-e766-49a0-85d3-f6a2cf196b55.1676576416.28.1677279225.1677254382.a4a21cc0-b399-4db0-9609-d93be3f4dcd3.1a86e98f-5b14-4631-a07b-65d00468e796.b09d276c-8f2f-4c06-bfa4-d4882df97cac.1677278538161.21',
        '_ga_CFMZTSS5FM': 'GS1.1.1677278538.26.1.1677279229.0.0.0',
        '_ga_BNX5WPP3YK': 'GS1.1.1677278538.26.1.1677279229.46.0.0',
    }

    headers = {
        'authority': 'www.mvideo.ru',
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
        'baggage': 'sentry-transaction=%2F,sentry-public_key=1e9efdeb57cf4127af3f903ec9db1466,sentry-trace_id=51cd122fa10e425099e78f9099a257f5,sentry-sample_rate=0.5',
        # 'cookie': 'MVID_ACTOR_API_AVAILABILITY=true; MVID_BLACK_FRIDAY_ENABLED=true; MVID_CART_AVAILABILITY=true; MVID_CATALOG_STATE=1; MVID_CITY_ID=CityCZ_1638; MVID_COOKIE=3500; MVID_CREDIT_AVAILABILITY=true; MVID_CRITICAL_GTM_INIT_DELAY=3000; MVID_FILTER_CODES=true; MVID_FILTER_TOOLTIP=1; MVID_FLOCKTORY_ON=true; MVID_GEOLOCATION_NEEDED=true; MVID_GIFT_KIT=true; MVID_GLC=true; MVID_GLP=true; MVID_GTM_ENABLED=011; MVID_IMG_RESIZE=true; MVID_INTERVAL_DELIVERY=true; MVID_IS_NEW_BR_WIDGET=true; MVID_KLADR_ID=7800000000000; MVID_LAYOUT_TYPE=1; MVID_LP_SOLD_VARIANTS=3; MVID_MCLICK=true; MVID_MCLICK_NEW=true; MVID_MINDBOX_DYNAMICALLY=true; MVID_MINI_PDP=true; MVID_NEW_ACCESSORY=true; MVID_NEW_LK_CHECK_CAPTCHA=true; MVID_NEW_LK_OTP_TIMER=true; MVID_NEW_MBONUS_BLOCK=true; MVID_PROMO_CATALOG_ON=true; MVID_REGION_ID=6; MVID_REGION_SHOP=S904; MVID_SERVICES=111; MVID_TIMEZONE_OFFSET=3; MVID_TYP_CHAT=true; MVID_WEB_SBP=true; SENTRY_ERRORS_RATE=0.1; SENTRY_TRANSACTIONS_RATE=0.5; _gid=GA1.2.19773447.1676576416; _ym_uid=1676576416123405199; _ym_d=1676576416; __SourceTracker=google__organic; admitad_deduplication_cookie=google__organic; gdeslon.ru.__arc_domain=gdeslon.ru; gdeslon.ru.user_id=1a77c54e-73db-4470-9d49-50397b073712; tmr_lvid=6827ac7662087918a8d764c23da85cf5; tmr_lvidTS=1676576419112; advcake_track_id=44e79641-8443-4501-9943-b3c7f70bc6ef; advcake_session_id=0e937b29-63d8-6556-0fb6-7db0c3c6af64; flocktory-uuid=8bc994f0-c843-4a81-bf80-bb7de5516145-5; uxs_uid=bef59730-ae31-11ed-b314-6902a30f5395; afUserId=d1866e7d-34f8-4cf9-9779-79ae544d1920-p; adrcid=Aa8XqtNYpNCzn3KyYjYqNpw; MVID_GUEST_ID=22299143724; MVID_VIEWED_PRODUCTS=; wurfl_device_id=generic_web_browser; MVID_CALC_BONUS_RUBLES_PROFIT=true; NEED_REQUIRE_APPLY_DISCOUNT=true; MVID_CART_MULTI_DELETE=true; PROMOLISTING_WITHOUT_STOCK_AB_TEST=2; MVID_GET_LOCATION_BY_DADATA=DaData; PRESELECT_COURIER_DELIVERY_FOR_KBT=false; HINTS_FIO_COOKIE_NAME=1; searchType2=1; COMPARISON_INDICATOR=false; MVID_NEW_OLD=eyJjYXJ0IjpmYWxzZSwiZmF2b3JpdGUiOnRydWUsImNvbXBhcmlzb24iOnRydWV9; MVID_OLD_NEW=eyJjb21wYXJpc29uIjogdHJ1ZSwgImZhdm9yaXRlIjogdHJ1ZSwgImNhcnQiOiB0cnVlfQ==; deviceType=desktop; flacktory=no; BIGipServeratg-ps-prod_tcp80=1929698314.20480.0000; bIPs=2118529862; MVID_GTM_BROWSER_THEME=1; SMSError=; authError=; BIGipServeratg-ps-prod_tcp80_clone=1929698314.20480.0000; PHPSESSID=ds8cbt6opbtuurbl3t6mfe0e9p; JSESSIONID=2GLxj2cWQXL0KmrwvhCFMr8yQnQrQYQ7vPZv2GtNW87pJLjk0qw8!655022204; CACHE_INDICATOR=true; __zzatgib-w-mvideo=MDA0dC0cTApcfEJcdGswPi17CT4VHThHKHIzd2UrUgllIUkURmR9aXlAVlNGOVtiHSglRRIWOUp9DkYITic/bSNPGGk3OH9yY2kjRR49Cjx7GkFqIl9JWyFDWT56KyAYeGspUQoLXkBGX28beyJfKggkYzVfGUNqTg1pN1wUPHVlPkd0eio7ax9jS18nR1E/SF5dSRIyYhJAQE1HDTdAXjdXYTAPFhFNRxU9VlJPQyhrG3FYMA==Xw3cmA==; __zzatgib-w-mvideo=MDA0dC0cTApcfEJcdGswPi17CT4VHThHKHIzd2UrUgllIUkURmR9aXlAVlNGOVtiHSglRRIWOUp9DkYITic/bSNPGGk3OH9yY2kjRR49Cjx7GkFqIl9JWyFDWT56KyAYeGspUQoLXkBGX28beyJfKggkYzVfGUNqTg1pN1wUPHVlPkd0eio7ax9jS18nR1E/SF5dSRIyYhJAQE1HDTdAXjdXYTAPFhFNRxU9VlJPQyhrG3FYMA==Xw3cmA==; __lhash_=42d4609bde895c0f8ca5a027332cfb40; cfidsgib-w-mvideo=O6VA+/Gt8NRjKbsSBacwFjDmomFWvPckpeqxUWFxPV9l2yJtPvdeDIG8M8b5ZHhrLgIBCMoe+r60kYXY5PTqNBqoZjUdh5KeLpaXu/3VBZul6lxGnlGVasrXacZyy50dNqdQHI42VHdgsEr0R6jC90WNoK+4P3uJBKvkqw==; cfidsgib-w-mvideo=O6VA+/Gt8NRjKbsSBacwFjDmomFWvPckpeqxUWFxPV9l2yJtPvdeDIG8M8b5ZHhrLgIBCMoe+r60kYXY5PTqNBqoZjUdh5KeLpaXu/3VBZul6lxGnlGVasrXacZyy50dNqdQHI42VHdgsEr0R6jC90WNoK+4P3uJBKvkqw==; gsscgib-w-mvideo=05TBa6F1YIHoEgGua3E3TpQBkETSL2BlmDwufUxVB4ErZlDGjttZWqr26/uY+A+8WrDmyjsSRfcWJUQXWXXcO27kxDdm+KdueZ4ggfIpZKc+C653J6IW7m6XNUXNqkFrsUB3YdqzbvcpiqvTWtnby9O9ltyT+OxgasRO565gCL/yajO1IONWtf4LzKRXN80BWKAErgXlDc34YAallrEsL5Ufs1BXwmUVe2NqlIo1LJikiGLoDgnoB7Z3nrdOdw==; gsscgib-w-mvideo=05TBa6F1YIHoEgGua3E3TpQBkETSL2BlmDwufUxVB4ErZlDGjttZWqr26/uY+A+8WrDmyjsSRfcWJUQXWXXcO27kxDdm+KdueZ4ggfIpZKc+C653J6IW7m6XNUXNqkFrsUB3YdqzbvcpiqvTWtnby9O9ltyT+OxgasRO565gCL/yajO1IONWtf4LzKRXN80BWKAErgXlDc34YAallrEsL5Ufs1BXwmUVe2NqlIo1LJikiGLoDgnoB7Z3nrdOdw==; fgsscgib-w-mvideo=nMHG7560803e05e51d5a7135ad72e86920b356a5; fgsscgib-w-mvideo=nMHG7560803e05e51d5a7135ad72e86920b356a5; cfidsgib-w-mvideo=P9RMHnV6ZraZVKbWzWckbu2bSe3HUgTKIwNJ9Wt/traWORRvoCok5Q20AhzF7UGs7tqehG0O//Gbjbu6b0idC2iJYwgvLlrSgMlX/rAs76GDhw0V+0uPWahIOlydd2+46aNvTub+/crPSto9i6X7Vv5TGRjfv9RtZvmcMA==; AF_SYNC=1677185997805; mindboxDeviceUUID=2777081e-2b5c-459c-b470-7c455e608a7c; directCrm-session=%7B%22deviceGuid%22%3A%222777081e-2b5c-459c-b470-7c455e608a7c%22%7D; _sp_ses.d61c=*; _ym_isad=2; cookie_ip_add=188.162.64.183; __hash_=bc6ad6dbfc51e5966c5f70465787322c; _dc_gtm_UA-1873769-1=1; _ga=GA1.2.439832334.1676576415; _dc_gtm_UA-1873769-37=1; MVID_ENVCLOUD=prod2; tmr_detect=0%7C1677279221080; _sp_id.d61c=4b8037c8-e766-49a0-85d3-f6a2cf196b55.1676576416.28.1677279225.1677254382.a4a21cc0-b399-4db0-9609-d93be3f4dcd3.1a86e98f-5b14-4631-a07b-65d00468e796.b09d276c-8f2f-4c06-bfa4-d4882df97cac.1677278538161.21; _ga_CFMZTSS5FM=GS1.1.1677278538.26.1.1677279229.0.0.0; _ga_BNX5WPP3YK=GS1.1.1677278538.26.1.1677279229.46.0.0',
        'referer': 'https://www.mvideo.ru/smartfony-i-svyaz-10/smartfony-205?reff=menu_main',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sentry-trace': '51cd122fa10e425099e78f9099a257f5-b3e512adff6832bc-0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'x-set-application-id': '6d324a09-dac9-4864-aad3-080233104d4a',
    }

    response = requests.get('https://www.mvideo.ru/bff/seo/plp/cities', cookies=cookies, headers=headers).json()
    city_id = response.get('body').get('cities').get('data')
    with open('city_id.json', 'w') as file:
        json.dump(city_id, file, indent=5, ensure_ascii=False)


def get_urls():
    urls = []
    file = open('1_products_info.json', 'r', encoding='utf-8')
    info_of_products = json.load(file)
    with open('urls_products.json', 'w') as f:
        for i in range(len(info_of_products)):
            for j in range(len(info_of_products[i])):
                #urls.append(["https://www.mvideo.ru/products/" + f'{info_of_products[i][j]["nameTranslit"]}' + f'-{info_of_products[i][j]["productId"]}', info_of_products[i][j]["productId"]])
                urls.append({"URL": "https://www.mvideo.ru/products/" + f'{info_of_products[i][j]["nameTranslit"]}' + f'-{info_of_products[i][j]["productId"]}', "id": info_of_products[i][j]["productId"]})
        json.dump(urls, f, indent=5, ensure_ascii=False)
    return urls


def get_prices(id_from_filter_message, city_from_message, list_for_filterparams):
    id = get_id(id_from_filter_message, city_from_message, list_for_filterparams)
    get_city_id()
    desired_city = ''
    file_city_ids = open('city_id.json', 'r')
    city_ids = json.load(file_city_ids)
    for i in range(len(city_ids)):
        if city_ids[i]["cityNameRu"] == city_from_message:
            desired_city = city_ids[i]["cityId"]
    price = []
    for i in range(len(id)):
        cookies = {
            '__lhash_': 'fa7ae0180348194b666960594e052dd9',
            'MVID_ACTOR_API_AVAILABILITY': 'true',
            'MVID_BLACK_FRIDAY_ENABLED': 'true',
            'MVID_CART_AVAILABILITY': 'true',
            'MVID_CATALOG_STATE': '1',
            'MVID_CITY_ID': f'\'{desired_city}\'',
            'MVID_COOKIE': '3500',
            'MVID_CREDIT_AVAILABILITY': 'true',
            'MVID_CRITICAL_GTM_INIT_DELAY': '3000',
            'MVID_FILTER_CODES': 'true',
            'MVID_FILTER_TOOLTIP': '1',
            'MVID_FLOCKTORY_ON': 'true',
            'MVID_GEOLOCATION_NEEDED': 'true',
            'MVID_GIFT_KIT': 'true',
            'MVID_GLC': 'true',
            'MVID_GLP': 'true',
            'MVID_GTM_ENABLED': '011',
            'MVID_IMG_RESIZE': 'true',
            'MVID_INTERVAL_DELIVERY': 'true',
            'MVID_IS_NEW_BR_WIDGET': 'true',
            'MVID_KLADR_ID': '7800000000000',
            'MVID_LAYOUT_TYPE': '1',
            'MVID_LP_SOLD_VARIANTS': '3',
            'MVID_MCLICK': 'true',
            'MVID_MCLICK_NEW': 'true',
            'MVID_MINDBOX_DYNAMICALLY': 'true',
            'MVID_MINI_PDP': 'true',
            'MVID_NEW_ACCESSORY': 'true',
            'MVID_NEW_LK_CHECK_CAPTCHA': 'true',
            'MVID_NEW_LK_OTP_TIMER': 'true',
            'MVID_NEW_MBONUS_BLOCK': 'true',
            'MVID_PROMO_CATALOG_ON': 'true',
            'MVID_REGION_ID': '6',
            'MVID_REGION_SHOP': 'S904',
            'MVID_SERVICES': '111',
            'MVID_TIMEZONE_OFFSET': '3',
            'MVID_TYP_CHAT': 'true',
            'MVID_WEB_SBP': 'true',
            'SENTRY_ERRORS_RATE': '0.1',
            'SENTRY_TRANSACTIONS_RATE': '0.5',
            '_gid': 'GA1.2.19773447.1676576416',
            '_ym_uid': '1676576416123405199',
            '_ym_d': '1676576416',
            '__SourceTracker': 'google__organic',
            'admitad_deduplication_cookie': 'google__organic',
            'gdeslon.ru.__arc_domain': 'gdeslon.ru',
            'gdeslon.ru.user_id': '1a77c54e-73db-4470-9d49-50397b073712',
            'tmr_lvid': '6827ac7662087918a8d764c23da85cf5',
            'tmr_lvidTS': '1676576419112',
            'advcake_track_id': '44e79641-8443-4501-9943-b3c7f70bc6ef',
            'advcake_session_id': '0e937b29-63d8-6556-0fb6-7db0c3c6af64',
            'flocktory-uuid': '8bc994f0-c843-4a81-bf80-bb7de5516145-5',
            'uxs_uid': 'bef59730-ae31-11ed-b314-6902a30f5395',
            'afUserId': 'd1866e7d-34f8-4cf9-9779-79ae544d1920-p',
            'AF_SYNC': '1676576420459',
            'adrcid': 'Aa8XqtNYpNCzn3KyYjYqNpw',
            'MVID_GUEST_ID': '22299143724',
            'MVID_VIEWED_PRODUCTS': '',
            'wurfl_device_id': 'generic_web_browser',
            'MVID_CALC_BONUS_RUBLES_PROFIT': 'true',
            'NEED_REQUIRE_APPLY_DISCOUNT': 'true',
            'MVID_CART_MULTI_DELETE': 'true',
            'PROMOLISTING_WITHOUT_STOCK_AB_TEST': '2',
            'MVID_GET_LOCATION_BY_DADATA': 'DaData',
            'PRESELECT_COURIER_DELIVERY_FOR_KBT': 'false',
            'HINTS_FIO_COOKIE_NAME': '1',
            'searchType2': '1',
            'COMPARISON_INDICATOR': 'false',
            'MVID_NEW_OLD': 'eyJjYXJ0IjpmYWxzZSwiZmF2b3JpdGUiOnRydWUsImNvbXBhcmlzb24iOnRydWV9',
            'MVID_OLD_NEW': 'eyJjb21wYXJpc29uIjogdHJ1ZSwgImZhdm9yaXRlIjogdHJ1ZSwgImNhcnQiOiB0cnVlfQ==',
            'deviceType': 'desktop',
            'JSESSIONID': 'KvX6jz3ZYWJfdJ9SKpmtnRSLP2KQRpzMTNMSvT1nZLp0Pnn2yz1G!1118286650',
            'flacktory': 'no',
            'BIGipServeratg-ps-prod_tcp80': '1929698314.20480.0000',
            'bIPs': '2118529862',
            'MVID_GTM_BROWSER_THEME': '1',
            'SMSError': '',
            'authError': '',
            'BIGipServeratg-ps-prod_tcp80_clone': '1929698314.20480.0000',
            #'__zzatgib-w-mvideo': 'MDA0dC0cTApcfEJcdGswPi17CT4VHThHKHIzd2VECRUjIRlcSWx8ZzdZMxoiDmMUS0l9YF0VdURcD10xZH09YHgbJSZXOxszI29FSV0OE24SGjxmHmdJYSVJWk1qJh8YfXQkVQ0RYEBDdmUlLS1SKRIaYg9HV0VnXkZzXWcQREBNR0Jzei9EZiNlTlkjRlhJa2xSVTd+YhZCRBgvSzk9bnBhDysYIVQ1Xz9BYUpKPTdYH0t1MBI=qzN3cA==',
            #'__zzatgib-w-mvideo': 'MDA0dC0cTApcfEJcdGswPi17CT4VHThHKHIzd2VECRUjIRlcSWx8ZzdZMxoiDmMUS0l9YF0VdURcD10xZH09YHgbJSZXOxszI29FSV0OE24SGjxmHmdJYSVJWk1qJh8YfXQkVQ0RYEBDdmUlLS1SKRIaYg9HV0VnXkZzXWcQREBNR0Jzei9EZiNlTlkjRlhJa2xSVTd+YhZCRBgvSzk9bnBhDysYIVQ1Xz9BYUpKPTdYH0t1MBI=qzN3cA==',
            #'cfidsgib-w-mvideo': 'eGX4s2VXWU4ppPgVY2A5GNmITIwnphst1c8s1t+Pyh13NtfkdeZzvm1KIrPH5McReZhkcT0qqFTzC9kJeWTeXBa7Z3KFd1Ujb3p1+nd2pZAgkK3FCtFtxrDUPg4fg+TXWlHB/G4NNbJGXdd6KNDCFRLvNBYVRG3ZMbvGAA==',
            #'cfidsgib-w-mvideo': 'eGX4s2VXWU4ppPgVY2A5GNmITIwnphst1c8s1t+Pyh13NtfkdeZzvm1KIrPH5McReZhkcT0qqFTzC9kJeWTeXBa7Z3KFd1Ujb3p1+nd2pZAgkK3FCtFtxrDUPg4fg+TXWlHB/G4NNbJGXdd6KNDCFRLvNBYVRG3ZMbvGAA==',
            #'gsscgib-w-mvideo': '268NLJq5ssxqDXFU9qAKWHNaW3jrugC29ABFDidNhwJsxFQH+lJdmuWPtihbWVkehNlCILJjWjSDYFmrk1X04M1Q13h1Xb8O8v+8J7eiBaSlUGZJsQ+jwzBOHSxe9EBKlV9sM7hZMOko1IjA/OKSX3uvLMArB5tGfNmKtKk6QN7cCNFZwN4P4rWkrg1DS3VRlJg4QutLv5scTQ3lK0BmWf0IMSQ4gOJPqxlINAWXBTXAQTcf+0IuDGhfD5aNUktHLQ==',
            #'gsscgib-w-mvideo': '268NLJq5ssxqDXFU9qAKWHNaW3jrugC29ABFDidNhwJsxFQH+lJdmuWPtihbWVkehNlCILJjWjSDYFmrk1X04M1Q13h1Xb8O8v+8J7eiBaSlUGZJsQ+jwzBOHSxe9EBKlV9sM7hZMOko1IjA/OKSX3uvLMArB5tGfNmKtKk6QN7cCNFZwN4P4rWkrg1DS3VRlJg4QutLv5scTQ3lK0BmWf0IMSQ4gOJPqxlINAWXBTXAQTcf+0IuDGhfD5aNUktHLQ==',
            #'fgsscgib-w-mvideo': 'fdW8f65b74020ee819408281d7e036ca9cb0bf8f',
            #'fgsscgib-w-mvideo': 'fdW8f65b74020ee819408281d7e036ca9cb0bf8f',
            'cfidsgib-w-mvideo': 'XVxUmL2tPqKSPxqQ3MkKDcoToEhYV+0sySK/Mi1Qrh4f8p8vGqJ+mlh5B9lg6So6xdzD3QpVGiouuj3TMID+zXma0K3SsELh4rEjui3FLeJ0/EhhffeKfmoK9pCsJqCIyBBJiHSff9KuNf14ymZcK7C83JJR227jjOx9Nw==',
            'CACHE_INDICATOR': 'false',
            #'__hash_': 'c816523f4948b5a1b2ea5c8f4a937b4e',
            '_sp_ses.d61c': '*',
            '_ga': 'GA1.2.439832334.1676576415',
            '_dc_gtm_UA-1873769-1': '1',
            '_ym_isad': '2',
            '_dc_gtm_UA-1873769-37': '1',
            'tmr_detect': '0%7C1676991798320',
            '_sp_id.d61c': '4b8037c8-e766-49a0-85d3-f6a2cf196b55.1676576416.16.1676991810.1676919440.28399d1a-8e77-4d3f-81ef-6a63504c0b09.57fd4b53-986b-48d9-8f2f-d8538875493c.e700cc20-2326-4f32-9815-30286bc08fc7.1676991792044.9',
            '_ga_CFMZTSS5FM': 'GS1.1.1676991792.17.1.1676991815.0.0.0',
            '_ga_BNX5WPP3YK': 'GS1.1.1676991792.17.1.1676991815.37.0.0',
            'MVID_ENVCLOUD': 'prod1',
            'mindboxDeviceUUID': '2777081e-2b5c-459c-b470-7c455e608a7c',
            'directCrm-session': '%7B%22deviceGuid%22%3A%222777081e-2b5c-459c-b470-7c455e608a7c%22%7D',
        }

        headers = {
            'authority': 'www.mvideo.ru',
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
            'baggage': 'sentry-transaction=%2F,sentry-public_key=1e9efdeb57cf4127af3f903ec9db1466,sentry-trace_id=980684d5f6c24beab4fc862650b51999,sentry-sample_rate=0.5',
            # Requests sorts cookies= alphabetically
            # 'cookie': '__lhash_=fa7ae0180348194b666960594e052dd9; MVID_ACTOR_API_AVAILABILITY=true; MVID_BLACK_FRIDAY_ENABLED=true; MVID_CART_AVAILABILITY=true; MVID_CATALOG_STATE=1; MVID_CITY_ID=CityCZ_1638; MVID_COOKIE=3500; MVID_CREDIT_AVAILABILITY=true; MVID_CRITICAL_GTM_INIT_DELAY=3000; MVID_FILTER_CODES=true; MVID_FILTER_TOOLTIP=1; MVID_FLOCKTORY_ON=true; MVID_GEOLOCATION_NEEDED=true; MVID_GIFT_KIT=true; MVID_GLC=true; MVID_GLP=true; MVID_GTM_ENABLED=011; MVID_IMG_RESIZE=true; MVID_INTERVAL_DELIVERY=true; MVID_IS_NEW_BR_WIDGET=true; MVID_KLADR_ID=7800000000000; MVID_LAYOUT_TYPE=1; MVID_LP_SOLD_VARIANTS=3; MVID_MCLICK=true; MVID_MCLICK_NEW=true; MVID_MINDBOX_DYNAMICALLY=true; MVID_MINI_PDP=true; MVID_NEW_ACCESSORY=true; MVID_NEW_LK_CHECK_CAPTCHA=true; MVID_NEW_LK_OTP_TIMER=true; MVID_NEW_MBONUS_BLOCK=true; MVID_PROMO_CATALOG_ON=true; MVID_REGION_ID=6; MVID_REGION_SHOP=S904; MVID_SERVICES=111; MVID_TIMEZONE_OFFSET=3; MVID_TYP_CHAT=true; MVID_WEB_SBP=true; SENTRY_ERRORS_RATE=0.1; SENTRY_TRANSACTIONS_RATE=0.5; _gid=GA1.2.19773447.1676576416; _ym_uid=1676576416123405199; _ym_d=1676576416; __SourceTracker=google__organic; admitad_deduplication_cookie=google__organic; gdeslon.ru.__arc_domain=gdeslon.ru; gdeslon.ru.user_id=1a77c54e-73db-4470-9d49-50397b073712; tmr_lvid=6827ac7662087918a8d764c23da85cf5; tmr_lvidTS=1676576419112; advcake_track_id=44e79641-8443-4501-9943-b3c7f70bc6ef; advcake_session_id=0e937b29-63d8-6556-0fb6-7db0c3c6af64; flocktory-uuid=8bc994f0-c843-4a81-bf80-bb7de5516145-5; uxs_uid=bef59730-ae31-11ed-b314-6902a30f5395; afUserId=d1866e7d-34f8-4cf9-9779-79ae544d1920-p; AF_SYNC=1676576420459; adrcid=Aa8XqtNYpNCzn3KyYjYqNpw; MVID_GUEST_ID=22299143724; MVID_VIEWED_PRODUCTS=; wurfl_device_id=generic_web_browser; MVID_CALC_BONUS_RUBLES_PROFIT=true; NEED_REQUIRE_APPLY_DISCOUNT=true; MVID_CART_MULTI_DELETE=true; PROMOLISTING_WITHOUT_STOCK_AB_TEST=2; MVID_GET_LOCATION_BY_DADATA=DaData; PRESELECT_COURIER_DELIVERY_FOR_KBT=false; HINTS_FIO_COOKIE_NAME=1; searchType2=1; COMPARISON_INDICATOR=false; MVID_NEW_OLD=eyJjYXJ0IjpmYWxzZSwiZmF2b3JpdGUiOnRydWUsImNvbXBhcmlzb24iOnRydWV9; MVID_OLD_NEW=eyJjb21wYXJpc29uIjogdHJ1ZSwgImZhdm9yaXRlIjogdHJ1ZSwgImNhcnQiOiB0cnVlfQ==; deviceType=desktop; JSESSIONID=KvX6jz3ZYWJfdJ9SKpmtnRSLP2KQRpzMTNMSvT1nZLp0Pnn2yz1G!1118286650; flacktory=no; BIGipServeratg-ps-prod_tcp80=1929698314.20480.0000; bIPs=2118529862; MVID_GTM_BROWSER_THEME=1; SMSError=; authError=; BIGipServeratg-ps-prod_tcp80_clone=1929698314.20480.0000; __zzatgib-w-mvideo=MDA0dC0cTApcfEJcdGswPi17CT4VHThHKHIzd2VECRUjIRlcSWx8ZzdZMxoiDmMUS0l9YF0VdURcD10xZH09YHgbJSZXOxszI29FSV0OE24SGjxmHmdJYSVJWk1qJh8YfXQkVQ0RYEBDdmUlLS1SKRIaYg9HV0VnXkZzXWcQREBNR0Jzei9EZiNlTlkjRlhJa2xSVTd+YhZCRBgvSzk9bnBhDysYIVQ1Xz9BYUpKPTdYH0t1MBI=qzN3cA==; __zzatgib-w-mvideo=MDA0dC0cTApcfEJcdGswPi17CT4VHThHKHIzd2VECRUjIRlcSWx8ZzdZMxoiDmMUS0l9YF0VdURcD10xZH09YHgbJSZXOxszI29FSV0OE24SGjxmHmdJYSVJWk1qJh8YfXQkVQ0RYEBDdmUlLS1SKRIaYg9HV0VnXkZzXWcQREBNR0Jzei9EZiNlTlkjRlhJa2xSVTd+YhZCRBgvSzk9bnBhDysYIVQ1Xz9BYUpKPTdYH0t1MBI=qzN3cA==; cfidsgib-w-mvideo=eGX4s2VXWU4ppPgVY2A5GNmITIwnphst1c8s1t+Pyh13NtfkdeZzvm1KIrPH5McReZhkcT0qqFTzC9kJeWTeXBa7Z3KFd1Ujb3p1+nd2pZAgkK3FCtFtxrDUPg4fg+TXWlHB/G4NNbJGXdd6KNDCFRLvNBYVRG3ZMbvGAA==; cfidsgib-w-mvideo=eGX4s2VXWU4ppPgVY2A5GNmITIwnphst1c8s1t+Pyh13NtfkdeZzvm1KIrPH5McReZhkcT0qqFTzC9kJeWTeXBa7Z3KFd1Ujb3p1+nd2pZAgkK3FCtFtxrDUPg4fg+TXWlHB/G4NNbJGXdd6KNDCFRLvNBYVRG3ZMbvGAA==; gsscgib-w-mvideo=268NLJq5ssxqDXFU9qAKWHNaW3jrugC29ABFDidNhwJsxFQH+lJdmuWPtihbWVkehNlCILJjWjSDYFmrk1X04M1Q13h1Xb8O8v+8J7eiBaSlUGZJsQ+jwzBOHSxe9EBKlV9sM7hZMOko1IjA/OKSX3uvLMArB5tGfNmKtKk6QN7cCNFZwN4P4rWkrg1DS3VRlJg4QutLv5scTQ3lK0BmWf0IMSQ4gOJPqxlINAWXBTXAQTcf+0IuDGhfD5aNUktHLQ==; gsscgib-w-mvideo=268NLJq5ssxqDXFU9qAKWHNaW3jrugC29ABFDidNhwJsxFQH+lJdmuWPtihbWVkehNlCILJjWjSDYFmrk1X04M1Q13h1Xb8O8v+8J7eiBaSlUGZJsQ+jwzBOHSxe9EBKlV9sM7hZMOko1IjA/OKSX3uvLMArB5tGfNmKtKk6QN7cCNFZwN4P4rWkrg1DS3VRlJg4QutLv5scTQ3lK0BmWf0IMSQ4gOJPqxlINAWXBTXAQTcf+0IuDGhfD5aNUktHLQ==; fgsscgib-w-mvideo=fdW8f65b74020ee819408281d7e036ca9cb0bf8f; fgsscgib-w-mvideo=fdW8f65b74020ee819408281d7e036ca9cb0bf8f; cfidsgib-w-mvideo=XVxUmL2tPqKSPxqQ3MkKDcoToEhYV+0sySK/Mi1Qrh4f8p8vGqJ+mlh5B9lg6So6xdzD3QpVGiouuj3TMID+zXma0K3SsELh4rEjui3FLeJ0/EhhffeKfmoK9pCsJqCIyBBJiHSff9KuNf14ymZcK7C83JJR227jjOx9Nw==; CACHE_INDICATOR=false; __hash_=c816523f4948b5a1b2ea5c8f4a937b4e; _sp_ses.d61c=*; _ga=GA1.2.439832334.1676576415; _dc_gtm_UA-1873769-1=1; _ym_isad=2; _dc_gtm_UA-1873769-37=1; tmr_detect=0%7C1676991798320; _sp_id.d61c=4b8037c8-e766-49a0-85d3-f6a2cf196b55.1676576416.16.1676991810.1676919440.28399d1a-8e77-4d3f-81ef-6a63504c0b09.57fd4b53-986b-48d9-8f2f-d8538875493c.e700cc20-2326-4f32-9815-30286bc08fc7.1676991792044.9; _ga_CFMZTSS5FM=GS1.1.1676991792.17.1.1676991815.0.0.0; _ga_BNX5WPP3YK=GS1.1.1676991792.17.1.1676991815.37.0.0; MVID_ENVCLOUD=prod1; mindboxDeviceUUID=2777081e-2b5c-459c-b470-7c455e608a7c; directCrm-session=%7B%22deviceGuid%22%3A%222777081e-2b5c-459c-b470-7c455e608a7c%22%7D',
            'referer': 'https://www.mvideo.ru/noutbuki-planshety-komputery-8/noutbuki-118/f/tolko-v-nalichii=da',
            'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sentry-trace': '980684d5f6c24beab4fc862650b51999-b2a57fd2182701b0-1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            'x-set-application-id': 'd9658309-cb54-4708-ae05-5b8434dd9593',
        }

        string_of_ids = ''
        for j in range(len(id[i])):
            string_of_ids += str(id[i][j])
            string_of_ids += ','

        params = {
            'productIds': string_of_ids,
            'addBonusRubles': 'true',
            'isPromoApplied': 'true',
        }

        response = requests.get('https://www.mvideo.ru/bff/products/prices', params=params, cookies=cookies,
                                headers=headers).json()
        price_info = response.get('body').get('materialPrices')
        for item in price_info:
            item_id = item.get('price').get('productId')
            item_base_price = item.get('price').get('basePrice')
            item_sale_price = item.get('price').get('salePrice')
            item_base_promo_price = item.get('price').get('basePromoPrice')
            price.append({"id": item_id, "base_price": item_base_price, "sale_price": item_sale_price,
                          "base_promo_price": item_base_promo_price})

    with open('prices_of_products.json', 'w') as file:
        json.dump(price, file, indent=5, ensure_ascii=False)


def get_count_pages(id_from_filter_message, list_for_filterparams):
    cookies = {
        '__lhash_': 'fa7ae0180348194b666960594e052dd9',
        'MVID_ACTOR_API_AVAILABILITY': 'true',
        'MVID_BLACK_FRIDAY_ENABLED': 'true',
        'MVID_CART_AVAILABILITY': 'true',
        'MVID_CATALOG_STATE': '1',
        'MVID_CITY_ID': 'CityCZ_1638',
        'MVID_COOKIE': '3500',
        'MVID_CREDIT_AVAILABILITY': 'true',
        'MVID_CRITICAL_GTM_INIT_DELAY': '3000',
        'MVID_FILTER_CODES': 'true',
        'MVID_FILTER_TOOLTIP': '1',
        'MVID_FLOCKTORY_ON': 'true',
        'MVID_GEOLOCATION_NEEDED': 'true',
        'MVID_GIFT_KIT': 'true',
        'MVID_GLC': 'true',
        'MVID_GLP': 'true',
        'MVID_GTM_ENABLED': '011',
        'MVID_IMG_RESIZE': 'true',
        'MVID_INTERVAL_DELIVERY': 'true',
        'MVID_IS_NEW_BR_WIDGET': 'true',
        'MVID_KLADR_ID': '7800000000000',
        'MVID_LAYOUT_TYPE': '1',
        'MVID_LP_SOLD_VARIANTS': '3',
        'MVID_MCLICK': 'true',
        'MVID_MCLICK_NEW': 'true',
        'MVID_MINDBOX_DYNAMICALLY': 'true',
        'MVID_MINI_PDP': 'true',
        'MVID_NEW_ACCESSORY': 'true',
        'MVID_NEW_LK_CHECK_CAPTCHA': 'true',
        'MVID_NEW_LK_OTP_TIMER': 'true',
        'MVID_NEW_MBONUS_BLOCK': 'true',
        'MVID_PROMO_CATALOG_ON': 'true',
        'MVID_REGION_ID': '6',
        'MVID_REGION_SHOP': 'S904',
        'MVID_SERVICES': '111',
        'MVID_TIMEZONE_OFFSET': '3',
        'MVID_TYP_CHAT': 'true',
        'MVID_WEB_SBP': 'true',
        'SENTRY_ERRORS_RATE': '0.1',
        'SENTRY_TRANSACTIONS_RATE': '0.5',
        '_gid': 'GA1.2.19773447.1676576416',
        '_ym_uid': '1676576416123405199',
        '_ym_d': '1676576416',
        '__SourceTracker': 'google__organic',
        'admitad_deduplication_cookie': 'google__organic',
        'gdeslon.ru.__arc_domain': 'gdeslon.ru',
        'gdeslon.ru.user_id': '1a77c54e-73db-4470-9d49-50397b073712',
        'tmr_lvid': '6827ac7662087918a8d764c23da85cf5',
        'tmr_lvidTS': '1676576419112',
        'advcake_track_id': '44e79641-8443-4501-9943-b3c7f70bc6ef',
        'advcake_session_id': '0e937b29-63d8-6556-0fb6-7db0c3c6af64',
        'flocktory-uuid': '8bc994f0-c843-4a81-bf80-bb7de5516145-5',
        'uxs_uid': 'bef59730-ae31-11ed-b314-6902a30f5395',
        'afUserId': 'd1866e7d-34f8-4cf9-9779-79ae544d1920-p',
        'AF_SYNC': '1676576420459',
        'adrcid': 'Aa8XqtNYpNCzn3KyYjYqNpw',
        '_ym_isad': '2',
        '_sp_ses.d61c': '*',
        'mindboxDeviceUUID': '2777081e-2b5c-459c-b470-7c455e608a7c',
        'directCrm-session': '%7B%22deviceGuid%22%3A%222777081e-2b5c-459c-b470-7c455e608a7c%22%7D',
        '_sp_id.d61c': '4b8037c8-e766-49a0-85d3-f6a2cf196b55.1676576416.4.1676661776.1676653296.68d8c146-393c-439e-9f9d-ca4414bd7d05.a11bf9b9-8419-4c27-8b2d-6237a2ea7429.0632b9f8-1a1c-4990-bddc-4c8fa75f6f69.1676655703529.103',
        '_ga_CFMZTSS5FM': 'GS1.1.1676659077.5.1.1676661775.0.0.0',
        '_ga_BNX5WPP3YK': 'GS1.1.1676659077.5.1.1676661775.45.0.0',
        '_ga': 'GA1.2.439832334.1676576415',
        'tmr_detect': '0%7C1676661781538',
        # '__hash_': 'f06f44a4c511ca9efc6ef8cf739cef5d',
        'MVID_ENVCLOUD': 'prod1',
    }

    headers = {
        'authority': 'www.mvideo.ru',
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
        'baggage': 'sentry-transaction=%2F,sentry-public_key=1e9efdeb57cf4127af3f903ec9db1466,sentry-trace_id=0bf2ad35d39b4e6ab6c72f4f8202c1f1,sentry-sample_rate=0.5',
        # Requests sorts cookies= alphabetically
        # 'cookie': '__lhash_=fa7ae0180348194b666960594e052dd9; MVID_ACTOR_API_AVAILABILITY=true; MVID_BLACK_FRIDAY_ENABLED=true; MVID_CART_AVAILABILITY=true; MVID_CATALOG_STATE=1; MVID_CITY_ID=CityCZ_1638; MVID_COOKIE=3500; MVID_CREDIT_AVAILABILITY=true; MVID_CRITICAL_GTM_INIT_DELAY=3000; MVID_FILTER_CODES=true; MVID_FILTER_TOOLTIP=1; MVID_FLOCKTORY_ON=true; MVID_GEOLOCATION_NEEDED=true; MVID_GIFT_KIT=true; MVID_GLC=true; MVID_GLP=true; MVID_GTM_ENABLED=011; MVID_IMG_RESIZE=true; MVID_INTERVAL_DELIVERY=true; MVID_IS_NEW_BR_WIDGET=true; MVID_KLADR_ID=7800000000000; MVID_LAYOUT_TYPE=1; MVID_LP_SOLD_VARIANTS=3; MVID_MCLICK=true; MVID_MCLICK_NEW=true; MVID_MINDBOX_DYNAMICALLY=true; MVID_MINI_PDP=true; MVID_NEW_ACCESSORY=true; MVID_NEW_LK_CHECK_CAPTCHA=true; MVID_NEW_LK_OTP_TIMER=true; MVID_NEW_MBONUS_BLOCK=true; MVID_PROMO_CATALOG_ON=true; MVID_REGION_ID=6; MVID_REGION_SHOP=S904; MVID_SERVICES=111; MVID_TIMEZONE_OFFSET=3; MVID_TYP_CHAT=true; MVID_WEB_SBP=true; SENTRY_ERRORS_RATE=0.1; SENTRY_TRANSACTIONS_RATE=0.5; _gid=GA1.2.19773447.1676576416; _ym_uid=1676576416123405199; _ym_d=1676576416; __SourceTracker=google__organic; admitad_deduplication_cookie=google__organic; gdeslon.ru.__arc_domain=gdeslon.ru; gdeslon.ru.user_id=1a77c54e-73db-4470-9d49-50397b073712; tmr_lvid=6827ac7662087918a8d764c23da85cf5; tmr_lvidTS=1676576419112; advcake_track_id=44e79641-8443-4501-9943-b3c7f70bc6ef; advcake_session_id=0e937b29-63d8-6556-0fb6-7db0c3c6af64; flocktory-uuid=8bc994f0-c843-4a81-bf80-bb7de5516145-5; uxs_uid=bef59730-ae31-11ed-b314-6902a30f5395; afUserId=d1866e7d-34f8-4cf9-9779-79ae544d1920-p; AF_SYNC=1676576420459; adrcid=Aa8XqtNYpNCzn3KyYjYqNpw; _ym_isad=2; _sp_ses.d61c=*; mindboxDeviceUUID=2777081e-2b5c-459c-b470-7c455e608a7c; directCrm-session=%7B%22deviceGuid%22%3A%222777081e-2b5c-459c-b470-7c455e608a7c%22%7D; _sp_id.d61c=4b8037c8-e766-49a0-85d3-f6a2cf196b55.1676576416.4.1676661776.1676653296.68d8c146-393c-439e-9f9d-ca4414bd7d05.a11bf9b9-8419-4c27-8b2d-6237a2ea7429.0632b9f8-1a1c-4990-bddc-4c8fa75f6f69.1676655703529.103; _ga_CFMZTSS5FM=GS1.1.1676659077.5.1.1676661775.0.0.0; _ga_BNX5WPP3YK=GS1.1.1676659077.5.1.1676661775.45.0.0; _ga=GA1.2.439832334.1676576415; tmr_detect=0%7C1676661781538; __hash_=f06f44a4c511ca9efc6ef8cf739cef5d; MVID_ENVCLOUD=prod1',
        'referer': 'https://www.mvideo.ru/noutbuki-planshety-komputery-8/noutbuki-118/f/tolko-v-nalichii=da?from=under_search',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sentry-trace': '0bf2ad35d39b4e6ab6c72f4f8202c1f1-a7fee6a66e5e88dc-1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'x-set-application-id': '51c7c4f8-f510-4b72-9df1-950fd2abf377',
    }

    params = {
        'categoryId': f'{id_from_filter_message}',
        'offset': '0',
        'limit': '24',
        #'filterParams': 'WyJ0b2xrby12LW5hbGljaGlpIiwiIiwiZGEiXQ==',
        'filterParams': list_for_filterparams,
        'doTranslit': 'true',
    }

    response = requests.get('https://www.mvideo.ru/bff/products/listing', params=params, cookies=cookies,
                            headers=headers).json()
    count_pages = math.ceil(response.get('body').get('total') / 24)
    return count_pages


def get_id(id_from_filter_message, city_from_message, list_for_filterparams):
    l = []
    get_city_id()
    desired_city = ''
    file_city_ids = open('city_id.json', 'r')
    city_ids = json.load(file_city_ids)
    for i in range(len(city_ids)):
        if city_ids[i]["cityNameRu"] == city_from_message:
            desired_city = city_ids[i]["cityId"]
    pages = get_count_pages(id_from_filter_message, list_for_filterparams)

    with open('products_ids.json', 'w') as file:
        for i in range(0, pages*24, 24):
            cookies = {
                '__lhash_': 'fa7ae0180348194b666960594e052dd9',
                'MVID_ACTOR_API_AVAILABILITY': 'true',
                'MVID_BLACK_FRIDAY_ENABLED': 'true',
                'MVID_CART_AVAILABILITY': 'true',
                'MVID_CATALOG_STATE': '1',
                'MVID_CITY_ID': f'\'{desired_city}\'',
                'MVID_COOKIE': '3500',
                'MVID_CREDIT_AVAILABILITY': 'true',
                'MVID_CRITICAL_GTM_INIT_DELAY': '3000',
                'MVID_FILTER_CODES': 'true',
                'MVID_FILTER_TOOLTIP': '1',
                'MVID_FLOCKTORY_ON': 'true',
                'MVID_GEOLOCATION_NEEDED': 'true',
                'MVID_GIFT_KIT': 'true',
                'MVID_GLC': 'true',
                'MVID_GLP': 'true',
                'MVID_GTM_ENABLED': '011',
                'MVID_IMG_RESIZE': 'true',
                'MVID_INTERVAL_DELIVERY': 'true',
                'MVID_IS_NEW_BR_WIDGET': 'true',
                'MVID_KLADR_ID': '7800000000000',
                'MVID_LAYOUT_TYPE': '1',
                'MVID_LP_SOLD_VARIANTS': '3',
                'MVID_MCLICK': 'true',
                'MVID_MCLICK_NEW': 'true',
                'MVID_MINDBOX_DYNAMICALLY': 'true',
                'MVID_MINI_PDP': 'true',
                'MVID_NEW_ACCESSORY': 'true',
                'MVID_NEW_LK_CHECK_CAPTCHA': 'true',
                'MVID_NEW_LK_OTP_TIMER': 'true',
                'MVID_NEW_MBONUS_BLOCK': 'true',
                'MVID_PROMO_CATALOG_ON': 'true',
                'MVID_REGION_ID': '6',
                'MVID_REGION_SHOP': 'S904',
                'MVID_SERVICES': '111',
                'MVID_TIMEZONE_OFFSET': '3',
                'MVID_TYP_CHAT': 'true',
                'MVID_WEB_SBP': 'true',
                'SENTRY_ERRORS_RATE': '0.1',
                'SENTRY_TRANSACTIONS_RATE': '0.5',
                '_gid': 'GA1.2.19773447.1676576416',
                '_ym_uid': '1676576416123405199',
                '_ym_d': '1676576416',
                '__SourceTracker': 'google__organic',
                'admitad_deduplication_cookie': 'google__organic',
                'gdeslon.ru.__arc_domain': 'gdeslon.ru',
                'gdeslon.ru.user_id': '1a77c54e-73db-4470-9d49-50397b073712',
                'tmr_lvid': '6827ac7662087918a8d764c23da85cf5',
                'tmr_lvidTS': '1676576419112',
                'advcake_track_id': '44e79641-8443-4501-9943-b3c7f70bc6ef',
                'advcake_session_id': '0e937b29-63d8-6556-0fb6-7db0c3c6af64',
                'flocktory-uuid': '8bc994f0-c843-4a81-bf80-bb7de5516145-5',
                'uxs_uid': 'bef59730-ae31-11ed-b314-6902a30f5395',
                'afUserId': 'd1866e7d-34f8-4cf9-9779-79ae544d1920-p',
                'AF_SYNC': '1676576420459',
                'adrcid': 'Aa8XqtNYpNCzn3KyYjYqNpw',
                '_ym_isad': '2',
                '_sp_ses.d61c': '*',
                'mindboxDeviceUUID': '2777081e-2b5c-459c-b470-7c455e608a7c',
                'directCrm-session': '%7B%22deviceGuid%22%3A%222777081e-2b5c-459c-b470-7c455e608a7c%22%7D',
                '_sp_id.d61c': '4b8037c8-e766-49a0-85d3-f6a2cf196b55.1676576416.4.1676661776.1676653296.68d8c146-393c-439e-9f9d-ca4414bd7d05.a11bf9b9-8419-4c27-8b2d-6237a2ea7429.0632b9f8-1a1c-4990-bddc-4c8fa75f6f69.1676655703529.103',
                '_ga_CFMZTSS5FM': 'GS1.1.1676659077.5.1.1676661775.0.0.0',
                '_ga_BNX5WPP3YK': 'GS1.1.1676659077.5.1.1676661775.45.0.0',
                '_ga': 'GA1.2.439832334.1676576415',
                'tmr_detect': '0%7C1676661781538',
                #'__hash_': 'f06f44a4c511ca9efc6ef8cf739cef5d',
                'MVID_ENVCLOUD': 'prod1',
            }

            headers = {
                'authority': 'www.mvideo.ru',
                'accept': 'application/json',
                'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
                'baggage': 'sentry-transaction=%2F,sentry-public_key=1e9efdeb57cf4127af3f903ec9db1466,sentry-trace_id=0bf2ad35d39b4e6ab6c72f4f8202c1f1,sentry-sample_rate=0.5',
                # Requests sorts cookies= alphabetically
                # 'cookie': '__lhash_=fa7ae0180348194b666960594e052dd9; MVID_ACTOR_API_AVAILABILITY=true; MVID_BLACK_FRIDAY_ENABLED=true; MVID_CART_AVAILABILITY=true; MVID_CATALOG_STATE=1; MVID_CITY_ID=CityCZ_1638; MVID_COOKIE=3500; MVID_CREDIT_AVAILABILITY=true; MVID_CRITICAL_GTM_INIT_DELAY=3000; MVID_FILTER_CODES=true; MVID_FILTER_TOOLTIP=1; MVID_FLOCKTORY_ON=true; MVID_GEOLOCATION_NEEDED=true; MVID_GIFT_KIT=true; MVID_GLC=true; MVID_GLP=true; MVID_GTM_ENABLED=011; MVID_IMG_RESIZE=true; MVID_INTERVAL_DELIVERY=true; MVID_IS_NEW_BR_WIDGET=true; MVID_KLADR_ID=7800000000000; MVID_LAYOUT_TYPE=1; MVID_LP_SOLD_VARIANTS=3; MVID_MCLICK=true; MVID_MCLICK_NEW=true; MVID_MINDBOX_DYNAMICALLY=true; MVID_MINI_PDP=true; MVID_NEW_ACCESSORY=true; MVID_NEW_LK_CHECK_CAPTCHA=true; MVID_NEW_LK_OTP_TIMER=true; MVID_NEW_MBONUS_BLOCK=true; MVID_PROMO_CATALOG_ON=true; MVID_REGION_ID=6; MVID_REGION_SHOP=S904; MVID_SERVICES=111; MVID_TIMEZONE_OFFSET=3; MVID_TYP_CHAT=true; MVID_WEB_SBP=true; SENTRY_ERRORS_RATE=0.1; SENTRY_TRANSACTIONS_RATE=0.5; _gid=GA1.2.19773447.1676576416; _ym_uid=1676576416123405199; _ym_d=1676576416; __SourceTracker=google__organic; admitad_deduplication_cookie=google__organic; gdeslon.ru.__arc_domain=gdeslon.ru; gdeslon.ru.user_id=1a77c54e-73db-4470-9d49-50397b073712; tmr_lvid=6827ac7662087918a8d764c23da85cf5; tmr_lvidTS=1676576419112; advcake_track_id=44e79641-8443-4501-9943-b3c7f70bc6ef; advcake_session_id=0e937b29-63d8-6556-0fb6-7db0c3c6af64; flocktory-uuid=8bc994f0-c843-4a81-bf80-bb7de5516145-5; uxs_uid=bef59730-ae31-11ed-b314-6902a30f5395; afUserId=d1866e7d-34f8-4cf9-9779-79ae544d1920-p; AF_SYNC=1676576420459; adrcid=Aa8XqtNYpNCzn3KyYjYqNpw; _ym_isad=2; _sp_ses.d61c=*; mindboxDeviceUUID=2777081e-2b5c-459c-b470-7c455e608a7c; directCrm-session=%7B%22deviceGuid%22%3A%222777081e-2b5c-459c-b470-7c455e608a7c%22%7D; _sp_id.d61c=4b8037c8-e766-49a0-85d3-f6a2cf196b55.1676576416.4.1676661776.1676653296.68d8c146-393c-439e-9f9d-ca4414bd7d05.a11bf9b9-8419-4c27-8b2d-6237a2ea7429.0632b9f8-1a1c-4990-bddc-4c8fa75f6f69.1676655703529.103; _ga_CFMZTSS5FM=GS1.1.1676659077.5.1.1676661775.0.0.0; _ga_BNX5WPP3YK=GS1.1.1676659077.5.1.1676661775.45.0.0; _ga=GA1.2.439832334.1676576415; tmr_detect=0%7C1676661781538; __hash_=f06f44a4c511ca9efc6ef8cf739cef5d; MVID_ENVCLOUD=prod1',
                'referer': 'https://www.mvideo.ru/noutbuki-planshety-komputery-8/noutbuki-118/f/tolko-v-nalichii=da?from=under_search',
                'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'sentry-trace': '0bf2ad35d39b4e6ab6c72f4f8202c1f1-a7fee6a66e5e88dc-1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
                'x-set-application-id': '51c7c4f8-f510-4b72-9df1-950fd2abf377',
            }

            params = {
                'categoryId': f'{id_from_filter_message}',
                'offset': f'{i}',
                'limit': '24',
                #'filterParams': 'WyJ0b2xrby12LW5hbGljaGlpIiwiIiwiZGEiXQ==',
                'filterParams': list_for_filterparams,
                'doTranslit': 'true',
            }
            try:
                response = requests.get('https://www.mvideo.ru/bff/products/listing', params=params, cookies=cookies,
                                    headers=headers).json()
                products_ids = response.get('body').get('products')
                l.append(products_ids)
            except requests.exceptions.TooManyRedirects:
                pass
        json.dump(l, file, indent=5, ensure_ascii=False)
        return l


def get_info_products(id_from_filter_message, city_from_message, list_for_filterparams):
    #get_city_id()
    desired_city = ''
    file_city_ids = open('city_id.json', 'r')
    city_ids = json.load(file_city_ids)
    for i in range(len(city_ids)):
        if city_ids[i]["cityNameRu"] == city_from_message:
            desired_city = city_ids[i]["cityId"]

    get_filters(id_from_filter_message, city_from_message)

    cookies = {
        '__lhash_': 'fa7ae0180348194b666960594e052dd9',
        'MVID_ACTOR_API_AVAILABILITY': 'true',
        'MVID_BLACK_FRIDAY_ENABLED': 'true',
        'MVID_CART_AVAILABILITY': 'true',
        'MVID_CATALOG_STATE': '1',
        'MVID_CITY_ID': f'\'{desired_city}\'',
        'MVID_COOKIE': '3500',
        'MVID_CREDIT_AVAILABILITY': 'true',
        'MVID_CRITICAL_GTM_INIT_DELAY': '3000',
        'MVID_FILTER_CODES': 'true',
        'MVID_FILTER_TOOLTIP': '1',
        'MVID_FLOCKTORY_ON': 'true',
        'MVID_GEOLOCATION_NEEDED': 'true',
        'MVID_GIFT_KIT': 'true',
        'MVID_GLC': 'true',
        'MVID_GLP': 'true',
        'MVID_GTM_ENABLED': '011',
        'MVID_IMG_RESIZE': 'true',
        'MVID_INTERVAL_DELIVERY': 'true',
        'MVID_IS_NEW_BR_WIDGET': 'true',
        'MVID_KLADR_ID': '7800000000000',
        'MVID_LAYOUT_TYPE': '1',
        'MVID_LP_SOLD_VARIANTS': '3',
        'MVID_MCLICK': 'true',
        'MVID_MCLICK_NEW': 'true',
        'MVID_MINDBOX_DYNAMICALLY': 'true',
        'MVID_MINI_PDP': 'true',
        'MVID_NEW_ACCESSORY': 'true',
        'MVID_NEW_LK_CHECK_CAPTCHA': 'true',
        'MVID_NEW_LK_OTP_TIMER': 'true',
        'MVID_NEW_MBONUS_BLOCK': 'true',
        'MVID_PROMO_CATALOG_ON': 'true',
        'MVID_REGION_ID': '6',
        'MVID_REGION_SHOP': 'S904',
        'MVID_SERVICES': '111',
        'MVID_TIMEZONE_OFFSET': '3',
        'MVID_TYP_CHAT': 'true',
        'MVID_WEB_SBP': 'true',
        'SENTRY_ERRORS_RATE': '0.1',
        'SENTRY_TRANSACTIONS_RATE': '0.5',
        '_gid': 'GA1.2.19773447.1676576416',
        '_ym_uid': '1676576416123405199',
        '_ym_d': '1676576416',
        '_ym_isad': '2',
        '__SourceTracker': 'google__organic',
        'admitad_deduplication_cookie': 'google__organic',
        'gdeslon.ru.__arc_domain': 'gdeslon.ru',
        'gdeslon.ru.user_id': '1a77c54e-73db-4470-9d49-50397b073712',
        'tmr_lvid': '6827ac7662087918a8d764c23da85cf5',
        'tmr_lvidTS': '1676576419112',
        'advcake_track_id': '44e79641-8443-4501-9943-b3c7f70bc6ef',
        'advcake_session_id': '0e937b29-63d8-6556-0fb6-7db0c3c6af64',
        'flocktory-uuid': '8bc994f0-c843-4a81-bf80-bb7de5516145-5',
        'uxs_uid': 'bef59730-ae31-11ed-b314-6902a30f5395',
        'afUserId': 'd1866e7d-34f8-4cf9-9779-79ae544d1920-p',
        'AF_SYNC': '1676576420459',
        'adrcid': 'Aa8XqtNYpNCzn3KyYjYqNpw',
        '__hash_': 'ebaeb49d0a1a2935852ec58473d20ead',
        '_dc_gtm_UA-1873769-1': '1',
        '_sp_ses.d61c': '*',
        '_dc_gtm_UA-1873769-37': '1',
        'SMSError': '',
        'authError': '',
        'tmr_detect': '0%7C1676646083918',
        '_sp_id.d61c': '4b8037c8-e766-49a0-85d3-f6a2cf196b55.1676576416.2.1676646097.1676577714.94b658c5-033e-4cc6-b248-6f55217a9f0b.97d3262e-20c4-46ba-898d-6ebc81573edb.eec912d0-e967-47ec-b0c3-27d1238c8f87.1676646078316.41',
        '_ga_CFMZTSS5FM': 'GS1.1.1676646078.2.1.1676646097.0.0.0',
        '_ga_BNX5WPP3YK': 'GS1.1.1676646078.2.1.1676646097.41.0.0',
        '_ga': 'GA1.2.439832334.1676576415',
        'MVID_ENVCLOUD': 'prod2',
        'mindboxDeviceUUID': '2777081e-2b5c-459c-b470-7c455e608a7c',
        'directCrm-session': '%7B%22deviceGuid%22%3A%222777081e-2b5c-459c-b470-7c455e608a7c%22%7D',
    }

    headers = {
        'authority': 'www.mvideo.ru',
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
        'baggage': 'sentry-transaction=%2F,sentry-public_key=1e9efdeb57cf4127af3f903ec9db1466,sentry-trace_id=79068bac277c430bb1045a882261df2e,sentry-sample_rate=0.5',
        # Already added when you pass json=
        # 'content-type': 'application/json',
        # Requests sorts cookies= alphabetically
        # 'cookie': '__lhash_=fa7ae0180348194b666960594e052dd9; MVID_ACTOR_API_AVAILABILITY=true; MVID_BLACK_FRIDAY_ENABLED=true; MVID_CART_AVAILABILITY=true; MVID_CATALOG_STATE=1; MVID_CITY_ID=CityCZ_1638; MVID_COOKIE=3500; MVID_CREDIT_AVAILABILITY=true; MVID_CRITICAL_GTM_INIT_DELAY=3000; MVID_FILTER_CODES=true; MVID_FILTER_TOOLTIP=1; MVID_FLOCKTORY_ON=true; MVID_GEOLOCATION_NEEDED=true; MVID_GIFT_KIT=true; MVID_GLC=true; MVID_GLP=true; MVID_GTM_ENABLED=011; MVID_IMG_RESIZE=true; MVID_INTERVAL_DELIVERY=true; MVID_IS_NEW_BR_WIDGET=true; MVID_KLADR_ID=7800000000000; MVID_LAYOUT_TYPE=1; MVID_LP_SOLD_VARIANTS=3; MVID_MCLICK=true; MVID_MCLICK_NEW=true; MVID_MINDBOX_DYNAMICALLY=true; MVID_MINI_PDP=true; MVID_NEW_ACCESSORY=true; MVID_NEW_LK_CHECK_CAPTCHA=true; MVID_NEW_LK_OTP_TIMER=true; MVID_NEW_MBONUS_BLOCK=true; MVID_PROMO_CATALOG_ON=true; MVID_REGION_ID=6; MVID_REGION_SHOP=S904; MVID_SERVICES=111; MVID_TIMEZONE_OFFSET=3; MVID_TYP_CHAT=true; MVID_WEB_SBP=true; SENTRY_ERRORS_RATE=0.1; SENTRY_TRANSACTIONS_RATE=0.5; _gid=GA1.2.19773447.1676576416; _ym_uid=1676576416123405199; _ym_d=1676576416; _ym_isad=2; __SourceTracker=google__organic; admitad_deduplication_cookie=google__organic; gdeslon.ru.__arc_domain=gdeslon.ru; gdeslon.ru.user_id=1a77c54e-73db-4470-9d49-50397b073712; tmr_lvid=6827ac7662087918a8d764c23da85cf5; tmr_lvidTS=1676576419112; advcake_track_id=44e79641-8443-4501-9943-b3c7f70bc6ef; advcake_session_id=0e937b29-63d8-6556-0fb6-7db0c3c6af64; flocktory-uuid=8bc994f0-c843-4a81-bf80-bb7de5516145-5; uxs_uid=bef59730-ae31-11ed-b314-6902a30f5395; afUserId=d1866e7d-34f8-4cf9-9779-79ae544d1920-p; AF_SYNC=1676576420459; adrcid=Aa8XqtNYpNCzn3KyYjYqNpw; __hash_=ebaeb49d0a1a2935852ec58473d20ead; _dc_gtm_UA-1873769-1=1; _sp_ses.d61c=*; _dc_gtm_UA-1873769-37=1; SMSError=; authError=; tmr_detect=0%7C1676646083918; _sp_id.d61c=4b8037c8-e766-49a0-85d3-f6a2cf196b55.1676576416.2.1676646097.1676577714.94b658c5-033e-4cc6-b248-6f55217a9f0b.97d3262e-20c4-46ba-898d-6ebc81573edb.eec912d0-e967-47ec-b0c3-27d1238c8f87.1676646078316.41; _ga_CFMZTSS5FM=GS1.1.1676646078.2.1.1676646097.0.0.0; _ga_BNX5WPP3YK=GS1.1.1676646078.2.1.1676646097.41.0.0; _ga=GA1.2.439832334.1676576415; MVID_ENVCLOUD=prod2; mindboxDeviceUUID=2777081e-2b5c-459c-b470-7c455e608a7c; directCrm-session=%7B%22deviceGuid%22%3A%222777081e-2b5c-459c-b470-7c455e608a7c%22%7D',
        'origin': 'https://www.mvideo.ru',
        'referer': 'https://www.mvideo.ru/noutbuki-planshety-komputery-8/noutbuki-118?from=under_search',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sentry-trace': '79068bac277c430bb1045a882261df2e-b4811ff447cd6a6a-0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'x-set-application-id': 'db57d908-3389-4d08-a5fa-6d2c5deb7ffe',
    }

    id = get_id(id_from_filter_message, city_from_message, list_for_filterparams)
    get_prices(id_from_filter_message, city_from_message, list_for_filterparams)
    info = []
    file_of_prices = open('prices_of_products.json', 'r')
    prices = json.load(file_of_prices)
    for i in range(len(id)):

        json_data = {
            'productIds':
            id[i],
            'mediaTypes': [
                'images',
            ],
            'category': True,
            'status': True,
            'brand': True,
            'propertyTypes': [
                'KEY',
            ],
            'propertiesConfig': {
                'propertiesPortionSize': 5,
            },
            'multioffer': False,
            }

        params = {
            'categoryId': f'{id_from_filter_message}',
            'offset': f'{i*len(id[i])}',
            'limit': '24',
            #'filterParams': 'WyJ0b2xrby12LW5hbGljaGlpIiwiIiwiZGEiXQ==',
            'filterParams': list_for_filterparams,
            'doTranslit': 'true',
        }
        time.sleep(40)
        try:
            response = requests.post('https://www.mvideo.ru/bff/product-details/list', cookies=cookies, headers=headers, params=params, json=json_data).json()
            products_info = response.get('body').get('products')
            for t in range(len(products_info)):
                for j in range(len(prices)):
                    if products_info[t]["productId"] == prices[j]["id"]:
                        products_info[t]["Price"] = prices[j]
            info.append(products_info)
        except json.decoder.JSONDecodeError:
            zapor.append(id[i])
            pass
    file_of_prices.close()
    with open('1_products_info.json', 'w', encoding='utf-8') as file:
        json.dump(info, file, indent=5, ensure_ascii=False)


def func_chunks_generators(lst, n):
    l = []
    for i in range(0, len(lst), n):
        l.append(lst[i : i + n])
    return l

logging.basicConfig(level=logging.INFO)

TOKEN = "5873310624:AAF596NEnNJJ0hTcYC0PJuJqdxb6ij7Mbj4"
MSG = "Ты как?"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=} {time.asctime()}')
    await message.reply(f"Привет, {user_name}")


@dp.message_handler(commands=['weather'])
async def get_weather(message: types.Message):
    keyboard_for_weather = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_for_weather.add("Выйти")
    await message.answer("Введите название города", reply_markup=keyboard_for_weather)

    @dp.message_handler()
    async def get_weather_2(message: types.Message):
        city = message.text
        #print(message.text)
        open_weather_token = "3e9f3ed8670f3f3b3b3c054dccb37e85"
        r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric')
        data = r.json()
        city = data["name"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        wind = data["wind"]["speed"]
        humidity = data["main"]["humidity"]
        await message.answer(f"Температура: {temp} °С\n"
                             f"Ощущается как: {feels_like} °С\n"
                             f"Ветер: {wind} м/с\n"
                             f"Влажность: {humidity} %\n"
                             "Хорошего дня)")


categories = [
  {
    "category": "Ноутбуки",
    "id": 118
  },
  {
    "category": "Ноутбуки-трансформеры",
    "id": 1224
  },
  {
    "category": "Планшеты",
    "id": 195
  },
  {
    "category": "Системные блоки",
    "id": 80
  },
  {
    "category": "Мониторы",
    "id": 101
  },
  {
    "category": "Моноблоки",
    "id": 603
  },
  {
    "category": "Материнские платы",
    "id": 5432
  },
  {
    "category": "Процессоры",
    "id": 5431
  },
  {
    "category": "Видеокарты",
    "id": 5429
  },
  {
    "category": "Жесткие диски(HDD и SSD)",
    "id": 5436
  },
  {
    "category": "Оперативная память",
    "id": 5433
  },
  {
    "category": "Блоки питания",
    "id": 5435
  },
  {
    "category": "Корпуса",
    "id": 5434
  },
  {
    "category": "Звуковые карты",
    "id": 5430
  },
  {
    "category": "Оптические приводы",
    "id": 5747
  },
  {
    "category": "Системы охлаждения",
    "id": 6127
  },
  {
    "category": "Клавиатуры для планшетов",
    "id": 360
  },
  {
    "category": "Чехлы и кейсы для планшетов",
    "id": 280
  },
  {
    "category": "Защитные стекла для планшетов",
    "id": 2088
  },
  {
    "category": "стилусы",
    "id": 3007
  },
  {
    "category": "Док-станции для планшетов",
    "id": 4827
  },
  {
    "category": "Держатели для планшетов",
    "id": 24081
  },
  {
    "category": "Зарядные устройства",
    "id": 2587
  },
  {
    "category": "Системные блоки игровые",
    "id": 3188
  },
  {
    "category": "Игровые мониторы",
    "id": 3587
  },
  {
    "category": "Кронштейны для мониторов",
    "id": 5667
  },
  {
    "category": "Электронные книги",
    "id": 73
  },
  {
    "category": "Чехлы для электронных книг",
    "id": 1081
  },
  {
    "category": "Принтеры",
    "id": 81
  },
  {
    "category": "Фотопринтеры компактные",
    "id": 2478
  },
  {
    "category": "МФУ",
    "id": 146
  },
  {
    "category": "Картриджы",
    "id": 215
  },
  {
    "category": "3D-ручки",
    "id": 6087
  },
  {
    "category": "Пластик для 3D печати",
    "id": 1253
  },
  {
    "category": "Бумага",
    "id": 2487
  },
  {
    "category": "Сканеры",
    "id": 82
  },
  {
    "category": "Ламинаторы",
    "id": 3447
  },
  {
    "category": "Шредеры",
    "id": 188
  },
  {
    "category": "Переплётчики",
    "id": 7147
  },
  {
    "category": "Резаки для бумаги",
    "id": 7148
  },
  {
    "category": "Кассовые аппараты",
    "id": 84
  },
  {
    "category": "Принтеры этикеток",
    "id": 7528
  },
  {
    "category": "Роутеры и сетевое оборудование",
    "id": 186
  },
  {
    "category": "Внешние жесткие диски и ssd",
    "id": 184
  },
  {
    "category": "Сумки для ноутбуков",
    "id": 216
  },
  {
    "category": "Мыши",
    "id": 183
  },
  {
    "category": "Клавиатуры и комплекты",
    "id": 217
  },
  {
    "category": "Компьютерные колонки",
    "id": 182
  },
  {
    "category": "Флеш-накопители",
    "id": 185
  },
  {
    "category": "Компьютерная мебель",
    "id": 1781
  },
  {
    "category": "Коврики для мыши",
    "id": 2593
  },
  {
    "category": "Подставки для ноутбуков",
    "id": 218
  },
  {
    "category": "Компьютерные наушники",
    "id": 219
  },
  {
    "category": "Веб-камеры",
    "id": 208
  },
  {
    "category": "Сетевые адаптеры для ноутбуков",
    "id": 2591
  },
  {
    "category": "Прочие компьютерные аксессуары",
    "id": 220
  },
  {
    "category": "Подключение к интернету (3G/4G)",
    "id": 71
  },
  {
    "category": "Очки для компьютера",
    "id": 354
  },
  {
    "category": "Кейсы для внешнего жесткого диска",
    "id": 1821
  },
  {
    "category": "Источники бесперебойного питания",
    "id": 2592
  },
  {
    "category": "Графические планшеты",
    "id": 287
  },
  {
    "category": "Игровые рули, джойстики и геймпады",
    "id": 285
  },
  {
    "category": "Мыши и клавиатуры Apple",
    "id": 2607
  },
  {
    "category": "Презентеры",
    "id": 3628
  },
  {
    "category": "Аккумуляторы для ноутбуков",
    "id": 6927
  },
  {
    "category": "Аксессуары для Mac",
    "id": 9227
  },
  {
    "category": "Кодовые замки для ноутбуков",
    "id": 24079
  },
  {
    "category": "Кабели и разветвители",
    "id": 27473
  },
  {
    "category": "Кабели для компьютера",
    "id": 821
  },
  {
    "category": "Микрофоны",
    "id": 236
  },
]
categories.sort(key=lambda dictionary: dictionary['category'])
list_str_for_base64 = []


@dp.message_handler(Text(equals="Выйти"))
async def exit_from_cmd_start(message: types.Message):
    await message.answer("Если понадобится, обращайся", reply_markup=types.ReplyKeyboardRemove())



filter_of_cities = []
filter_of_id_category = 0
keyboard_6 = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_6.add("Другие варианты")
keyboard_6.add("Выбрать другую категорию")
keyboard_6.add("Изменить фильтры")
keyboard_6.add("Выйти")


@dp.message_handler(commands=['pars'])
async def cmd_start(message: types.Message):
    get_city_id()
    file_cities = open('city_id.json', 'r')
    cities = json.load(file_cities)
    filter_of_cities = []
    filter_of_id_category = 0
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Выйти")
    for t in range(len(cities)):
        button_1 = cities[t]["cityNameRu"]
        keyboard.add(button_1)
    await message.answer("В каком городе вы хотите просмотреть товары?", reply_markup=keyboard)

    for i in range(len(cities)):
        @dp.message_handler(Text(equals=f'{cities[i]["cityNameRu"]}'))
        async def filter_2(message: types.Message):
            filter_of_cities.append(f'{message.text}')
            keyboard_2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for j in range(len(categories)):
                button_2 = f'{categories[j]["category"]}'
                keyboard_2.add(button_2)
            keyboard_2.add("Выйти")
            await message.answer("Выберите категорию товаров", reply_markup=keyboard_2)
            for h in range(len(categories)):
                @dp.message_handler(Text(equals=f'{categories[h]["category"]}'))
                async def filter_3(message: types.Message):
                    filter_of_id_category = 0
                    for y in range(len(categories)):
                        if categories[y]["category"] == message.text:
                            filter_of_id_category = int(categories[y]["id"])
                    get_filters(filter_of_id_category, filter_of_cities)
                    file_filters = open('filters.json', 'r')
                    filters_from_file = json.load(file_filters)
                    keyboard_3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    keyboard_3.add("Выйти")
                    keyboard_3.add("Пропустить")
                    keyboard_3.add("Назад")
                    keyboard_3.add("Фильтры выставлены")
                    for p in range(len(filters_from_file)):
                        keyboard_3.add(filters_from_file[p]["name"])
                    await message.answer("Какие фильтры выставить?", reply_markup=keyboard_3)
                    filters_from_message = []
                    for u in range(len(filters_from_file)):
                        @dp.message_handler(Text(equals=f'{filters_from_file[u]["name"]}'))
                        async def filter_4(message: types.Message):
                            keyboard_4 = types.ReplyKeyboardMarkup(resize_keyboard=True)
                            keyboard_4.add("Выйти")
                            keyboard_4.add("Назад")
                            keyboard_5 = types.ReplyKeyboardMarkup(resize_keyboard=True)
                            keyboard_5.add("Выйти")
                            keyboard_5.add("Назад")
                            index = 0
                            for b in range(len(filters_from_file)):
                                if filters_from_file[b]["name"] == message.text:
                                    string_for_base64 = "b'" + '[' + f'"{filters_from_file[b]["translitName"]}"' + "," + '""' + ","
                                    index = b
                                    filters_from_message.append(string_for_base64)
                                    for v in range(len(filters_from_file[b]["criterias"])):
                                        keyboard_4.add(filters_from_file[b]["criterias"][v]["name"])
                            keyboard_4.add("Выбрать всё")
                            if message.text != "Цена":
                                await message.answer("Выбирай)", reply_markup=keyboard_4)
                            else:
                                await message.answer("Введите диапазон цен через тире", reply_markup=keyboard_5)
                            indexs_2 = [1]

                            @dp.message_handler()
                            async def filter_5(message: types.Message):
                                count_chisla = 0
                                count_tire = 0
                                for t in range(len(message.text)):
                                    if message.text[t].isdigit() == True:
                                        count_chisla += 1
                                    if message.text[t] == "-":
                                        count_tire += 1
                                if count_chisla == len(message.text) - 1 and count_tire == 1:
                                    list_of_split_messageprice = message.text.split('-')
                                    if (len(list_of_split_messageprice) == 2) and (list_of_split_messageprice[0].isdigit() == True) and (list_of_split_messageprice[1].isdigit() == True):
                                        filters_from_message.append(f'"{message.text}"' + ",")
                                    else:
                                        await message.answer("Неверный формат ввода", reply_markup=keyboard_5)
                                else:
                                    for u in range(len(filters_from_file)):
                                        for ind in range(len(filters_from_file[u]["criterias"])):
                                            if message.text == filters_from_file[u]["criterias"][ind]["name"] and filters_from_file[u]["name"] != "Цена":
                                                if filters_from_file[u]["criterias"][ind]["translitName"] != None and filters_from_file[u]["criterias"][ind]["translitValue"] == None:
                                                    filters_from_message.append(f'"{filters_from_file[u]["criterias"][ind]["translitName"]}"' + ",")
                                                if filters_from_file[u]["criterias"][ind]["translitName"] == None and filters_from_file[u]["criterias"][ind]["translitValue"] != None:
                                                    if str(filters_from_file[u]["criterias"][ind]["translitValue"]).isdigit() != True:
                                                        filters_from_message.append(f'"{filters_from_file[u]["criterias"][ind]["translitValue"]}"' + ",")
                                                if filters_from_file[u]["criterias"][ind]["translitName"] != None and filters_from_file[u]["criterias"][ind]["translitValue"] != None:
                                                    filters_from_message.append(f'"{filters_from_file[u]["criterias"][ind]["translitName"]}-{filters_from_file[u]["criterias"][ind]["translitValue"]}"' + ",")

                                if message.text == "Назад":
                                    string_for_base64_itog = ''
                                    if len(filters_from_message) > 1:
                                        for l in range(len(filters_from_message)):
                                            string_for_base64_itog += filters_from_message[l]
                                        string_for_base64_itog = string_for_base64_itog[:-1]
                                        #print(string_for_base64_itog)
                                        if string_for_base64_itog != "b'" + '[' + f'"{filters_from_file[index]["translitName"]}"' + ',' + '""':
                                            string_for_base64_itog += "]'"
                                            list_str_for_base64.append(string_for_base64_itog[2:-1])
                                        string_for_base64_itog = ''
                                        filters_from_message.clear()
                                        #print(list_str_for_base64)
                                    else:
                                        filters_from_message.clear()
                                    await message.answer("Еще что-нибудь?", reply_markup=keyboard_3)

                                if message.text == "Фильтры выставлены":
                                    await message.answer("Сейчас поищу, это займет некоторое время", reply_markup=types.ReplyKeyboardRemove())
                                    for e in range(len(list_str_for_base64)):
                                       list_str_for_base64[e] = str(base64.b64encode(list_str_for_base64[e].encode('utf-8')))[1:]
                                    get_info_products(filter_of_id_category, filter_of_cities, list_str_for_base64)
                                    list_str_for_base64.clear()
                                    file_of_URLfilteredProducts = open("urls_products.json", 'r')
                                    URLfilterProducts = json.load(file_of_URLfilteredProducts)
                                    file_of_URLfilteredProducts.close()
                                    if len(URLfilterProducts) == 0:
                                        await message.answer("Ничего не найдено", reply_markup=keyboard_2)
                                    Urls_of_products = [URLfilterProducts[i]["URL"] for i in range(len(URLfilterProducts))]
                                    l = Urls_of_products
                                    list_split_of_url = func_chunks_generators(Urls_of_products, 4)
                                    for y in range(len(list_split_of_url[0])):
                                        await message.answer(list_split_of_url[0][y], reply_markup=keyboard_6)
                                        time.sleep(0.5)
                                if message.text == "Выбрать другую категорию":
                                    await message.answer("Выберите категорию товаров", reply_markup=keyboard_2)
                                if message.text == "Изменить фильтры":
                                    await message.answer("Какие фильтры выставить? (Предыдущие фильтры удалены)", reply_markup=keyboard_3)

                                if message.text == "Другие варианты":
                                    f = open('urls_products.json', 'r')
                                    urls = json.load(f)
                                    l_2 = func_chunks_generators([urls[i]["URL"] for i in range(len(urls))], 4)
                                    if indexs_2[-1] < len(l_2):
                                        for h in range(len(l_2[indexs_2[-1]])-1):
                                            await message.answer(l_2[indexs_2[-1]][h])
                                        await message.answer(l_2[indexs_2[-1]][-1], reply_markup=keyboard_6)
                                        indexs_2.append(indexs_2[-1] + 1)
                                    else:
                                        await message.answer("Больше ничего нет", reply_markup=keyboard_6)
                                        indexs_2.append(indexs_2[-1] + 1)


if __name__ == '__main__':
    executor.start_polling(dp)
    types.ReplyKeyboardRemove()
