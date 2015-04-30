import numpy as np
from utils.redis import redis
from search_engine.indexing import fdt_name, ft_name, wd_name


def get_frequency_of_term_in_document(collection_kind, term, doc_ID):
    '''
    Gets the frequency of the given term in the given document.
    '''
    collection = fdt_name(collection_kind, term)
    return redis.zscore(collection, doc_ID)


def get_number_of_documents_containing_term(collection_kind, term):
    '''
    Gets the number of documents containing the given term.
    '''
    return redis.hmget(ft_name(collection_kind), term)


def get_number_of_terms_in_collection(collection_kind):
    '''
    Get the total number of terms in the given collection.
    '''
    frequencies = 0
    for v in redis.hvals(ft_name(collection_kind)):
        frequencies += int(v)

    return frequencies


def get_magnitude_of_weights_vector(collection_kind, doc_ID):
    return redis.hmget(wd_name(collection_kind), doc_ID)


def get_weight_of_term_in_document(term_frequency_in_document):
    return 1 + np.log(term_frequency_in_document)


def get_magnitude_of_vector(vector):
    '''
    Vector is a list of quantities.

    Returns the square root of the sum of the squares
    of the terms.
    '''
    v = np.array(vector)
    return np.sqrt(v.dot(v))
