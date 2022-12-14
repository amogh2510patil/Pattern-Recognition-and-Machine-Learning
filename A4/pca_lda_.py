
import scipy
import numpy as np
def covariance(x,u):
    N = len(x)-1
    out = np.zeros((len(x[0]),len(x[0])))
    for i,v in enumerate(x):
        vec = (v-u)
        vec = vec.reshape((len(vec),1))
        out += np.dot(vec,vec.T)
    covariance_matrix = (1/N) * out
    return covariance_matrix

def pca_(data,L):
    cov = covariance(data,np.mean(data,axis=0))
    e,V = np.linalg.eig(cov)        #Finding Eigen values and vectors of martix A
    mag,e,V = map(np.array, zip(*sorted(zip(abs(e),e,V.T),reverse=True)))   #Sorting eigen vals and vecs
    V=V.T
    for i in range(len(cov)):
        exp_var = np.sum(e[:i+1]) / np.sum(e)
        if exp_var > L:
            break
    return V[:,:i+1]

def lda_(X, y, Per):
    if X.shape[1] >3000:
        return pca_(X,Per)
    n_features = X.shape[1]
    class_labels = np.unique(y)

    mean_overall = np.mean(X, axis=0)
    SW = np.zeros((n_features, n_features))
    SB = np.zeros((n_features, n_features))
    cov = covariance(X,mean_overall)
    for c in class_labels:
        X_c = X[y == c]
        mean_c = np.mean(X_c, axis=0)
        SW += X_c.shape[0]*covariance(X_c,mean_c)
        n_c = X_c.shape[0]
        mean_diff = (mean_c - mean_overall).reshape(n_features, 1)
        mean_diff = mean_diff.reshape((len(mean_diff),1))
        SB += n_c * np.dot(mean_diff,mean_diff.T)
    
    # A = np.linalg.inv(SW).dot(SB)
    A = np.linalg.solve(SW,SB)

    e, V = scipy.linalg.eig(SW, SB)    
    idxs = np.argsort(abs(e))[::-1]
    e = e[idxs]
    V = V[idxs]
 
    V=V.T
    eigenvectors = V
    eigenvalues = e
    # store first n eigenvectors
    for i in range(len(eigenvalues)):
        exp_var = np.sum(eigenvalues[:i+1]) / np.sum(eigenvalues)
        if exp_var > Per:
            break
    return eigenvectors[:,:i+1]

def transform(Q, X):
    # project data
    return np.dot(X, Q).real