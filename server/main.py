from data_loader import DataLoader
from random_forest import RandomForest


if __name__ == '__main__':

    dl = DataLoader()

    # dl.populate_django_db(movieLimit=5360, castLimit=10, continueFrom=2666)

    X,y = dl.load_dataset()
    rf = RandomForest(X,y)
    rf.test_performance()
