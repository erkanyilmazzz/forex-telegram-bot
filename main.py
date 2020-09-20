import requests
import re
import time

from telegram.ext import Updater, CommandHandler


def sent_all_companys(bot, update):
    message_str = ""
    r = requests.get('https://uzmanpara.milliyet.com.tr/canli-borsa/?Endex=XUTUM')
    words = r.text
    companys_re = "<tr class=\"zebra\" id=\"h_tr_id_[A-Z]*\" >"
    companys = re.findall(companys_re, words)
    for i in companys:
        company_name = re.findall("[A-Z][A-Z][A-Z][A-Z][A-Z]", i)
        if len(company_name) != 0:
            message_str = message_str + company_name[0] + "\n"
    message_str = message_str + "\n"
    bot.send_message(chat_id=update.message.chat_id, text=message_str)
    pass

def sent_company_info(bot, update):
    tex_message = update.message.text
    params = tex_message.split(' ')
    print(params[1])
    str = "fiyat :"+get_current_value(params[1]) + "\nyüzde "+ get_current_percent(params[1])
    bot.send_message(chat_id=update.message.chat_id, text =str)
    time.sleep(5)

    pass

def get_current_value(str_name):
    r = requests.get('https://uzmanpara.milliyet.com.tr/canli-borsa/?Endex=XUTUM')
    words = r.text
    str = str_name+'\">([0-9|,|:|-]*)<'
    findall_re = re.findall(str,words)
    return findall_re[0]

def get_current_percent(str_name):
    r = requests.get('https://uzmanpara.milliyet.com.tr/canli-borsa/?Endex=XUTUM')
    words = r.text
    str = str_name+'\">([0-9|,|:|-]*)<'
    findall_re = re.findall(str,words)
    return findall_re[1]

def get_last_time(str_name):
    r = requests.get('https://uzmanpara.milliyet.com.tr/canli-borsa/?Endex=XUTUM')
    words = r.text
    str = str_name+'\">([0-9|,|:|-]*)<'
    findall_re = re.findall(str,words)
    return findall_re[2]

def print_company_info(str_name):
    r = requests.get('https://uzmanpara.milliyet.com.tr/canli-borsa/?Endex=XUTUM')
    words = r.text
    str = str_name+'\">([0-9|,|:|-]*)<'
    findall_re = re.findall(str,words)
    print("fiyat :"+findall_re[0])
    print("yüzde :"+findall_re[1])
    print("zaman :"+findall_re[2])

def show_all_company():
    r = requests.get('https://uzmanpara.milliyet.com.tr/canli-borsa/?Endex=XUTUM')
    words = r.text
    companys_re ="<tr class=\"zebra\" id=\"h_tr_id_[A-Z]*\" >"
    companys = re.findall(companys_re,words)
    counter=0
    for i in companys:
        company_name = re.findall("[A-Z][A-Z][A-Z][A-Z][A-Z]",i)
        if len(company_name) !=0:
            print(company_name[0],end="                 ")
            counter = counter+1
            if ((counter %10) ==0):
                print()
    print()


def echo(bot, update):
    tex_message = update.message.text
    params =tex_message.split(' ')
    print(params[1])

    counter = 0
    while(1):
        str = "fiyat :"+get_current_value(params[1]) + "\nyüzde "+ get_current_percent(params[1])
        bot.send_message(chat_id=update.message.chat_id, text =str)
        time.sleep(5)
        counter += 1


def help(bot,update):
    tex_message = update.message.text

    str = "forex botuna hosgeldiniz \n"+"yapabileceginiz işlemler\n"+"1)/showCompanys\n"+"2)/showCompanyInfo [company_name]\n"
    bot.send_message(chat_id=update.message.chat_id, text =str)

    pass


def runner():
    print("hellonwrold!!")
    updater = Updater('1339682750:AAGk_PC4ihuZsmWCknUNoAhF_SfdF4rLyGQ')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('help',help))
    dp.add_handler(CommandHandler('showCompanys',sent_all_companys))
    dp.add_handler(CommandHandler('echo', echo))
    dp.add_handler(CommandHandler('showCompanyInfo', sent_company_info))

    updater.start_polling()
    updater.idle()


if __name__ =='__main__':
    runner()
