import random
import vk_api
import os.path
import os 
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

class user:
    def __init__(self,user_index):
        self.__index = str(user_index)
        self.__state = str("WAITING_START")
        self.__htype = str("NONE")
        self.__ufile = os.getcwd() + str("\\userdata\\" + (self.__index + ".hbuf"))
        if (os.path.isfile(self.__ufile)):
            self.read_save()
        else:
            self.write_save() 
    def read_save(self):
        with open(self.__ufile,"r") as user_file:
            for index, line in enumerate(user_file):
                if (index == 0):
                    self.__state = str(line.replace("\n",""))
                if (index == 1):
                    self.__htype = str(line.replace("\n",""))
        
        user_file.close()
    def write_save(self):
        with open(self.__ufile,"w") as user_file:
            user_file.write(str(self.__state) + "\n")
            user_file.write(str(self.__htype) + "\n")
        user_file.close()
    def get_state(self):
        return(self.__state)
    def set_state(self,state):
        self.__state = str(state)
        self.write_save()
    def set_htype(self,htype):
        self.__htype = str(htype)
        self.write_save()
    def get_htype(self):
        return(self.__htype)
    
def message_send(peer_id,text,attachment = None,keyboard = None):
    api_system_session.method("messages.send",{
        "random_id" : random.randint(-2147483648, +2147483648),
        "peer_id"   : peer_id,
        "message"   : text,
        "attachment": attachment,
        "keyboard"  : keyboard
    })

def user_get(user_id):
    return api_system_session.method('users.get',{'user_ids': user_id})


