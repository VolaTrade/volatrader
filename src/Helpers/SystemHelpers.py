import os 


#TODO unit test 
def removeJsonFromDir() -> None:
    dir_name = os.getcwd()
    test = os.listdir(dir_name)
    for item in test:
        if item.endswith(".json"):
            os.remove(os.path.join(dir_name, item))
