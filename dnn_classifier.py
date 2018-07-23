import os
import sys
import numpy as np
import tensorflow as tf
from classify_image import NodeLookup

modelDir = "/usr/src/app/model"

modelName = "classify_image_graph_def.pb"
label_lookup_path = "imagenet_2012_challenge_label_map_proto.pbtxt"
uid_lookup_path = "imagenet_synset_to_human_label_map.txt"

def classifyImage(imagePath):
	scores_list = []
	image_data = tf.gfile.FastGFile(imagePath, 'rb').read()
	
	with tf.gfile.FastGFile(os.path.join(modelDir, modelName), 'rb') as f:
	    graph_def = tf.GraphDef()
	    graph_def.ParseFromString(f.read())
	    _ = tf.import_graph_def(graph_def, name='')


	with tf.Session() as sess:
    		softmax_tensor = sess.graph.get_tensor_by_name('softmax:0')
    		predictions = sess.run(softmax_tensor,
                           {'DecodeJpeg/contents:0': image_data})
    		predictions = np.squeeze(predictions)

    		# Creates node ID --> English string lookup.
    		node_lookup = NodeLookup(os.path.join(modelDir, label_lookup_path), os.path.join(modelDir, uid_lookup_path))

    		top_k = predictions.argsort()[-5:][::-1]
    		for node_id in top_k:
    			human_string = node_lookup.id_to_string(node_id)
      			score = predictions[node_id]
      			# scores_list.append((human_string, score))
            		scores_list.append(human_string.split(",")[0])
	return scores_list

# print classifyImage(sys.argv[1])
