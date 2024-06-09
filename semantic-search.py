import numpy as np
from annoy import AnnoyIndex
import pandas as pd
from datasets import Dataset
import cohere

def load_ann_index(ann_index_path):
    ann_index = AnnoyIndex(100, 'angular')  # Assuming embedding dimension is 100
    ann_index.load(ann_index_path)  # Load the saved Annoy index
    return ann_index

def find_nearest_neighbors(ann_index, query_embedding, num_neighbors=10):
    # Retrieve the nearest neighbors
    similar_item_ids = ann_index.get_nns_by_vector(query_embedding, num_neighbors, include_distances=True)
    return similar_item_ids

def main():
    ann_index_path = 'testFinal.ann'
    ann_index = load_ann_index(ann_index_path)

    # Assuming you have the code for embedding the query description using Cohere
    model_name = "embed-english-v3.0"
    api_key = "wnIb0A1JGzSqNSH8XzpLIKarwGLF800b8u0ztlGw"
    input_type_query = "search_query"
    co = cohere.Client(api_key)
    query_description = """
    Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
    You may assume that each input would have exactly one solution, and you may not use the same element twice.
    You can return the answer in any order.
    """
    query_embedding = co.embed(texts=[query_description], model=model_name, input_type=input_type_query).embeddings[0]

    # Find nearest neighbors
    similar_item_ids = find_nearest_neighbors(ann_index, query_embedding)

    # Display results
    dataset = pd.read_csv('dataAlgTwo.txt', delimiter='\t')  # Load your dataset here if it's not already loaded
    query_results = pd.DataFrame(data={'algorithm': dataset.iloc[similar_item_ids[0]]['algorithm'],
                                       'description': similar_item_ids[1]})
    print(query_results)

if __name__ == "__main__":
    main()