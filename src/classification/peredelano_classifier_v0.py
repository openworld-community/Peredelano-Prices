def pp_classifier(prd_name: str, clf_name: str = 'SGD_clf.pickle') -> str:
    """
    Peredelano-Prices
    This is function for classifying the product by the product name
    Currently the classifier was learned basing on the product list
    from Franca, Aroma and Voli shops in Chernogoria

    Parameters
    ----------
    prd_name : str
        Name of the product we want to classify
    clf_name : str
        filename for the pickled classifier we are going to use
        default is SGD_clf.pickle

    Returns
    -------
    str
        Category name given by the classifier

    """

    import string
    import pickle
    import pandas as pd
    
       
    name_tmp = prd_name.lower()\
        .translate(str.maketrans('','',string.punctuation))\
        .translate(str.maketrans('','',string.digits))
        
    with open(clf_name, 'rb') as f:
        clf_pickled = pickle.load(f)
        
    clf_features = clf_pickled.feature_names_in_
    
    X_test = [int(a in name_tmp.split()) for a in clf_features]
    X_test = pd.DataFrame([X_test], columns=clf_features)
    
    return clf_pickled.predict(X_test)
    
    