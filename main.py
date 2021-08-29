from kivy.utils import platform
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView

from kivy.properties import ObjectProperty

from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.metrics import dp
import os
from kivy.core.window import Window
from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'not allowed')
Config.write()

if platform == 'android':
    from android.storage import primary_external_storage_path
    dir = primary_external_storage_path()
    download_dir_path = os.path.join(dir, 'Download')

# мой классы работы с базой данных, с файлом текст словарем покупок


class Baze_write():
    def __init__(self, **kw):
        super(Baze_write, self).__init__(**kw)

    # Берем данные из ОБЩЕЙ базы словаря покупок
    def list_goods_open(self):
        file = open("allgoods.txt")
        a = file.read()
        a = a.split(',')
        # print(a)
        a.sort()
        if '' in a:
            a.remove('')
        print('Общая база товаров')
        print(a)
        return a

    # Берем данные из базы покупки СЕЙЧАС
    def list_goodsBuyNow_open(self):
        file = open("goodsbuynow.txt")
        a = file.read()
        a = a.split(',')
        # print(a)
        a.sort()
        if '' in a:
            a.remove('')
        print('Текущие покупки товаров')
        print(a)
        return a

    # добавить товар в ОБЩУЮ базу словарь и со старта создать словарь
    def listgoods_add(self, goods_item):
        file = open("allgoods.txt", 'a')
        # item = input('what?:')
        file.write(goods_item + ',')
        file.close()
        file = open("allgoods.txt")
        a = file.read()
        a = a.split(',')
        a.sort()
        print('Общая база товаров')
        print(a)
        return a

    # Добавить товар в базу buynow ТЕКУЩИЕ покупки и со старта создать buynow
    def listgoods_nowbuy(self, goods_item):
        file = open("goodsbuynow.txt", 'a')
        file.write(goods_item + ',')
        file.close()
        file = open("goodsbuynow.txt")
        a = file.read()
        a = a.split(',')
        a.sort()
        print('Текущие покупки товаров')
        print(a)
        return a

    # Удаление элемента из общей базы
    def listgoods_del_value(self, goods_item):
        file = open("allgoods.txt", 'r')
        a = file.read()
        a = a.split(',')
        a.remove(goods_item)
        file = open("allgoods.txt", 'w')
        for a1 in a:
            if a1 == '':
                continue
            else:
                file.write(a1 + ',')
        file.close()
        file = open("allgoods.txt")
        a = file.read()
        a = a.split(',')
        a.sort()
        if '' in a:
            a.remove('')
        print('Общая база товаров')
        print(a)
        return a

    # удаление элемента из ТЕКУЩЕЙ базы покупок купить сейчас
    def list_goodsBuyNow_del_value(self, goods_item):
        file = open("goodsbuynow.txt", 'r')
        a = file.read()
        a = a.split(',')
        a.remove(goods_item)
        file = open("goodsbuynow.txt", 'w')
        for a1 in a:
            if a1 == '':
                continue
            else:
                file.write(a1 + ',')
        file.close()
        file = open("allgoods.txt")
        a = file.read()
        a = a.split(',')
        a.sort()
        if '' in a:
            a.remove('')
        print('Текущие покупки товаров')
        print(a)
        return a

    # очистить полностью словарь всех товаров!!!
    def listgoods_сlear(self):
        open('allgoods.txt', 'w').close()


class ScreenManagement(ScreenManager):
    def __init__(self, **kw):
        super(ScreenManagement, self).__init__(**kw)

    goods_input = ObjectProperty()
    last_add_goods = ObjectProperty()
    password_del_baze = ObjectProperty()
    inf_lbl_del_baze = ObjectProperty()
    goods_buy_now_list = ObjectProperty()
    goods_list_plus = ObjectProperty()
    zzzzzz = ObjectProperty()

    def goods_list_plus_update(self):
        self.dict = {}
        # при входе на экран обнояляет список товаров
        self.z = Baze_write()
        self.z = self.z.list_goods_open()
        # в цикле добовляет лейблы товара и кнопку делейт
        for i in self.z:
            self.lbl = Label(text=str(i), font_size='50dp',
                             size_hint_y=None, height=90, color=[.19, .19, .19, 1])
            self.lbl.id = str(i)

            self.btn = Button(text='+', size_hint_x=.3, size_hint_y=None, height=90,
                              on_press=self.get_id_btn)
            self.dict[self.btn] = self.lbl.id

            self.goods_list_plus.add_widget(self.lbl)
            self.goods_list_plus.add_widget(self.btn)

    def get_id_btn(self, instance):
        self.z = Baze_write()
        self.z.listgoods_del_value(str(self.dict[instance]))
        self.c = str(self.dict[instance])
        self.zzzzzz.clear_widgets()
        self.update_list_goods_base()
        self.last_add_goods.color = .80, 0, 0, 1
        self.last_add_goods.text = ('Удалено: ' + self.c)

    # добавление товара в базу при нажатии кнопки Добавить товар

    def buttonClicked(self):
        if self.goods_input.text == '':
            self.last_add_goods.background_normal = ''
            self.last_add_goods.color = .80, 0, 0, 1
            self.last_add_goods.text = 'Добавьте товар !!!'
        else:
            self.last_add_goods.color = .17, .4, .68, 1
            self.new_goods = self.goods_input.text
            self.last_add_goods.text = 'Последнее добавлено: ' + self.goods_input.text
            self.goods_input.text = ''
            self.new_goods_add = Baze_write()
            self.new_goods_add.listgoods_add(self.new_goods)
            self.zzzzzz.clear_widgets()
            self.update_list_goods_base()

    def clear_btn_all_goods(self):
        if self.password_del_baze.text == '1234':
            self.clear_baze = Baze_write()
            self.clear_baze.listgoods_сlear()
            self.inf_lbl_del_baze.text = 'База удалена!!!'
            self.password_del_baze.text = ''
            self.clear_baze.list_goods_open()
        else:
            self.inf_lbl_del_baze.text = 'Введите правильный пароль'
            self.password_del_baze.text = ''

    # функция обновления отражения списка товаров на скрине

    def update_list_goods_base(self):
        self.dict = {}
        # при входе на экран BaseGoodsAdd(Screen) обнояляет список товаров
        self.z = Baze_write()
        self.z = self.z.list_goods_open()
        # в цикле добовляет лейблы товара и кнопку делейт
        for i in self.z:
            self.lbl = Label(text=str(i), font_size='50dp',
                             size_hint_y=None, height=90, color=[.19, .19, .19, 1])
            self.lbl.id = str(i)

            self.btn = Button(text='Del', size_hint_x=.3, size_hint_y=None, height=90,
                              on_press=self.get_id_btn)
            # наполняет словарь
            self.dict[self.btn] = self.lbl.id

            self.zzzzzz.add_widget(self.lbl)
            self.zzzzzz.add_widget(self.btn)


