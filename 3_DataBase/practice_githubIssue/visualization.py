import psycopg2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import os
from dotenv import load_dotenv
from collections import Counter
import json

# 환경변수 로드
load_dotenv()

class IssueVisualization:
    def __init__(self):
        # DB 연결 정보
        self.db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'database': os.getenv('DB_NAME', 'postgres'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'password'),
            'port': os.getenv('DB_PORT', '5432')
        }
    
    def parse_embedding(self, embedding_str):
        """Convert embedding string to numpy array"""
        if isinstance(embedding_str, str):
            # Remove brackets and convert to number array
            embedding_str = embedding_str.strip('[]')
            return np.array([float(x) for x in embedding_str.split(',')])
        elif isinstance(embedding_str, list):
            return np.array(embedding_str)
        else:
            return np.array(embedding_str)
    
    def load_data_from_db(self):
        """Load issue data from database"""
        print("Loading issue data from database...")
        
        conn = psycopg2.connect(**self.db_config)
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, description, embedding FROM issues;")
            results = cursor.fetchall()
            
            # Separate data and convert embeddings
            ids = [row[0] for row in results]
            titles = [row[1] for row in results]
            descriptions = [row[2] for row in results]
            
            # Convert embedding strings to numpy arrays
            embeddings = []
            for row in results:
                embedding = self.parse_embedding(row[3])
                embeddings.append(embedding)
            
            embeddings = np.array(embeddings)
            
            print(f"Total {len(results)} issues loaded")
            print(f"Embedding dimensions: {embeddings.shape}")
            return ids, titles, descriptions, embeddings
            
        finally:
            cursor.close()
            conn.close()
    
    def find_optimal_clusters(self, embeddings, max_k=6):
        """Find optimal number of clusters using silhouette score"""
        print("Finding optimal number of clusters...")
        
        silhouette_scores = []
        k_range = range(2, min(max_k + 1, len(embeddings)))
        
        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            cluster_labels = kmeans.fit_predict(embeddings)
            score = silhouette_score(embeddings, cluster_labels)
            silhouette_scores.append(score)
            print(f"k={k}: Silhouette score {score:.3f}")
        
        # Select optimal k
        optimal_k = k_range[np.argmax(silhouette_scores)]
        print(f"Optimal number of clusters: {optimal_k} (Silhouette score: {max(silhouette_scores):.3f})")
        
        return optimal_k
    
    def perform_clustering(self, embeddings, n_clusters):
        """Perform KMeans clustering"""
        print(f"Clustering into {n_clusters} clusters...")
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(embeddings)
        
        return cluster_labels, kmeans
    
    def perform_pca(self, embeddings):
        """Perform PCA dimensionality reduction"""
        print("Performing PCA dimensionality reduction...")
        
        pca = PCA(n_components=2, random_state=42)
        embeddings_2d = pca.fit_transform(embeddings)
        
        explained_variance = pca.explained_variance_ratio_
        print(f"PCA explained variance ratio: {explained_variance[0]:.3f}, {explained_variance[1]:.3f}")
        print(f"Total explained variance: {sum(explained_variance):.3f}")
        
        return embeddings_2d, pca
    
    def analyze_clusters(self, titles, descriptions, cluster_labels):
        """Analyze cluster characteristics"""
        print("\nCluster Analysis Results:")
        print("=" * 60)
        
        unique_labels = np.unique(cluster_labels)
        
        for label in unique_labels:
            mask = cluster_labels == label
            cluster_titles = [titles[i] for i in range(len(titles)) if mask[i]]
            cluster_descriptions = [descriptions[i] for i in range(len(descriptions)) if mask[i]]
            
            # Extract key words from titles
            all_text = ' '.join(cluster_titles + cluster_descriptions).lower()
            words = [word for word in all_text.split() if len(word) > 2]  # Only words with 2+ characters
            common_words = Counter(words).most_common(5)
            
            print(f"\nCluster {label} ({len(cluster_titles)} issues):")
            print(f"Key words: {[word for word, count in common_words]}")
            print(f"Representative issue: {cluster_titles[0]}")
    
    def create_visualization(self, embeddings_2d, cluster_labels, titles):
        """Create visualization"""
        print("Creating visualization...")
        
        # Increase figure size by 1.5x
        plt.figure(figsize=(18, 12))
        
        # Cluster colors
        unique_labels = np.unique(cluster_labels)
        colors = plt.cm.tab10(np.linspace(0, 1, len(unique_labels)))
        
        # Plot by cluster with 1.5x larger points
        for i, label in enumerate(unique_labels):
            mask = cluster_labels == label
            plt.scatter(
                embeddings_2d[mask, 0], 
                embeddings_2d[mask, 1],
                c=[colors[i]], 
                label=f'Cluster {label}',
                alpha=0.7,
                s=75  # Increased from 50 to 75 (1.5x)
            )
        
        # Increase font sizes by 1.5x
        plt.title('GitHub Issue Embedding Visualization (PCA + KMeans)', fontsize=24)  # 16 * 1.5
        plt.xlabel('PC1', fontsize=18)  # 12 * 1.5
        plt.ylabel('PC2', fontsize=18)  # 12 * 1.5
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)  # Added fontsize
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Save
        plt.savefig('issue_visualization.png', dpi=500, bbox_inches='tight')
        print("Visualization saved: issue_visualization.png")
        
        plt.show()
    
    def run_visualization(self):
        """Run complete visualization process"""
        print("=== GitHub Issue Visualization Started ===")
        
        # 1. Load data
        ids, titles, descriptions, embeddings = self.load_data_from_db()
        
        # 2. Find optimal number of clusters
        optimal_k = self.find_optimal_clusters(embeddings)
        
        # 3. Clustering
        cluster_labels, kmeans = self.perform_clustering(embeddings, optimal_k)
        
        # 4. PCA dimensionality reduction
        embeddings_2d, pca = self.perform_pca(embeddings)
        
        # 5. Cluster analysis
        self.analyze_clusters(titles, descriptions, cluster_labels)
        
        # 6. Create visualization
        self.create_visualization(embeddings_2d, cluster_labels, titles)
        
        print("\n=== Visualization Complete ===")

# 실행 코드
if __name__ == "__main__":
    visualizer = IssueVisualization()
    visualizer.run_visualization()