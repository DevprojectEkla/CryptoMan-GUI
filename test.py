"""Modules natifs, modules kivy, kivy properties, modules persos"""
import os
os.environ['KIVY_IMAGE'] = 'pil'

from kivy.app import App
from kivy.config import Config
# pour activer le clavier virtuel 
# Config.set('kivy', 'keyboard_mode', 'systemanddock')
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
# l'import suivant est utilisé lorsque l'on veut redimmensionner la fenêtre d'affichage
""" Contrairement aux indications de PyCharm ces imports sont nécessaires
pour le fonctionnement du fichier cryptogui.kv
car le ScreenManager fait appel à chacune de ces classes"""
from _01_AlgoG import AlgoG
from _02_ChoixFichier import FichierIntrouvable
from _02_KeyFile import Key
from _03_RootWidget import RootWidget
from _03_ChoixFichierClef import ChoixFichierClef
from _03_ChoixDossierCrypter import ChoixDossierCrypter
from _03_ChoixDossierDecrypter import ChoixDossierDecrypter
from _03_ChoixFichierCrypter import ChoixFichierCrypter, AskOverwriteCrypter
from _03_ChoixFichierDecrypter import ChoixFichierDecrypter, AskOverwriteDecrypter
from _04_CrypterFichier import CrypterFichier
from _04_CrypterDossier import CrypterDossier
from _05_DecrypterDossier import DecrypterDossier
from _05_DecrypterFichier import DecrypterFichier
import pdb # test de PythonDebugger mais pas encore en place...

def reset():
    import kivy.core.window as window
    from kivy.base import EventLoop
    if not EventLoop.event_listeners:
        from kivy.cache import Cache
        window.Window = window.core_select_lib('window', window.window_impl, True)
        Cache.print_usage()
        for cat in Cache._categories:
            Cache._objects[cat] = {}

class CryptoGUI(App):
    """Main Loop et screen manager de l'application"""
    app_path = os.path.dirname(os.path.abspath("_00_CryptoGUI.py"))
    main_screen = ObjectProperty()
    touch_y = None
    touch_x = None
    touch = None

    def build(self):
        # print(Window._get_size())
        # pdb.set_trace() python debugger
        
        # pour l'effet de presentation uncomment this:
        Window.minimize()
        Window.fullscreen = True
        # not this:
        # Window.size = (800, 600) changement dynamique de la taille de fenêtre
        self.icon = f"{self.app_path}\\img\\icons\\icon128x128.ico"
        self.title = "CryptoMan v.2.0"
        algo = AlgoG()
        # uncomment this too
        algo.presentation2()
        os.chdir(self.app_path)
        Window.restore()
        sm = ScreenManager()
        return sm

    def click(self, touch):
        print("\nCustomLabel.on_touch_down:")
        self.touch_x, self.touch_y = touch.spos[0], touch.spos[1]

    def drag(self, touch):
        Window.top = self.touch_y + touch.spos[0]
        Window.left = self.touch_x + touch.spos[1]

    def close_app(self):
        self.close_app()

    @staticmethod
    def minimize():
        Window.minimize()


class MoveWindow(Button):

    touch_y = None
    touch_x = None

    def on_touch_down(self, touch):
        print("\nCustomLabel.on_touch_down:")
        CryptoGUI.click(self, touch)
        print(super(MoveWindow, self).on_touch_down(touch))
        if self.collide_point(*touch.pos):
            print("\ttouch.pos =", touch.pos)
            self.touch_x, self.touch_y = touch.spos[0], touch.spos[1]
            return True
        return super(MoveWindow, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        print("\nCustomLabel.on_touch_move:")
        while CryptoGUI.drag(self, touch):
            Window.top = self.touch_y + touch.spos[0]
            Window.left = self.touch_x + touch.spos[1]
            if self.collide_point(*touch.pos):
                print("\ttouch.pos =", touch.pos)
                Window.top = self.touch_y + touch.spos[0]
                Window.left = self.touch_x + touch.spos[1]
                return True
            return super(MoveWindow, self).on_touch_move(touch)


if __name__ == '__main__':
    # Changement permanent de la taille de la fenêtre. Il ne faut pas lancer l'appli en même temps.
    # Config.set('graphics', 'width', '1440')
    # Config.set('graphics', 'height', '960')
    # Config.write()
    # reset()
    CryptoGUI().run()

    # retour aux valeurs par défaut
    # Config.set('graphics', 'width', '800')
    # Config.set('graphics', 'height', '600')
    # Config.write()
