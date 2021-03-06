import numpy as np
import tensorflow as tf
import pandas as pd
import sys
import pprint

def restore_with_var_dict(key, var_dict):
    try:
        return tf.get_variable(key, shape = var_dict[key]['shape'], initializer = tf.constant_initializer(var_dict[key]['value']))
    except KeyError:
        print("No such string")
        return

def get_var_dict(sess, string):
    var_dict = {}
    i= 0
    
    while True:
        try: 
            temp = tf.get_collection(string)[i]
            prop = {}
            prop['shape'] = temp.get_shape().as_list()
            prop['value'] = sess.run(temp)
            var_dict[temp.op.name] = prop
            i+=1
        except IndexError:
            break;
    
    return var_dict

def master_initializer(sess):
    uninitailized_variables=[] 
    for v in tf.global_variables():
        try :
            sess.run(v)
        except tf.errors.FailedPreconditionError:
            uninitailized_variables.append(v)
    return tf.variables_initializer(uninitailized_variables)

def print_keys(string):
    print("Collection name : {}".format(string))
    i = 0
    while True:
        try:
            print(tf.get_collection(string)[i])
            i+=1
        except IndexError:
            break;

def get_tensor_by_name(string):
    i = 0
    while True:
        try:
            if tf.global_variables()[i].name == string:
                return tf.global_variables()[i]
            i+=1
        except IndexError:
            print("No such tensor")
            return None

def print_nodes(graph):
    print("Graph : {}".format(graph))
    temp = [n.name for n in graph.as_graph_def().node]
    for i in range(len(temp)):
        print(temp[i])

def print_graph_properties(graph):
    print("building_function : {}".format(graph.building_function))
    print("finalized : {}".format(graph.finalized))
    print("graph_def_versions : {}".format(graph.graph_def_versions))
    print("seed : {}".format(graph.seed))
    print("version : {}".format(graph.version))
