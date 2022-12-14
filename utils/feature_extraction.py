import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA, KernelPCA

from tqdm import tqdm_notebook

import ast

def extract_embeddings_features(embeddings):
	"""
	Args:
		embeddings (pd.Series): Pandas Series of string representation of feature vectors.
	Return:
		(np.ndarray): feature matrix of dimension (n_observations, n_features)
	"""
	n = embeddings.shape[0]
	embeddings_matrix = []

	for i in tqdm_notebook(range(n), desc="extracting features"):
		# embeddings are encoded as string representation of vector
		# convert these into list
		# Note: should'nt set ast.litteral_eval(...) to a variable, then append to the list
		# since it would consume a huge quantity of ram.
		# better directly appending
		embeddings_matrix.append(ast.literal_eval(embeddings.iloc[i]))

	return embeddings_matrix

def pca_on_embeddings(train_embeddings_matrix, test_embeddings_matrix, X2_embeddings_matrix, train_index, test_index, X2_index, prefix, n_components=10, run_pca=True, non_linear=True):
	scaler = StandardScaler()

	n_features_before_pca = len(train_embeddings_matrix[0])

	# standardize data
	train_embeddings_matrix = scaler.fit_transform(train_embeddings_matrix)
	test_embeddings_matrix = scaler.transform(test_embeddings_matrix)
	X2_embeddings_matrix = scaler.transform(X2_embeddings_matrix)

	print(n_components)

	if run_pca:
		if non_linear:
			kpca = KernelPCA(n_components=n_components, kernel="rbf")

			train_embeddings_matrix = kpca.fit_transform(train_embeddings_matrix)
			test_embeddings_matrix = kpca.transform(test_embeddings_matrix)
			X2_embeddings_matrix = kpca.transform(X2_embeddings_matrix)

		else:
			pca = PCA(n_components=n_components)

			train_embeddings_matrix = pca.fit_transform(train_embeddings_matrix)
			test_embeddings_matrix = pca.transform(test_embeddings_matrix)
			X2_embeddings_matrix = pca.transform(X2_embeddings_matrix)

		print(f"successfully reduced from {n_features_before_pca} features to {len(train_embeddings_matrix[0])} features")
	
	
	train_embeddings_df = pd.DataFrame(train_embeddings_matrix, index=train_index).add_prefix(prefix)
	test_embeddings_df = pd.DataFrame(test_embeddings_matrix, index=test_index).add_prefix(prefix)
	X2_embeddings_matrix = pd.DataFrame(X2_embeddings_matrix, index=X2_index).add_prefix(prefix)

	return train_embeddings_df, test_embeddings_df, X2_embeddings_matrix