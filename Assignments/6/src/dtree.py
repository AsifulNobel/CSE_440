#!/usr/bin/env python2

import sys
import logging
import operator
import random
from math import log as logarithm
from collections import OrderedDict
from datetime import datetime
from data_structure import BinaryTree

logger = logging.getLogger("dtree")
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('decision.log', mode='w')
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

random.seed(datetime.now())


def distribution(examples):
    """Calculate distribution of class labels and return a dictionary with keys
    as class label and values as distribution values"""

    example_class_index = len(examples[0]) - 1
    example_class_count = {}

    # Initialize dictionary with class labels as key and 0 as value
    for line in examples:
        example_class_count[line[example_class_index]] = 0

    for line in examples:
        example_class_count[line[example_class_index]] += 1

    total_examples_count = len(examples) * 1.0
    examples_distribution = {}

    for key in example_class_count.keys():
        examples_distribution[key] = example_class_count[key]/total_examples_count

    return examples_distribution


def information_gain(examples, attribute, threshold):
    # tec is total number of examples
    # el is total number of examples less than threshold
    # em is total number of examples greater than or equal to threshold

    tec = len(examples) * 1.0
    el = len([row[attribute] for row in examples if row[attribute] < threshold])
    em = len([row[attribute] for row in examples if row[attribute] >= threshold])

    gain = 0

    if (el/tec) > 0.0:
        gain -= ((el/tec)*logarithm((el/tec), 2))

    if (em/tec) > 0.0:
        gain -= ((em/tec)*logarithm((em/tec), 2))

    return gain


def choose_attribute(examples, attributes):
    max_gain = -1
    best_attribute = -1
    best_threshold = -1

    for attribute in attributes:
        attribute_values = [row[attribute] for row in examples]
        el = min(attribute_values)
        em = max(attribute_values)

        for k in xrange(1, 51):
            threshold = el + k * (em - el) / 51
            gain = information_gain(examples, attribute, threshold)

            if gain > max_gain:
                max_gain = gain
                best_attribute = attribute
                best_threshold = threshold

    return best_attribute, best_threshold, max_gain


def choose_rand_attribute(examples, attributes):
    max_gain = -1
    attribute = -1
    best_threshold = -1

    attribute = random.choice(attributes)
    attribute_values = [row[attribute] for row in examples]
    el = min(attribute_values)
    em = max(attribute_values)

    for k in xrange(1, 51):
        threshold = el + k * (em - el) / 51
        gain = information_gain(examples, attribute, threshold)

        if gain > max_gain:
            max_gain = gain
            best_threshold = threshold

    return attribute, best_threshold, max_gain


def optimized_DTL(examples, attributes, default, pruning_threshold):
    if max(default.values()) == 1 or (len(examples) < 50):
        logger.debug("Found a leaf node, default: {}".format(default))
        return default
    else:
        best_attribute, best_threshold, max_gain = choose_attribute(examples, attributes)

        tree = BinaryTree()
        tree.add_root(attribute=best_attribute, threshold=best_threshold, gain=max_gain)

        examples_left = [row for row in examples if row[best_attribute] < best_threshold]

        examples_right = [row for row in examples if row[best_attribute] >= best_threshold]

        if len(examples_left) > 0 and len(examples_right) > 0:
            tree.attach_left(optimized_DTL(examples_left, attributes, distribution(examples_left), pruning_threshold))

            tree.attach_right(optimized_DTL(examples_right, attributes, distribution(examples_right), pruning_threshold))
        elif len(examples_left) > 0:
            tree.attach_left(optimized_DTL(examples_left, attributes, distribution(examples_left), pruning_threshold))
        elif len(examples_right) > 0:
            tree.attach_right(optimized_DTL(examples_right, attributes, distribution(examples_right), pruning_threshold))


        return tree


def randomized_DTL(examples, attributes, default, pruning_threshold):
    if max(default.values()) == 1 or (len(examples) < 50):
        logger.debug("Found a leaf node, default: {}".format(default))
        return default
    else:
        best_attribute, best_threshold, max_gain = choose_rand_attribute(examples, attributes)

        tree = BinaryTree()
        tree.add_root(attribute=best_attribute, threshold=best_threshold, gain=max_gain)

        examples_left = [row for row in examples if row[best_attribute] < best_threshold]

        examples_right = [row for row in examples if row[best_attribute] >= best_threshold]

        if len(examples_left) > 0 and len(examples_right) > 0:
            tree.attach_left(randomized_DTL(examples_left, attributes, distribution(examples_left), pruning_threshold))

            tree.attach_right(randomized_DTL(examples_right, attributes, distribution(examples_right), pruning_threshold))
        elif len(examples_left) > 0:
            tree.attach_left(randomized_DTL(examples_left, attributes, distribution(examples_left), pruning_threshold))
        elif len(examples_right) > 0:
            tree.attach_right(randomized_DTL(examples_right, attributes, distribution(examples_right), pruning_threshold))

        return tree

