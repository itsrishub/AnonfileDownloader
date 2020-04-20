from AnonHandler import bot, Var
import requests, os
from bs4 import BeautifulSoup as bs
from tempfile import NamedTemporaryFile as tf


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    wlcm_msg = '''*Yo*, *Sup Fam*?
This _bot_ is created for _fun_ and _testing_ purpose.
But it does *work* _sometimes_.

*How to use?*
*>>* `/anon <your_link>`
(*without <, > xD*) 
'''
    bot.reply_to(message, text=wlcm_msg, parse_mode='markdown')

@bot.message_handler(commands=['anon'])
def anon_handling(message):
    text = message.text
    if text.find('anonfile.com/') != -1:
        # Extracting link
        link = str(message.text).replace('/anon ', '')
        # Extracting filename and downloading it
        req = requests.get(link)
        if req.status_code == 200:
            data = bs(req.text, 'html.parser')
            download_link = data.find('a', {'id':'download-url'}).get('href')
            link_parts = download_link.split('/')
            file_name = link_parts[len(link_parts)-1]
            # First notification to the user regarding the file
            reply = f'{file_name} is under process...\n __*Please wait*__'
            temp_reply = bot.reply_to(message, text=reply, parse_mode='markdown')
            
            file_data = requests.get(download_link)
            # Creating Temp file for uploading with file name intact xD
            tmp_file = tf() 
            tmp_file.name = file_name
            tmp_file.write(file_data.content)
            tmp_file.seek(0)
            # Deleting the previous message
            bot.delete_message(message.chat.id, temp_reply.message_id)
            # Uploading the file with file name intact xD
            bot.send_document(message.chat.id, tmp_file, caption=file_name,\
                              reply_to_message_id=message.message_id)
            # Closing(Deleted automatically) the temp file
            tmp_file.close()
    else:
        bot.reply_to(message, 'Not a valid link')

bot.polling() # <= Could use timeout and other features for less load ;p or maybe not