class Mainscreen(Screen):

    pass

# єкран текущие покупки


class ListGoodsBuyNow(Screen):

    def on_enter(self):
        self.updaite_goods_buy_now_list()

    def updaite_goods_buy_now_list(self):
        self.dict = {}
        # при входе на экран обнояляет список товаров
        self.z = Baze_write()
        self.z = self.z.list_goodsBuyNow_open()
        # в цикле добовляет лейблы товара и кнопку делейт
        for i in self.z:
            self.lbl = Label(text=str(i), font_size='50dp',
                             size_hint_y=None, height=90, color=[.19, .19, .19, 1])
            self.lbl.id = str(i)

            self.btn = Button(text='Del', size_hint_x=.3, size_hint_y=None, height=90,
                              on_press=self.get_id_del_nowbuy)
            # наполняет словарь
            self.dict[self.btn] = self.lbl.id

            self.goods_buy_now_list.add_widget(self.lbl)
            self.goods_buy_now_list.add_widget(self.btn)

    def get_id_del_nowbuy(self, instance):
        self.z = Baze_write()
        self.z.list_goodsBuyNow_del_value(str(self.dict[instance]))
        print(self.dict[instance])
        self.goods_buy_now_list.clear_widgets()
        self.updaite_goods_buy_now_list()

    def on_leave(self):
        self.goods_buy_now_list.clear_widgets()


# добавить в лист текущих покупок
class AddGoodsBuyNow(Screen):

    def on_enter(self):
        self.dict = {}
        # при входе на экран обнояляет список товаров
        self.z = Baze_write()
        self.z = self.z.list_goods_open()
        # в цикле добовляет лейблы товара и кнопку делейт
        for i in self.z:
            self.lbl = Label(text=str(i), font_size='50dp',
                             size_hint_y=None, height=90, color=[.19, .19, .19, 1])
            self.lbl.id = str(i)

            self.btn = Button(text='+', size_hint_x=.3, size_hint_y=None, height=90,
                              on_press=self.get_id_nowbuy)
            # наполняет словарь
            self.dict[self.btn] = self.lbl.id

            self.goods_list_plus.add_widget(self.lbl)
            self.goods_list_plus.add_widget(self.btn)

    def get_id_nowbuy(self, instance):
        self.z = Baze_write()
        self.z.listgoods_nowbuy(str(self.dict[instance]))
        self.z.list_goodsBuyNow_open()

    def on_leave(self):
        self.goods_list_plus.clear_widgets()

# экран добовления товаров в базу


class BaseGoodsAdd(Screen):
    def __init__(self, **kw):
        super(BaseGoodsAdd, self).__init__(**kw)

    # при входе на экран добовления товара в общую базу
    def on_enter(self):
        self.update_list_goods_base()

    def update_list_goods_base(self):
        self.dict = {}
        # при входе на экран BaseGoodsAdd(Screen) обнояляет список товаров
        self.z = Baze_write()
        self.z = self.z.list_goods_open()
        # в цикле добовляет лейблы товара и кнопку делейт
        for i in self.z:
            self.lbl = Label(text=str(i), font_size='50dp', bold=True,
                             size_hint_y=None, height=90, color=[.19, .19, .19, 1])
            self.lbl.id = str(i)

            self.btn = Button(text='Del', bold=True, size_hint_x=.3, size_hint_y=None, height=90, font_size='30dp',
                              on_press=self.get_id_btn)
            # наполняет словарь
            self.dict[self.btn] = self.lbl.id

            self.zzzzzz.add_widget(self.lbl)
            self.zzzzzz.add_widget(self.btn)

    # удаление товара из общей базы
    def get_id_btn(self, instance):
        self.c = str(self.dict[instance])

        self.z = Baze_write()
        self.z.listgoods_del_value(str(self.dict[instance]))
        self.zzzzzz.clear_widgets()
        self.update_list_goods_base()
        self.last_add_goods.color = .80, 0, 0, 1
        self.last_add_goods.text = ('Удалено : ' + self.c)

    # при выходе с экрана BaseGoodsAdd(Screen) очистка виджетов
    def on_leave(self):
        self.zzzzzz.clear_widgets()


class BaseClearAll(Screen):
    pass


class Password(Screen):
    pass


class MyGoodsApp(App):
    def build(self):

        return ScreenManagement()


if __name__ == '__main__':
    MyGoodsApp().run()
