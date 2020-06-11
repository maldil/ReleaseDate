import json
import random

def write_test_file():
    fx=0
    file=[]
    for i in range(30):
        features= ["F"+str(j) for j in range(i+10)]
        feature_implimentation_time = [random.randint(j+10,j+100)  for j in range(i+10)]
        dependencies=[]
        if i%2==0:
            for th in range(i-10):
                dependencies.append(["F"+str(th),"F"+str(th+1)])
        else:
            dependencies =  [[features[random.randint(0, len(features)) - 1], features[random.randint(0, len(features)) - 1]] for j in
             range(i + 10)]
        sequential =  []
        developers = ["D"+str(j) for j in range(i+10)]
        parallel_tasks =   []
        feature_developer = []
        data_file = {"features":features ,"feature_implimentation_time":feature_implimentation_time ,
        "dependencies":dependencies ,"sequential":sequential , "developers":developers ,
        "parallel_tasks":parallel_tasks ,"feature_developer":feature_developer}
        file.append(data_file)
        json
    json_object = json.dumps(file, indent=4)
    with open('performance_data.json', 'w') as fp:
        fp.write(json_object)
if __name__ == '__main__':
    write_test_file()