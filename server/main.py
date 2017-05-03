from data_loader import DataLoader
from random_forest import RandomForest
from linear_regression import LinearRegressor
from data_converter import DataConverter
import pickle

if __name__ == '__main__':

    var = raw_input("Choose a Job: \n1)Populate Database\n2)Test Random Forest\n3)Test Linear Regression\n4)User Tests\n5)Save Random Forest Model\n6)Save Linear Regression Model\n")

    dl = DataLoader()

    if var is '1':
        continue_from = raw_input('Continue from:')
        dl.populate_django_db(movie_limit=4000, cast_limit=6, continue_from=int(continue_from))

    X,y = dl.load_dataset()


    if var is '2':
        rf = RandomForest(X,y)
        print('RANDOM FOREST: Testing Model Performance...\n')
        rf.test_performance()

    if var is '3':
        lr = LinearRegressor(X,y)
        print('LINEAR REGRESSION: Testing Model Performance...\n')
        lr.test_performance()

    if var is '5':
        print('RANDOM FOREST: Saving Model...\n')
        rf = RandomForest(X,y)
        model = rf.construct_model()
        filename = 'finalized_model.sav'
        pickle.dump(model, open(filename, 'wb'))

    if var is '6':
        print('LINEAR REGRESSION: Saving Model...\n')
        model = LinearRegressor(X,y).construct_model()
        filename = 'finalized_model.sav'
        pickle.dump(model, open(filename, 'wb'))

    if var is '4':
        print('Applying User Tests...\n')
        rf = RandomForest(X,y)
        rf.construct_model()

        data_converter = DataConverter()
        data=[]

        casting=['Johnny Depp','Geoffrey Rush','Orlando Bloom','Keira Knightley','Jack Davenport',
        'Jonathan Pryce','Lee Arenberg','Mackenzie Crook']
        genres=['Action','Adventure','Fantasy']
        director='Gore Verbinski'
        writer='Ted Elliott'
        year=2003
        data.append([casting,genres,director,writer,year])

        casting=['Hugh Jackman','Jim Carrey','Jackie Chan','Orlando Bloom','Vin Diesel','Halle Berry']
        genres=['Comedy','Romance']
        director='Sam Mendes'
        writer='Neal Purvis'
        year=2008
        data.append([casting,genres,director,writer,year])

        casting=['Hugh Jackman','Jim Carrey','Jackie Chan','Orlando Bloom','Vin Diesel','Halle Berry']
        genres=['Action','Adventure']
        director='Sam Mendes'
        writer='Neal Purvis'
        year=2008
        data.append([casting,genres,director,writer,year])

        casting=['Sylvester Stallone','Jason Statham','Jet Li','Rihanna','Victoria Bidewell']
        genres=['Romance','Family']
        director='Tim Burton'
        writer='Sylvester Stallone'
        year=2008
        data.append([casting,genres,director,writer,year])

        n=0
        for test_case in data:
            score = rf.predict_score(data_converter.create_movie(test_case))
            print('-Movie '+str(n+1)+'-')
            print('\nCasting: ')
            for a in test_case[0]:
                print(a)
            print('\nGenres:')
            for a in test_case[1]:
                print(a)
            print('\nDirector: ' + test_case[2])
            print('\nWriter: ' + test_case[3])
            print('\nYear: ' + test_case[4])
            print('\nScore: ' + str(score[0]))
            print('\n')
            n = n + 1
