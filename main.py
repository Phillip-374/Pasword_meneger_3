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
from kivy.uix.image import Image



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
    picture_path=str()
    website_address=str()

    def on_enter(self):
        Clock.schedule_once(self.add_pasword_in_grid)


    def add_pasword_in_grid(self,*args):
        self.password_grid.clear_widgets()
        print('add pasword in grid')
        p = open('pasword_list.txt', 'r+')
        while p.readline() != '':
            layout = GridLayout(cols=2,size_hint=(1, None), height=70)
            self.password_grid.add_widget(layout)
            picture_path_text=p.readline()[:-1]
            picture = Image(source=picture_path_text, size_hint=(None, 1), width=100)
            #(background_normal=p.readline()[:-1], size_hint=[0.5,0.3])
            layout.add_widget(picture)
            website_address = Button(text=p.readline()[:-1], background_color=[0,0,0,0], name=picture_path_text)
            layout.add_widget(website_address)
            #Pasword_1 = PaswordDecryptWindow()
            #website_address.bind(on_press=Pasword_1.viewing_password)
            website_address.bind(on_press=self.go_pasword_decrypt)

        p.close()


        #while p.readline() != '':
        #    picture = Button(background_normal=p.readline()[:-1],size_hint=(None,None), height=100)
        #    #(background_normal=p.readline()[:-1], size_hint=[0.5,0.3])
        #    self.password_grid.add_widget(picture)
        #    website_address = Button(text=p.readline(),size_hint=(None,None), height=100)
        #    self.password_grid.add_widget(website_address)
        #p.close()


    def go_pasword_decrypt(self,pasword):
        PaswordListWindow.picture_path = pasword.name
        PaswordListWindow.website_address = pasword.text
        self.manager.current = "pasword_decrypt"

        #Da=PaswordDecryptWindow()
        #Da.viewing_password(source=pasword.name)
        #PaswordDecryptWindow.picture.source=pasword.name
        #print(self.password_grid.layout)





class SettingsWindow(Screen):
    pass


class AddPaswordWindow(Screen):
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
        print("images/"+self.website_address.text+".png", file=p)
        print(self.website_address.text, file=p)
        p.close()


        m=open('message.txt', 'w')
        m.write(self.login.text)
        m.write('*-/n-*')
        m.write(self.pasword.text)
        m.close()

        encrypted_image = Steganography.encrypt('key.key', self.picture_path.text, 'message.txt')

        encrypted_image.save("images/"+self.website_address.text+".png")
        print("Шифрую")

        m = open('message.txt', 'w')
        m.write('')
        m.close()

        #PaswordListWindow.add_pasword_in_grid()



class PaswordDecryptWindow(Screen):

    picture = ObjectProperty(None)
    website_address = ObjectProperty(None)
    login = ObjectProperty(None)
    pasword = ObjectProperty(None)


    def on_enter(self):
        Clock.schedule_once(self.drawing_image)


    def drawing_image(self,*args):
        print("viewing_password")
        #print(PaswordListWindow.picture_path)
        #print(PaswordListWindow.website_address)
        self.picture.source=PaswordListWindow.picture_path
        self.website_address.text=PaswordListWindow.website_address
        self.login.text=''
        self.pasword.text =''
        #picture = Image(source=PaswordListWindow.picture_path, pos_hint={'x':0.1,'y':0.62})
        #PaswordDecryptWindow.add_widget(picture)


    def show_password(self):

        decrypted_text = Steganography.decrypt("key.key", PaswordListWindow.picture_path)
        login_pasword=decrypted_text.split('*-/n-*')
        self.login.text=login_pasword[0]
        self.pasword.text=login_pasword[1]
        print("Расшифорвывал")



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