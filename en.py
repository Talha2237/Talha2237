from kivy.app import App 
 from kivy.lang import Builder 
 from kivy.base import EventLoop 
 from kivy.core.window import Window 
 from kivy.core.clipboard import Clipboard 
 from kivy.uix.popup import Popup 
 from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition 
 from cryptography.fernet import Fernet 
 import json 
 import os 
  
  
 Builder.load_string(""" 
 <EncryptWindow> 
     GridLayout: 
         size: root.width, root.height 
         canvas.before: 
             Rectangle: 
                 pos: self.pos 
                 size: self.size 
                 source: 'bg.jpg' 
         Label: 
             text: '[b]Enter Message[/b]' 
             markup: True 
             font_size: 40 
             size: 50, 50 
             pos: root.width / 2 - 25, root.height - 90 
         TextInput: 
             id: input 
             canvas.before: 
                 Color: 
                     rgba: 1, 1, 1, 1 
                 Line: 
                     width: 1.5 
                     rectangle: 50, root.height / 2, root.width - 100, (root.height / 2) - 120 
             font_size: 40 
             size: root.width - 100, (root.height / 2) - 120 
             pos: 50, root.height / 2 
             background_color: 0, 0, 0, 0 
             selection_color: 1, 1, 1, 0.4 
             cursor_color: 1, 1, 1, 1 
         Button: 
             canvas.before: 
                 Color: 
                     rgba: 1, 1, 1, 1 
                 Line: 
                     width: 1.5 
                     rectangle: 50, root.height / 2 - 80, (root.width - 100) / 3 - 50, 60 
             text: 'Encrypt' 
             font_size: 35 
             size: (root.width - 100) / 3 - 50, 60 
             pos: 50, root.height / 2 - 80 
             background_normal: 'w.png' 
             background_down: 'b.png' 
             background_color: 1, 1, 1, 0.2 
             on_release: root.encrypt() 
         Spinner: 
             id: key 
             canvas.before: 
                 Color: 
                     rgba: 1, 1, 1, 1 
                 Line: 
                     width: 1.5 
                     rectangle: root.width / 2 - ((root.width - 100) / 6) - 30, root.height / 2 - 80, (root.width - 100) / 3 + 60, 60 
             text: 'Choose Key' 
             font_size: 35 
             size: (root.width - 100) / 3 + 60, 60 
             pos: root.width / 2 - ((root.width - 100) / 6) - 30, root.height / 2 - 80 
             background_normal: 'w.png' 
             background_down: 'b.png' 
             background_color: 1, 1, 1, 0.2 
             values: ['ff', 'Stanford'] 
         Button: 
             canvas.before: 
                 Color: 
                     rgba: 1, 1, 1, 1 
                 Line: 
                     width: 1.5 
                     rectangle: root.width / 2 + ((root.width - 100) / 6) + 50, root.height / 2 - 80, (root.width - 100) / 3 - 50, 60 
             text: 'New Key' 
             font_size: 35 
             size: (root.width - 100) / 3 - 50, 60 
             pos: root.width / 2 + ((root.width - 100) / 6) + 50, root.height / 2 - 80 
             background_normal: 'w.png' 
             background_down: 'b.png' 
             background_color: 1, 1, 1, 0.2 
             on_release: root.add_key() 
  
 <DecryptWindow> 
     GridLayout: 
         size: root.width, root.height 
         canvas.before: 
             Rectangle: 
                 pos: self.pos 
                 size: self.size 
                 source: 'bg.jpg' 
         Label: 
             text: '[b]Enter Encrypted Message[/b]' 
             markup: True 
             font_size: 40 
             size: 50, 50 
             pos: root.width / 2 - 25, root.height - 90 
         TextInput: 
             id: input 
             canvas.before: 
                 Color: 
                     rgba: 1, 1, 1, 1 
                 Line: 
                     width: 1.5 
                     rectangle: 50, root.height / 2, root.width - 100, (root.height / 2) - 120 
             font_size: 40 
             size: root.width - 100, (root.height / 2) - 120 
             pos: 50, root.height / 2 
             background_color: 0, 0, 0, 0 
             selection_color: 1, 1, 1, 0.4 
             cursor_color: 1, 1, 1, 1 
         Button: 
             canvas.before: 
                 Color: 
                     rgba: 1, 1, 1, 1 
                 Line: 
                     width: 1.5 
                     rectangle: 50, root.height / 2 - 80, (root.width - 100) / 3 - 50, 60 
             text: 'Decrypt' 
             font_size: 35 
             size: (root.width - 100) / 3 - 50, 60 
             pos: 50, root.height / 2 - 80 
             background_normal: 'w.png' 
             background_down: 'b.png' 
             background_color: 1, 1, 1, 0.2 
             on_release: root.decrypt() 
         Spinner: 
             id: key 
             canvas.before: 
                 Color: 
                     rgba: 1, 1, 1, 1 
                 Line: 
                     width: 1.5 
                     rectangle: root.width / 2 - ((root.width - 100) / 6) - 30, root.height / 2 - 80, (root.width - 100) / 3 + 60, 60 
             text: 'Choose Key' 
             font_size: 35 
             size: (root.width - 100) / 3 + 60, 60 
             pos: root.width / 2 - ((root.width - 100) / 6) - 30, root.height / 2 - 80 
             background_normal: 'w.png' 
             background_down: 'b.png' 
             background_color: 1, 1, 1, 0.2 
             values: ['ff', 'Stanford'] 
         Button: 
             canvas.before: 
                 Color: 
                     rgba: 1, 1, 1, 1 
                 Line: 
                     width: 1.5 
                     rectangle: root.width / 2 + ((root.width - 100) / 6) + 50, root.height / 2 - 80, (root.width - 100) / 3 - 50, 60 
             text: 'New Key' 
             font_size: 35 
             size: (root.width - 100) / 3 - 50, 60 
             pos: root.width / 2 + ((root.width - 100) / 6) + 50, root.height / 2 - 80 
             background_normal: 'w.png' 
             background_down: 'b.png' 
             background_color: 1, 1, 1, 0.2 
             on_release: root.add_key() 
         TextInput: 
             id: output 
             canvas.before: 
                 Color: 
                     rgba: 1, 1, 1, 1 
                 Line: 
                     width: 1.5 
                     rectangle: 50, 20, root.width - 100, (root.height / 2) - 120 
             font_size: 40 
             selection_color: 1, 1, 1, 0.4 
             cursor_color: 1, 1, 1, 1 
             size: root.width - 100, (root.height / 2) - 120 
             pos: 50, 20 
             background_color: 0, 0, 0, 0 
              
 <KeyWindow> 
     GridLayout: 
         size: root.width, root.height 
         canvas.before: 
             Rectangle: 
                 pos: self.pos 
                 size: self.size 
                 source: 'bg.jpg' 
         Label: 
             text: '[b]Enter Key Name[/b]' 
             markup: True 
             font_size: 40 
             size: 50, 50 
             pos: (root.width / 2) - 25, root.height - 250 
         TextInput: 
             id: key_name 
             canvas.before: 
                 Color: 
                     rgba: 1, 1, 1, 1 
                 Line: 
                     width: 1.5 
                     rectangle: 50, root.height - 350, root.width - 100, 60 
             font_size: 40 
             multiline: False 
             selection_color: 1, 1, 1, 0.4 
             cursor_color: 1, 1, 1, 1 
             size: root.width - 100, 60 
             pos: 50, root.height - 350 
             background_color: 0, 0, 0, 0 
         Label: 
             text: '[b]Enter Key[/b]' 
             markup: True 
             font_size: 40 
             size: 50, 50 
             pos: (root.width / 2) - 25, root.height - 500 
         TextInput: 
             id: key_value 
             canvas.before: 
                 Color: 
                     rgba: 1, 1, 1, 1 
                 Line: 
                     width: 1.5 
                     rectangle: 50, root.height - 600, root.width - 100, 60 
             font_size: 40 
             multiline: False 
             selection_color: 1, 1, 1, 0.4 
             cursor_color: 1, 1, 1, 1 
             size: root.width - 100, 60 
             pos: 50, root.height - 600 
             background_color: 0, 0, 0, 0 
         Button: 
             canvas.before: 
                 Color: 
                     rgba: 1, 1, 1, 1 
                 Line: 
                     width: 2 
                     rectangle: root.width / 2 - 70, root.height - 750, 140, 60 
             text: '[b]Done[/b]' 
             markup: True 
             font_size: 35 
             size: 140, 60 
             pos: root.width / 2 - 70, root.height - 750 
             background_normal: 'w.png' 
             background_down: 'b.png' 
             background_color: 1, 1, 1, 0.2 
             on_release: root.add_key() 
 """) 
  
  
 KEYS = {} 
  
  
 class EncryptWindow(Screen): 
     def on_pre_enter(self): 
         self.ids.input.text = '' 
         self.ids.key.values = list(KEYS.keys()) 
          
     def add_key(self): 
         self.manager.current = 'key' 
          
     def encrypt(self): 
         try: 
             if self.ids.key.text == 'Choose Key': 
                 return Popup(title='Select encryption Key or add a new one', 
                              title_align='center', 
                              size_hint=(None, None), 
                              size=(500, 80), 
                              background_color=(0,0,0,0), 
                              content=None).open() 
             msg = self.ids.input.text 
             msg_bytes = bytes(msg, 'utf-8') 
             encrypted_msg_bytes = Fernet(KEYS[self.ids.key.text]).encrypt(msg_bytes) 
             encrypted_msg = bytes.decode(encrypted_msg_bytes) 
             Clipboard.copy(encrypted_msg)