if __name__ == "__main__":
    api_config_token = os.getenv("VK_GROUP_TOKEN")
    api_config_group = os.getenv("VK_GROUP_ID")
    api_system_session  = vk_api.VkApi(token=api_config_token)
    api_system_longpool = VkBotLongPoll(api_system_session, api_config_group)
    for event in api_system_longpool.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            current_user = user(event.object.from_id)
            if current_user.get_state() == "WAITING_START":
                current_keyboard = VkKeyboard(one_time=True)
                current_keyboard.add_button('Овен', color=VkKeyboardColor.SECONDARY)
                current_keyboard.add_button('Телец', color=VkKeyboardColor.POSITIVE)
                current_keyboard.add_button('Близнецы', color=VkKeyboardColor.SECONDARY)
                current_keyboard.add_line()
                current_keyboard.add_button('Рак', color=VkKeyboardColor.POSITIVE)
                current_keyboard.add_button('Лев', color=VkKeyboardColor.SECONDARY)
                current_keyboard.add_button('Дева', color=VkKeyboardColor.POSITIVE)
                current_keyboard.add_line()
                current_keyboard.add_button('Весы', color=VkKeyboardColor.SECONDARY)
                current_keyboard.add_button('Скорпион', color=VkKeyboardColor.POSITIVE)
                current_keyboard.add_button('Стрелец', color=VkKeyboardColor.SECONDARY)
                current_keyboard.add_line()
                current_keyboard.add_button('Козерог', color=VkKeyboardColor.POSITIVE)
                current_keyboard.add_button('Водолей', color=VkKeyboardColor.SECONDARY)
                current_keyboard.add_button('Рыбы', color=VkKeyboardColor.POSITIVE)
                message_send(event.object.peer_id,"Привет, " + user_get(event.object.from_id)[0]["first_name"] + ", напиши свой знак по гороскопу в формате!", keyboard=current_keyboard.get_keyboard())
                current_user.set_state("WAITING_HTYPE")
            elif current_user.get_state() == "WAITING_HTYPE":
                message_text = event.object.text.lower().replace(" ","")
                allowed_list = {
                    "овен":"♈",
                    "телец":"♉",
                    "близнецы":"♊",
                    "рак":"♋",
                    "лев":"♌",
                    "дева":"♍",
                    "весы":"♎",
                    "скорпион":"♏",
                    "стрелец":"♐",
                    "козерог":"♑",
                    "водолей":"♒",
                    "рыбы":"♓"
                }
                translated_list = {
                    "овен":"aries",
                    "телец":"taurus",
                    "близнецы":"gemini",
                    "рак":"cancer",
                    "лев":"leo",
                    "дева":"virgo",
                    "весы":"libra",
                    "скорпион":"scorpio", 
                    "стрелец":"sagittarius",
                    "козерог":"capricorn",
                    "водолей":"aquarius",
                    "рыбы":"pisces"
                }
                if (message_text in allowed_list):
                    current_keyboard = VkKeyboard(one_time=True)
                    current_keyboard.add_button('Гороскоп на день', color=VkKeyboardColor.SECONDARY)
                    current_keyboard.add_line()
                    current_keyboard.add_button('Гороскоп на неделю', color=VkKeyboardColor.POSITIVE)
                    current_keyboard.add_line()
                    current_keyboard.add_button('Сменить знак', color=VkKeyboardColor.SECONDARY)
                    current_keyboard.add_line()
                    current_keyboard.add_button('Доп.Информация', color=VkKeyboardColor.POSITIVE)
                    message_send(event.object.peer_id, user_get(event.object.from_id)[0]["first_name"] + " ты выбрал(а) знак по гороскопу - " + message_text + allowed_list[message_text],keyboard=current_keyboard.get_keyboard())
                    current_user.set_htype(translated_list[message_text])
                    current_user.set_state("WAITING_CONTINUE")
                else:
                    current_keyboard = VkKeyboard(one_time=True)
                    current_keyboard.add_button('Овен', color=VkKeyboardColor.SECONDARY)
                    current_keyboard.add_button('Телец', color=VkKeyboardColor.POSITIVE)
                    current_keyboard.add_button('Близнецы', color=VkKeyboardColor.SECONDARY)
                    current_keyboard.add_line()
                    current_keyboard.add_button('Рак', color=VkKeyboardColor.POSITIVE)
                    current_keyboard.add_button('Лев', color=VkKeyboardColor.SECONDARY)
                    current_keyboard.add_button('Дева', color=VkKeyboardColor.POSITIVE)
                    current_keyboard.add_line()
                    current_keyboard.add_button('Весы', color=VkKeyboardColor.SECONDARY)
                    current_keyboard.add_button('Скорпион', color=VkKeyboardColor.POSITIVE)
                    current_keyboard.add_button('Стрелец', color=VkKeyboardColor.SECONDARY)
                    current_keyboard.add_line()
                    current_keyboard.add_button('Козерог', color=VkKeyboardColor.POSITIVE)
                    current_keyboard.add_button('Водолей', color=VkKeyboardColor.SECONDARY)
                    current_keyboard.add_button('Рыбы', color=VkKeyboardColor.POSITIVE)
                    message_send(event.object.peer_id, "Извини, но я не нашел такой знак!",keyboard=current_keyboard.get_keyboard())
            elif current_user.get_state() == "WAITING_CONTINUE":
                message_text = event.object.text.lower()
                if message_text == "гороскоп на день" or message_text == "гороскоп на неделю" or message_text == "сменить знак" or message_text == "доп.информация": 
                    if message_text == "гороскоп на день":
                        current_keyboard = VkKeyboard(one_time=True)
                        current_keyboard.add_button('Общий гороскоп', color=VkKeyboardColor.SECONDARY)
                        current_keyboard.add_button('Эротический гороскоп', color=VkKeyboardColor.POSITIVE)
                        current_keyboard.add_line()
                        current_keyboard.add_button('Антигороскоп', color=VkKeyboardColor.SECONDARY)
                        current_keyboard.add_button('Бизнес-гороскоп', color=VkKeyboardColor.POSITIVE)
                        current_keyboard.add_line()
                        current_keyboard.add_button('Гороскоп здоровья', color=VkKeyboardColor.SECONDARY)
                        current_keyboard.add_button('Кулинарный гороскоп', color=VkKeyboardColor.POSITIVE)
                        current_keyboard.add_line()
                        current_keyboard.add_button('Любовный гороскоп', color=VkKeyboardColor.SECONDARY)
                        current_keyboard.add_button('Мобильный гороскоп', color=VkKeyboardColor.POSITIVE)
                        reply_text = "Выбери желаемый гороскоп из списка:\n[1]Общий гороскоп,\n[2]Эротический гороскоп,\n[3]Антигороскоп,\n[4]Бизнес-гороскоп,\n[5]Гороскоп здоровья,\n[6]Кулинарный гороскоп,\n[7]Любовный гороскоп,\n[8]Мобильный гороскоп"
                        message_send(event.object.peer_id, reply_text, keyboard=current_keyboard.get_keyboard())
                        current_user.set_state("WAITING_TYPE_DAILY")
                    elif message_text == "гороскоп на неделю":
                        current_keyboard = VkKeyboard(one_time=True)
                        current_keyboard.add_button('Общий гороскоп', color=VkKeyboardColor.SECONDARY)
                        current_keyboard.add_button('Бизнес-гороскоп', color=VkKeyboardColor.POSITIVE)
                        current_keyboard.add_line()
                        current_keyboard.add_button('Гороскоп "Семья, любовь"', color=VkKeyboardColor.SECONDARY)
                        current_keyboard.add_button('Автомобильный гороскоп', color=VkKeyboardColor.POSITIVE)
                        current_keyboard.add_line()
                        current_keyboard.add_button('Гороскоп здоровья', color=VkKeyboardColor.SECONDARY)
                        current_keyboard.add_button('Шоппинг-гороскоп', color=VkKeyboardColor.POSITIVE)
                        current_keyboard.add_line()
                        current_keyboard.add_button('Гороскоп красоты', color=VkKeyboardColor.SECONDARY)
                        current_keyboard.add_button('Эротический гороскоп', color=VkKeyboardColor.POSITIVE)
                        current_keyboard.add_line()
                        current_keyboard.add_button('Ювелирный гороскоп', color=VkKeyboardColor.SECONDARY)
                        reply_text = 'Выбери желаемый гороскоп из списка:\n🌍Общий гороскоп,\n👔Бизнес-гороскоп,\n❤Гороскоп "Семья, любовь",\n🚙Автомобильный гороскоп,\n⚽Гороскоп здоровья,\n💰Шоппинг-гороскоп,\n💄Гороскоп красоты,\n💋Эротический гороскоп,\n💎Ювелирный гороскоп'
                        message_send(event.object.peer_id, reply_text, keyboard=current_keyboard.get_keyboard())
                        current_user.set_state("WAITING_TYPE_WEEKLY")
                    elif message_text == "сменить знак": 
                        current_keyboard = VkKeyboard(one_time=True)
                        current_keyboard.add_button('Овен', color=VkKeyboardColor.SECONDARY)
                        current_keyboard.add_button('Телец', color=VkKeyboardColor.POSITIVE)
                        current_keyboard.add_button('Близнецы', color=VkKeyboardColor.SECONDARY)
                        current_keyboard.add_line()
                        current_keyboard.add_button('Рак', color=VkKeyboardColor.POSITIVE)
                        current_keyboard.add_button('Лев', color=VkKeyboardColor.SECONDARY)
                        current_keyboard.add_button('Дева', color=VkKeyboardColor.POSITIVE)
                        current_keyboard.add_line()
                        current_keyboard.add_button('Весы', color=VkKeyboardColor.SECONDARY)
                        current_keyboard.add_button('Скорпион', color=VkKeyboardColor.POSITIVE)
                        current_keyboard.add_button('Стрелец', color=VkKeyboardColor.SECONDARY)
                        current_keyboard.add_line()
                        current_keyboard.add_button('Козерог', color=VkKeyboardColor.POSITIVE)
                        current_keyboard.add_button('Водолей', color=VkKeyboardColor.SECONDARY)
                        current_keyboard.add_button('Рыбы', color=VkKeyboardColor.POSITIVE)
                        message_send(event.object.peer_id,user_get(event.object.from_id)[0]["first_name"] + ", напиши свой знак по гороскопу!", keyboard=current_keyboard.get_keyboard())
                        current_user.set_state("WAITING_HTYPE")
                    elif message_text == "доп.информация":
                        current_keyboard = VkKeyboard(one_time=True)
                        current_keyboard.add_button('Гороскоп на день', color=VkKeyboardColor.SECONDARY)
                        current_keyboard.add_line()
                        current_keyboard.add_button('Гороскоп на неделю', color=VkKeyboardColor.POSITIVE)
                        current_keyboard.add_line()
                        current_keyboard.add_button('Сменить знак', color=VkKeyboardColor.SECONDARY)
                        current_keyboard.add_line()
                        current_keyboard.add_button('Доп.Информация', color=VkKeyboardColor.POSITIVE)
                        message_send(event.object.peer_id, "Автор: Кирилл Жосул(vk.com/kirillzhosul),\nВерсия: 1.0\nИспользуется API сайта https://ignio.com", keyboard=current_keyboard.get_keyboard())
                else:
                    current_keyboard = VkKeyboard(one_time=True)
                    current_keyboard.add_button('Гороскоп на день', color=VkKeyboardColor.SECONDARY)
                    current_keyboard.add_line()
                    current_keyboard.add_button('Гороскоп на неделю', color=VkKeyboardColor.POSITIVE)
                    current_keyboard.add_line()
                    current_keyboard.add_button('Сменить знак', color=VkKeyboardColor.SECONDARY)
                    current_keyboard.add_line()
                    current_keyboard.add_button('Доп.Информация', color=VkKeyboardColor.POSITIVE)
                    message_send(event.object.peer_id, "Не понял вас!", keyboard=current_keyboard.get_keyboard())
            elif current_user.get_state() == "WAITING_TYPE_DAILY" or current_user.get_state() == "WAITING_TYPE_WEEKLY":
                message_text = event.object.text.lower()
                if current_user.get_state() == "WAITING_TYPE_DAILY":
                    allowed_types = ["общий гороскоп","эротический гороскоп","антигороскоп","бизнес-гороскоп","гороскоп здоровья","кулинарный гороскоп","любовный гороскоп","мобильный гороскоп"]
                elif current_user.get_state() == "WAITING_TYPE_WEEKLY":
                    allowed_types = ["общий гороскоп","бизнес-гороскоп",'гороскоп "семья, любовь"',"автомобильный гороскоп","гороскоп здоровья","шоппинг-гороскоп","гороскоп красоты","ювелирный гороскоп","эротический гороскоп"]
                current_keyboard = VkKeyboard(one_time=True)
                current_keyboard.add_button('Гороскоп на день', color=VkKeyboardColor.SECONDARY)
                current_keyboard.add_line()
                current_keyboard.add_button('Гороскоп на неделю', color=VkKeyboardColor.POSITIVE)
                current_keyboard.add_line()
                current_keyboard.add_button('Сменить знак', color=VkKeyboardColor.SECONDARY)
                current_keyboard.add_line()
                current_keyboard.add_button('Доп.Информация', color=VkKeyboardColor.SECONDARY)
                if message_text in allowed_types:
                    if current_user.get_state() == "WAITING_TYPE_DAILY":
                        urls = {
                            allowed_types[0]: "https://ignio.com/r/export/win/xml/daily/com.xml",
                            allowed_types[1]: "https://ignio.com/r/export/win/xml/daily/ero.xml",
                            allowed_types[2]: "https://ignio.com/r/export/win/xml/daily/anti.xml",
                            allowed_types[3]: "https://ignio.com/r/export/win/xml/daily/bus.xml",
                            allowed_types[4]: "https://ignio.com/r/export/win/xml/daily/hea.xml",
                            allowed_types[5]: "https://ignio.com/r/export/win/xml/daily/cook.xml",
                            allowed_types[6]: "https://ignio.com/r/export/win/xml/daily/lov.xml",
                            allowed_types[7]: "https://ignio.com/r/export/win/xml/daily/mob.xml",
                        }
                        data = urlopen(urls[message_text])
                        parsed_data = ET.fromstring(data.read())
                        text = parsed_data.find(current_user.get_htype()).find("today").text
                        reply_text = "Гороскоп на сегодня:" + text
                        photo = random.choice(["photo-199977164_457239019","photo-199977164_457239020","photo-199977164_457239021","photo-199977164_457239022"])
                        message_send(event.object.peer_id, reply_text,attachment=photo,keyboard=current_keyboard.get_keyboard())
                    elif current_user.get_state() == "WAITING_TYPE_WEEKLY":
                        real_types = {
                            "общий гороскоп": "common",
                            "бизнес-гороскоп": "business",
                            'гороскоп "семья, любовь"': "love",
                            "автомобильный гороскоп": "car",
                            "гороскоп здоровья": "health",
                            "шоппинг-гороскоп": "shop",
                            "гороскоп красоты": "beauty",
                            "эротический гороскоп": "erotic",
                            "ювелирный гороскоп": "gold",
                        }
                        urls = {
                            "all":"https://ignio.com/r/export/utf/xml/weekly/cur.xml"
                        }
                        data = urlopen(urls["all"])
                        parsed_data = ET.fromstring(data.read())
                        date = parsed_data.find("date").get("weekly")
                        text = parsed_data.find(current_user.get_htype()).find(real_types[message_text]).text
                        reply_text = date + ":" + text
                        photo = random.choice(["photo-199977164_457239019","photo-199977164_457239020","photo-199977164_457239021","photo-199977164_457239022"])
                        message_send(event.object.peer_id, reply_text ,attachment=photo,keyboard=current_keyboard.get_keyboard())
                else:
                    
                    message_send(event.object.peer_id, user_get(event.object.from_id)[0]["first_name"] + ", я не нашел такого вида гороскопа😥!", keyboard=current_keyboard.get_keyboard())
                current_user.set_state("WAITING_CONTINUE")