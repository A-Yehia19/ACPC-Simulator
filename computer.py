class computer:
    def __init__(self, life):
        self.life = life
    
    '''add task to the computer'''
    def work(self, time):
        if time <= self.life:
            self.life -= time
            return True # can take the task
        else:
            return False # cant take the task
        