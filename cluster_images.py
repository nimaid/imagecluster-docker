#!/usr/bin/env python3

# Parse arguments before importing any other modules
import argparse
parser = argparse.ArgumentParser(description='Groups images together based on similarity (image clustering)')

parser.add_argument("-i", "--image_dir", type=str, required=True,
    help='path to folder with images to be clustered')
parser.add_argument("-s", "--similarity", type=float, required=False, default=0.5,
    help="the percent similarity needed to cluster together (0.0 - 1.0]")
parser.add_argument("-a", "--action", type=str, required=False, choices = ['copy', 'move'], default='copy',
    help="whether the program will copy the images or move them")

args = parser.parse_args()

IMAGE_PATH = args.image_dir
if args.similarity <= 0.0 or args.similarity > 1.0:
    raise ValueError('Similarity percentage must be greater than 0.0 and less than or equal to 1.0')
SIMILARITY = args.similarity
ACTION = args.action

# Import imagecluster and hide Keras FutureWarnings
import warnings  
with warnings.catch_warnings():  
    warnings.filterwarnings("ignore",category=FutureWarning)
    from imagecluster import calc, io as icio, postproc

# Import remaining modules
import os
import shutil

def main():
    clusters_path = os.path.join(IMAGE_PATH, icio.ic_base_dir, 'clusters')

    # The bottleneck is calc.fingerprints() called in this function, all other
    # operations are very fast. get_image_data() writes fingerprints to disk and
    # loads them again instead of re-calculating them.
    print('\nFingerprinting images...\n')
    images,fingerprints,timestamps = icio.get_image_data(IMAGE_PATH)
    print('\nImage fingerprinting done.\n')

    # Run clustering on the fingerprints. Select clusters with similarity index
    print('\nClustering images...\n')
    clusters = calc.cluster(fingerprints, sim=SIMILARITY)
    print('\nClustering done.\n')

    # Re-format clusters into a simple 2D list
    simple_clusters = list()
    for i, (num_in_cluster, cluster_list) in enumerate(clusters.items()):
        for cluster in cluster_list:
            simple_clusters.append(cluster)

    # Find unclustered images
    unclustered_images = set(images.keys()) # Start set with all images
    for cluster in simple_clusters:
        for image in cluster:
            unclustered_images = unclustered_images.difference(set([image]))
    unclustered_images = list(unclustered_images) # Convert to list

    if ACTION == 'copy':
        print('\nCopying images to clusters...\n')
    elif ACTION == 'move':
        print('\nMoving images to clusters...\n')

    # Remove existing clusters (if present)
    if os.path.exists(clusters_path):
        shutil.rmtree(clusters_path)

    # Move images into cluster folders
    cluster_dir_length = len(str(len(simple_clusters)))
    for i, cluster in enumerate(simple_clusters):
        cluster_name = str(i).zfill(cluster_dir_length)
        cluster_dir = os.path.join(clusters_path, cluster_name)
        
        os.makedirs(cluster_dir)
        for image in cluster:
            if ACTION == 'copy':
                shutil.copy(os.path.abspath(image), cluster_dir)
            elif ACTION == 'move':
                shutil.move(os.path.abspath(image), cluster_dir)

    # Move unclustered images too
    for i, image in enumerate(unclustered_images):
        if ACTION == 'copy':
            shutil.copy(os.path.abspath(image), clusters_path)
        elif ACTION == 'move':
            shutil.move(os.path.abspath(image), clusters_path)
        
    print('\nAll done!\n')

if __name__ == "__main__":
    main()