def output_decision_tree(decision_tree, index):
    """Print and log node info of decision tree"""

    for node, node_id in decision_tree.breadthFirst():
        if node._attribute is not None:
            logger.info("tree={0:2d}, node={1:3d}, feature={2:2d}, thr={3:6.2f}, gain={4:f}".format(index, node_id, node._attribute, node._threshold, node._gain))

            print "tree={0:2d}, node={1:3d}, feature={2:2d}, thr={3:6.2f}, gain={4:f}".format(index, node_id, node._attribute, node._threshold, node._gain)
        else:
            logger.info("tree={0:2d}, node={1:3d}, feature={2}, thr={3}, gain={4}".format(index, node_id, node._attribute, node._threshold, node._gain))

            "tree={0:2d}, node={1:3d}, feature={2}, thr={3}, gain={4}".format(index, node_id, node._attribute, node._threshold, node._gain)


def output(decision_tree, forest):
    """Print single tree information or multiple tree info of decision forest"""
    if not forest:
        output_decision_tree(decision_tree, 0)
    elif forest:
        for index, tree in enumerate(decision_tree):
            logger.debug("Output of tree: {}".format(index))

            output_decision_tree(tree, index)


def make_decision_tree(examples, attributes, option):
    if option == "optimized":
        logger.debug("Running optimized_DTL...")
        decision_tree = optimized_DTL(examples, attributes, distribution(examples), 50)

        logger.debug("Printing obtained decision_tree nodes...")
        output(decision_tree, False)
    elif option == "randomized":
        logger.debug("Running randomized_DTL...")
        decision_tree = randomized_DTL(examples, attributes, distribution(examples), 50)

        logger.debug("Printing obtained decision_tree nodes...")
        output(decision_tree, False)
    elif option == "forest3":
        logger.debug("Creating forest3...")
        decision_tree = [None] * 3

        for i in xrange(3):
            decision_tree[i] = randomized_DTL(examples, attributes, distribution(examples), 50)

        logger.debug("Printing obtained decision forest trees...")
        output(decision_tree, True)
    elif option == "forest15":
        logger.debug("Creating forest15...")
        decision_tree = [None] * 15

        for i in xrange(15):
            decision_tree[i] = randomized_DTL(examples, attributes, distribution(examples), 50)

        logger.debug("Printing obtained decision forest trees...")
        output(decision_tree, True)

    return decision_tree

def get_accuracy(sorted_distribution, test_example, object_id):
    """Predict class from sorted distribution of class labels. If max value of
    distribution is tied between class labels, randomly choose one and cross
    check it with actual class label of test object. Return accuracy of prediction."""

    sorted_distribution_values = sorted_distribution.values()

    tied_class = [None]
    accuracy = 0.0

    # If there is a tie between class labels, then just checking first two
    # elements of sorted_distribution is enough to detect a tie
    if len(sorted_distribution_values) > 1 and sorted_distribution_values[0] == sorted_distribution_values[1]:
        tied_class = [key for key, value in sorted_distribution.iteritems() if value == sorted_distribution_values[0]]

    logger.debug("tied_class: {}".format(tied_class))

    if tied_class[0] is not None:
        # randomly choose a class label
        predicted_class = random.choice(tied_class)
    else:
        predicted_class = sorted_distribution.items()[0][0]

    # actual class label of test object
    true_class = test_example[len(test_example)-1]

    if predicted_class == true_class:
        accuracy = 1.0
    elif true_class in tied_class:
        accuracy = 1.0 / len(tied_class)

    logger.info("ID={0:5d}, predicted={1:3d}, true={2:3d}, accuracy={3:4.2f}".format(object_id, predicted_class, true_class, accuracy))

    print "ID={0:5d}, predicted={1:3d}, true={2:3d}, accuracy={3:4.2f}\n".format(object_id, predicted_class, true_class, accuracy)

    return accuracy


def classify_test_object(test_example, object_id, node, forest):
    """Get class label distribution from leaf node and pass it to
    get_accuracy function"""

    logger.debug(node._distribution)

    sorted_distribution = OrderedDict(sorted(node._distribution.items(), key=operator.itemgetter(1), reverse=True))

    accuracy = 0.0
    if not forest:
        accuracy = get_accuracy(sorted_distribution, test_example, object_id)
    else:
        return sorted_distribution

    return sorted_distribution, accuracy


