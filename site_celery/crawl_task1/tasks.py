from site_celery.main import app
import time

@app.task(name='task1')
def add(x, y):
    time.sleep(2)
    print("The mots_add task has been run , result is : %s !" % str(x + y))
    return x + y