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

#Steganography.generate_key("")

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
        #button.background_normal = 'widgets/neon_batton.png'
        if button.background_normal == 'widgets/gray_button.png':
            button.background_normal = 'widgets/neon_batton.png'

        elif button.background_normal == 'widgets/neon_batton.png':
            button.background_normal = 'widgets/gray_button.png'



class MainEncryptWindow(Screen):
    picture_path = ObjectProperty(None)
    text = ObjectProperty(None)
    pasword = ObjectProperty(None)



class MainDecryptWindow(Screen):
    pass


class PaswordListWindow(Screen):
    def add_pasword_in_grid(self):
        print('+')
        #password_grid = ObjectProperty(None)
        #new_pasword = Label(text='hello')
        #password_grid.add_widget(new_pasword)

    def on_enter(self):
        print('+')


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


        encrypted_image = Steganography.encrypt("key.key", "input.png", "message.txt")
        encrypted_image.save("images/output.png")
        print("Шифрую")

        decrypted_text = Steganography.decrypt("key.key", "images/output.png")
        print(decrypted_text)
        print("Расшифорвываю")

        #PaswordListWindow.add_pasword_in_grid(PaswordListWindow.self)




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