def traverse_tree_test(test_example, object_id, node, forest):
    """Recursively traverse a decision tree and return distribution of class labels and/or accuracy depending on whether forest property is true. forest
    is True only if traverse_tree_test is called from traverse_forest_test."""

    # BinaryTree's breadthFirst search could have been used, but forgot to use
    # it. After full implementation, did not change it. Because if it works,
    # no need to fix it....:p
    if node.is_leaf() and not forest:
        sorted_distribution, accuracy = classify_test_object(test_example, object_id, node, forest)

        return sorted_distribution, accuracy
    elif node.is_leaf():
        sorted_distribution = classify_test_object(test_example, object_id, node, forest)

        return sorted_distribution
    else:
        if test_example[node._attribute] < node._threshold:
            if node._left is not None:
                logger.debug("Going left...")
                return traverse_tree_test(test_example, object_id, node._left, forest)
            else:
                # Sometimes tree nodes maybe None and NoneType is always less
                # than threshold. This is why this type of checking is done.

                logger.debug("Going right, but should have gone left...")
                return traverse_tree_test(test_example, object_id, node._right, forest)
        else:
            if node._right is not None:
                logger.debug("Going right...")
                return traverse_tree_test(test_example, object_id, node._right, forest)
            else:
                logger.debug("Going left, but should have gone right...")
                return traverse_tree_test(test_example, object_id, node._left, forest)


def traverse_forest_test(test_example, object_id, decision_tree_list):
    """Run test data on multiple decision trees contained in decision_tree_list.
    Get distribution from multiple decision trees, average those and return
    accuracy of prediction of those decision trees."""

    size_dist_list = len(decision_tree_list)
    sorted_distribution_list = [None] * size_dist_list

    i = 0
    for tree in decision_tree_list:
        sorted_distribution_list[i] = traverse_tree_test(test_example, object_id, tree.get_root(), True)

        i += 1

    sum_distribution = {}
    for key in sorted_distribution_list[0].keys():
        sum_distribution[key] = 0.0

    logger.debug("sum_distribution: {}".format(sum_distribution))
    logger.debug("sorted_distribution: {}".format(sorted_distribution_list))

    # get average of class label distribution values
    for row in xrange(size_dist_list):
        for key in sorted_distribution_list[row].keys():
            logger.debug("key: {}, row:{}".format(key, row))

            try:
                sum_distribution[key] += sorted_distribution_list[row][key]
            except KeyError:
                continue

    for key in sum_distribution.keys():
        sum_distribution[key] /= size_dist_list

    return get_accuracy(OrderedDict(sorted(sum_distribution.items(), key=operator.itemgetter(1), reverse=True)), test_example, object_id)




def get_training_data(file_name, examples):
    """Extract data from file and store it in a 2-d list"""

    logger.debug("Getting training data...")
    with open(file_name, 'rb') as file_handle:
        line_count = 0

        line = file_handle.readline()
        line_elems = line.split()
        elem_count = len(line_elems) - 1

        file_handle.seek(0)

        for line in file_handle:
            line_elems = line.split()
            examples.append([None] * (elem_count + 1))

            for index, elem in enumerate(line_elems):
                if index == elem_count:
                    examples[line_count][index] = int(elem)
                    # Because class label is always integer
                else:
                    examples[line_count][index] = float(elem)

            line_count += 1;

    logger.debug("Finished training data loading.")


def try_test_data(test_file_name, decision_tree):
    """Run all test data on decision_tree and predict class"""

    with open(test_file_name, 'rb') as file_handle:
        line = file_handle.readline()
        line_elems = line.split()
        elem_count = len(line_elems) - 1

        accuracy_list = []
        distribution_list = []

        file_handle.seek(0)

        for index, line in enumerate(file_handle):
            line_elems = line.split()
            test_example = [None] * len(line_elems)

            for i, elem in enumerate(line_elems):
                if i == elem_count:
                    test_example[i] = int(elem)
                    # Because class label is always integer
                else:
                    test_example[i] = float(elem)

            if isinstance(decision_tree, BinaryTree):
                distribution, accuracy = traverse_tree_test(test_example, index, decision_tree.get_root(), False)

                accuracy_list.append(accuracy)
            elif isinstance(decision_tree, list):
                accuracy = traverse_forest_test(test_example, index, decision_tree)

                accuracy_list.append(accuracy)

        logger.info("classification accuracy={0:6.4f}".format(reduce(lambda x, y: x+y, accuracy_list)/len(accuracy_list)))

        print "classification accuracy={0:6.4f}".format(reduce(lambda x, y: x+y, accuracy_list)/len(accuracy_list))


if __name__ == "__main__":
    if len(sys.argv) == 4:
        training_file_name = sys.argv[1]
        test_file_name = sys.argv[2]
        option = sys.argv[3]

        examples = []
        get_training_data(training_file_name, examples)

        # gets attribute indices from first line of examples
        # attribute indices exclude class label index
        attributes = [attribute for attribute in xrange(len(examples[0])-1)]

        # gets decision tree from training examples
        decision_tree = make_decision_tree(examples, attributes, option)

        # runs test data on obtained decision tree
        try_test_data(test_file_name, decision_tree)
    else:
        print "\nUsage: python dtree.py training_file_path test_file_path option"
