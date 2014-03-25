from brute_force import *

class Node(object):
    """
    A node of a graph
    """
    
    def __init__(self, label, links = []):
        """
        label: label of this graph
        links: other noed it is linked to
        """
        
        self.links = links
        self.label = label
    
    def __eq__(self, other):
        return self.label == other.label

class Graph(object):
    """
    Create a graph of variable corrolations from a properly formatted dictionary
    and an optional seed
    """
    
    def __init__(self, d, metric, seed = None):
        """
        d: dictionary from which data is pulled
        metric: how to calculate closeness of variables
        """
        
        self.d = d
        self.metric = metric
        self.nodes = {} # dict mapping labels to nodes

        if not (seed is None):
            self.add_node(seed)
    
    def add_node(self, label, links = []):
        """
        add a new node to the graph
        """
        
        node = Node(label, links)
        self.nodes[label] = node
        
        new_links = self.find_links(label)
        for link_label in new_links:
            if not(link_label in self.nodes):
                # it is new, so we create a new node instance that links back
                # to this node
                self.add_node(link_label, [node])
            else:
                # add node into the link lists for each
                if not(self.nodes[link_label] in node.links):
                    node.links.append(self.nodes[link_label])
                
                if not(node in self.nodes[link_label].links):
                    self.nodes[link_label].links.append(node)
    
    def find_links(self, label):
        """
        find all labels that should be linked to this one
        """
        #import pdb; pdb.set_trace()
        potential_links = MostRelated(self.d, label, metric = self.metric)
        potential_links.sort(reverse = True)
        
        links = []
        index = 0
        cutoff = 30;
        while potential_links[index][0] > cutoff:
            links.append(potential_links[index][1])
            index += 1
        
        return links

if __name__ == '__main__':
    
    taxo = dataToDict('taxo.csv')
    graph = Graph(taxo, CombinedMetrics, 'HypSxRat')
    
    print len(graph.nodes)
    for node in graph.nodes:
        print graph.nodes[node].label, [label.label for label in graph.nodes[node].links]
        
        
