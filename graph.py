from brute_force import *
from scales import *

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
    
    def __init__(self, d, metric, seed):
        """
        d: dictionary from which data is pulled
        metric: how to calculate closeness of variables
        """
        
        self.d = d
        self.metric = metric
        self.nodes = {} # dict mapping labels to nodes
        self.add_node(seed)
    
    def add_node(self, label, links = None):
        """
        add a new node to the graph
        """
        if links == None:
            links = []
        
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
        cutoff = 35;
        while potential_links[index][0] > cutoff:
            links.append(potential_links[index][1])
            index += 1
        
        return links
    
    def __str__(self):
    
        resp = str(len(self.nodes)) + ' nodes:\n'
        for node in self.nodes:
            resp += self.nodes[node].label+ str([link.label for link in self.nodes[node].links])+'\n'
        
        return resp

def all_graphs(d, metric):
    """
    Given a data dictionary, find all the graphs in it.
    Returns a list of graphs.
    """
    
    interesting_labels = {key for key in d['__numeric__'] if key in d['__relevant__']}
    
    graphs = []
    while interesting_labels:
        # pick a label
        label = interesting_labels.pop()
        # make a graph
        new_graph = Graph(d, metric, label)
        graphs.append(new_graph)
        # remove the used labels from the set of ones to look at
        interesting_labels -= set(new_graph.nodes.keys())
    
    return graphs
    

if __name__ == '__main__':
    
    taxo = dataToDict('taxo.csv')
    beths = dataToDict('beths.csv')
    #graph = Graph(taxo, CombinedMetrics, 'weapcr')
    
    #print graph
    #print len(graph.nodes)
    #for node in graph.nodes:
    #    print graph.nodes[node].label, [label.label for label in graph.nodes[node].links]
    
    #print len(all_graphs(taxo, CombinedMetrics))
    #for graph in all_graphs(taxo, MomentAnalysis):
    #    if len(graph.nodes)>1:
    #        print '\n=================\n'
    #        print graph
    
    scales.extend(demographics)
    reduced_taxo = {scale:taxo[scale] for scale in scales}
    label = 'HypSxRat'
    
    graph = Graph(reduced_taxo, MomentAnalysis, label)
    print graph
    
    print '\n==========\n'
    print 'MomentAnalysis'
    related = MostRelated(reduced_taxo, label, MomentAnalysis)
    related.sort(reverse = True)
    print related
    
    print '\n==========\n'
    print 'WeightedCorr'
    related = MostRelated(reduced_taxo, label, WeightedCorr)    
    related.sort(reverse = True)
    print related
    
    print '\n==========\n'
    print 'Corr'
    related = MostRelated(reduced_taxo, label)    
    related.sort(reverse = True)
    print related
