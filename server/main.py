from data_loader import DataLoader
from random_forest import RandomForest

if __name__ == '__main__':
    dl = DataLoader()
    # dl.populate_django_db(movie_limit=400, cast_limit=8, continue_from=0)
    X,y = dl.load_dataset()
    rf = RandomForest(X,y)

    print('Testing Model Performance...\n')
    rf.test_performance()
