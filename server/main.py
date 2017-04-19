from data_loader import DataLoader
from random_forest import RandomForest
from linear_regression import LinearRegressor
from data_converter import DataConverter

if __name__ == '__main__':
    dl = DataLoader()
    # dl.populate_django_db(movie_limit=400, cast_limit=8, continue_from=0)

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

    X,y = dl.load_dataset()
    rf = RandomForest(X,y)

    print('RANDOM FOREST: Testing Model Performance...\n')
    rf.test_performance()

    # print('Applying User Tests...\n')
    # rf.construct_model()

    X,y = dl.load_dataset()
    lr = LinearRegressor(X,y)

    print('LINEAR REGRESSION: Testing Model Performance...\n')
    lr.test_performance()

    # print('Applying User Tests...\n')
    # rf.construct_model()

    # n=0
    # for test_case in data:
    #     score = rf.predict_score(data_converter.create_movie(test_case))
    #     print('-Movie '+str(n+1)+'-')
    #     print('\nCasting: ')
    #     for a in test_case[0]:
    #         print(a)
    #     print('\nGenres:')
    #     for a in test_case[1]:
    #         print(a)
    #     print('\nDirector: ' + test_case[2])
    #     print('\nWriter: ' + test_case[3])
    #     print('\nYear: ' + test_case[4])
    #     print('\nScore: ' + str(score[0]))
    #     print('\n')
    #     n = n + 1
