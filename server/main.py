from data_loader import DataLoader
from random_forest import RandomForest
from data_converter import DataConverter

if __name__ == '__main__':
    # dl.populate_django_db(movie_limit=400, cast_limit=8, continue_from=0)

    data_converter = DataConverter()
    data=[]
    m=[]
    casting=['Johnny Depp','Geoffrey Rush','Orlando Bloom','Keira Knightley','Jack Davenport',
    'Jonathan Pryce','Lee Arenberg','Mackenzie Crook']
    genres=['Action','Adventure','Fantasy']
    director='Gore Verbinski'
    writer='Ted Elliott'
    year=2003
    m.append([casting,genres,director,writer,year])
    data.append(data_converter.create_movie(casting,year,genres,writer,director))

    casting=['Hugh Jackman','Jim Carrey','Jackie Chan','Orlando Bloom','Vin Diesel','Halle Berry']
    genres=['Comedy','Romance']
    director='Sam Mendes'
    writer='Neal Purvis'
    year=2008
    m.append([casting,genres,director,writer,year])
    data.append(data_converter.create_movie(casting,year,genres,writer,director))

    casting=['Hugh Jackman','Jim Carrey','Jackie Chan','Orlando Bloom','Vin Diesel','Halle Berry']
    genres=['Action','Adventure']
    director='Sam Mendes'
    writer='Neal Purvis'
    year=2008
    m.append([casting,genres,director,writer,year])
    data.append(data_converter.create_movie(casting,year,genres,writer,director))

    casting=['Sylvester Stallone','Jason Statham','Jet Li','Rihanna','Victoria Bidewell']
    genres=['Romance','Family']
    director='Tim Burton'
    writer='Sylvester Stallone'
    year=2008
    m.append([casting,genres,director,writer,year])
    data.append(data_converter.create_movie(casting,year,genres,writer,director))

    dl = DataLoader()
    X,y = dl.load_dataset(test_cases=data)
    test_cases = X[len(X)-len(data):]
    X = X[:len(X)-len(data)]
    rf = RandomForest(X,y)

    # print('Testing Model Performance...\n')
    # rf.test_performance()

    print('Applying User Tests...\n')
    rf.construct_model()

    n=0
    for test_case in test_cases:
        score = rf.predict_score(test_case)
        print('-Movie '+str(n+1)+'-')
        print('\nCasting: ')
        for a in m[n][0]:
            print(a)
        print('\nGenres:')
        for a in m[n][1]:
            print(a)
        print('\nDirector: ' + m[n][2])
        print('\nWriter: ' + m[n][3])
        print('\nScore: ' + str(score[0]))
        print('\n')
        n = n + 1
