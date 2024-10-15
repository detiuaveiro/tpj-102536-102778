from Utils import Subject

class Test(Subject):

    def on_key_down(self, key: int) -> None:
        print(key)
    

a = Test()
a.fps = 5
a.run()