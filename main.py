import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config
from kivy.core.window import Window
from steganocryptopy.steganography import Steganography
import base64
from kivy.clock import Clock


class encryption():
    def encrypted(self):
        encrypted_image = Steganography.encrypt("key.key", "input.png", "message.txt")
        encrypted_image.save("images/output.png")
        print("Шифрую")
        #self.name.text = ""
        #self.email.text = ""

    def decrypted(self):
        decrypted_text = Steganography.decrypt("key.key", "images/output.png")
        print(decrypted_text)
        print("Расшифорвываю")
        #self.message.text = decrypted_text



class AuthorizationWindow(Screen):
    def graphic_key(self,button):
        gk = open('key.key', 'r+')
        #print(str(button), file=gk)
        #print(gk.readline())

        if gk.readline()== '':
            Steganography.generate_key("key.key")
            gk.writelines(['button_1 /n','button_2','button_3','button_4','button_5'])
        col = 0
        for i in gk:
            col += 1
        gk.close
        #print(col)
        if col < 16:
            if button.background_normal == 'widgets/gray_button.png':
                button.background_normal = 'widgets/neon_batton.png'
                gk = open('key.key', 'r+')
                gk.seek(0,3)
                gk.write('+')
                #print('+',file=gk)
                gk.close()
                #for i in gk:
                    #print(i)
                    #print(button.name)
                    #if i == button.name:
                    #    print('+++')

            elif button.background_normal == 'widgets/neon_batton.png':
                button.background_normal = 'widgets/gray_button.png'
        else:
            gk.close()
            print('gk=что-то')


class MainEncryptWindow(Screen):
    picture_path = ObjectProperty(None)
    text = ObjectProperty(None)
    pasword = ObjectProperty(None)


    #def on_enter(self, *args):
    #    print('on_enter')
    #    Clock.schedule_once(self.regenerate_pasword,5)


    def regenerate_pasword(self,*args):
        #print('+')
        Steganography.generate_key('temporary_password.key')
        p=open('temporary_password.key', 'r+')
        self.pasword.text = p.readline()
        #p.write('')
        #print(self.pasword.text)
        p.close()

    def encrypted(self):
        m=open('message.txt', 'w')
        m.write(self.text.text)
        m.close()

        encrypted_image = Steganography.encrypt('temporary_password.key', self.picture_path.text, 'message.txt')
        encrypted_image.save("images/output.png")
        print("Шифрую")

        m = open('message.txt', 'w')
        m.write('')
        m.close()

        p = open('temporary_password.key', 'w')
        p.write('')
        p.close()


class MainDecryptWindow(Screen):
    picture_path = ObjectProperty(None)
    pasword = ObjectProperty(None)
    text = ObjectProperty(None)

    def decrypted(self):
        p=open('temporary_password.key', 'w')
        p.write(self.pasword.text)
        p.close()
        decrypted_text = Steganography.decrypt("temporary_password.key", self.picture_path.text)
        self.text.text=decrypted_text
        print("Расшифорвываю!")
        p = open('temporary_password.key', 'w')
        p.write('')
        p.close()


class PaswordListWindow(Screen):
    password_grid = ObjectProperty(None)
    picture_path = ObjectProperty(None)
    website_address = ObjectProperty(None)
    login = ObjectProperty(None)
    pasword = ObjectProperty(None)


    def on_enter(self):
        Clock.schedule_once(self.add_pasword_in_grid)


    def add_pasword_in_grid(self,*args):
        self.password_grid.clear_widgets()
        print('add pasword in grid')
        p = open('pasword_list.txt', 'r+')
        while p.readline() != '':
            new_pasword = Label(text=p.readline())
            self.password_grid.add_widget(new_pasword)
            new_pasword_2 = Label(text=p.readline())
            self.password_grid.add_widget(new_pasword_2)
        p.close()


class SettingsWindow(Screen):
    pass


class AddPaswordWindow(Screen):
    picture_path = ObjectProperty(None)
    website_address = ObjectProperty(None)
    login = ObjectProperty(None)
    pasword = ObjectProperty(None)

    def add_pasword(self):
        print(self.picture_path.text)
        print(self.website_address.text)
        print(self.login.text)
        print(self.pasword.text)

        p = open('pasword_list.txt', 'r+')
        print(p.readlines())
        L=p.readlines()
        for i in L:
            print(i, file=p)
        print('', file=p)
        print(self.website_address.text, file=p)
        print(self.picture_path.text, file=p)
        p.close()


        m=open('message.txt', 'w')
        m.write(self.login.text)
        m.write(self.pasword.text)
        m.close()

        encrypted_image = Steganography.encrypt('key.key', self.picture_path.text, 'message.txt')
        encrypted_image.save("images/output.png")
        print("Шифрую")

        m = open('message.txt', 'w')
        m.write('')
        m.close()

        #PaswordListWindow.add_pasword_in_grid()




class WindowManager(ScreenManager):
    pass




kv=Builder.load_file('my.kv')

#name = ObjectProperty(None)
#message = ObjectProperty(None)



class MyApp(App):
    def build(self):
        Window.size = (290, 585)
        return kv


if __name__ == "__main__":
    MyApp().run()