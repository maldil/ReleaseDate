from pysmt.shortcuts import Symbol, LE, GE, Int,String, And,Or, Equals, Plus, Solver, is_sat,Not, get_model, BVSub,Minus,ToReal
from pysmt.typing import INT,STRING
from itertools import combinations
from tqdm import tqdm
from time import sleep
from datetime import datetime,timedelta
import json

def error_handling(dependencies,sequential,feature_developer,feature_implimentation_time,features):
    assert len(features)==len(feature_implimentation_time), "You have to specify development time for all the features"
    for dev in dependencies:
        assert len(dev)==2 , str(dev)+", the length of the dependent jobs should be two, If F1 dependent on F2 it sould be [F1,F2]"
    for dev in sequential:
        assert len(dev)==2 , str(dev)+", the length of the dependent jobs should be two, If F1 can not be executed with F2 is should be [F1,F2]"
    for dev in feature_developer:
        assert len(dev)==2 , str(dev)+", the length of the dependent jobs should be two, If F1 can be executed by the developer D2 it should be [F1,D1]"

def iterate_to_find_satisfiable_solution(features, feature_implimentation_time, dependencies, sequential, developers, feature_developer,parallel_tasks, end_time):

    feature_time_map={}
    i=1
    for fe in features:
        feature_time_map[fe]={'EndTime':Symbol('E'+str(i),INT),'StartTime':Symbol('S'+str(i),INT),'Duration':Int(feature_implimentation_time[i-1])}
        i+=1

    b_greater = And(And(GE(feature_time_map[fe]['EndTime'],Int(0)),GE(feature_time_map[fe]['StartTime'],Int(0))) for fe in features)

    b_impli_time= And(Equals(Minus(feature_time_map[l]['EndTime'],feature_time_map[l]['StartTime']),feature_time_map[l]['Duration']) for l in features)


    b_dependencies =  And(GE(feature_time_map[depe[1]]['StartTime'],feature_time_map[depe[0]]['EndTime']) for depe in dependencies)

    b_sequential = And(Or(GE(feature_time_map[seq[1]]['StartTime'],feature_time_map[seq[0]]['EndTime']),
                          GE(feature_time_map[seq[0]]['StartTime'], feature_time_map[seq[1]]['EndTime'])) for seq in sequential)




    developer_feature_imp = {}
    for fet_dev in feature_developer:
        developer_feature_imp.setdefault(fet_dev[1],[]).append(fet_dev[0])


    and_relation = []
    for val in developer_feature_imp.values():
        if len(val)>1:
            for comb in combinations(val,2):
                and_relation.append(Or(GE(feature_time_map[comb[1]]['StartTime'], feature_time_map[comb[0]]['EndTime']),
                   GE(feature_time_map[comb[0]]['StartTime'], feature_time_map[comb[1]]['EndTime'])))
    b_dev_pararale = And(and_relation)
    and_parallel=[]
    for val in parallel_tasks:
        and_parallel.append(And(LE(feature_time_map[val[0]]['StartTime'], feature_time_map[val[1]]['StartTime']),
                   GE(feature_time_map[val[0]]['EndTime'], feature_time_map[val[1]]['StartTime'])))

    b_parallel = And(and_parallel)

    print('++++++++++++++Conditions++++++++++++++++')
    print('Start and End times should be grater than zero : ',b_greater)
    print('Difference between end and start times : ',b_impli_time)
    print('Some features should be implimented first : ',b_dependencies)
    print('Some features can not be executed parallelly : ',b_sequential)
    print('Some features need specific developers : ',b_dev_pararale)
    print('Some features need to be started before ending some features : ', b_parallel)

    print('++++++++++++++Release Dates++++++++++++++++')
    end_time=1
    max_end_time = sum(feature_implimentation_time)
    sloved = False
    for end in tqdm(range(max_end_time),'running binary search to find shortest release date'):
        sleep(0.25)
        b_end_time = And(LE(fe['EndTime'], Int(end_time)) for fe in feature_time_map.values())
        formula = And(b_greater, b_impli_time, b_dependencies, b_sequential, b_dev_pararale, b_end_time,b_parallel)
        if is_sat(formula):
            print('\n'+'You have to spend at least',end_time, 'days to finish your next release')
            print('Therefore, the closest release date is :', (datetime.today() + timedelta(end_time)).strftime('%d/%m/%Y'))
            for key,val in feature_time_map.items():
                print('Feature',key,', Start Date :', (datetime.today()+ timedelta(get_model(formula)[val['StartTime']].constant_value())).strftime('%d/%m/%Y')   ,'-> End Date : ', (datetime.today() + timedelta(get_model(formula)[val['EndTime']].constant_value())).strftime('%d/%m/%Y'))
            sloved=True
            break
        end_time+=1
    if sloved==False:
        print("This problem is not solvable")

    # print(b_devlopers)
    # print(is_sat(b_devlopers))


    return

def process(features, feature_implimentation_time, dependencies, sequential, developers, feature_developer,parallel_tasks):

    end_time = 5
    error_handling(dependencies, sequential, feature_developer,feature_implimentation_time,features)
    iterate_to_find_satisfiable_solution(features, feature_implimentation_time, dependencies, sequential, developers, feature_developer,parallel_tasks, end_time)

if __name__ == '__main__':
    with open('./release_data.json','r') as file:
        datas = json.loads(file.read())
    i=1
    for data in datas:
        print('\n'+'#################Test Case',i,'#####################')
        features = data['features']
        feature_implimentation_time = data['feature_implimentation_time']
        dependencies = data['dependencies']
        sequential = data['sequential']
        developers = data['developers']
        feature_developer = data['feature_developer']
        parallel_tasks=data["parallel_tasks"]
        process(features, feature_implimentation_time, dependencies, sequential, developers, feature_developer,parallel_tasks)
        i+=1