#!/usr/bin/python

import twik.db as db
from mapgen import graph_algorithms

def has_dst(pce_id):
    orders_for_piece = db.callproc('orders_for_piece', pce_id)
    if orders_for_piece:
        piece_order = orders_for_piece[0]
        return bool(piece_order['has_dst'])
    
    return False

def has_op(pce_id):
    orders_for_piece = db.callproc('orders_for_piece', pce_id)
    if orders_for_piece:
        piece_order = orders_for_piece[0]
        return bool(piece_order['operands'])
    
    return False

class graph(object):
    
    def __init__(self, gam_id):
        self.gam_id = gam_id
        self.terr_list = [int(row['ter_id']) for row in db.callproc('terrs_in_game', gam_id)]
        self.terr_list.sort()
        self.terr_map = dict([(self.terr_list[i], i) for i in xrange(len(self.terr_list))])
        self.m = [[0 for x in xrange(len(self.terr_list))] for y in xrange(len(self.terr_list))]
        for ter_id in self.terr_list:
            for row in db.callproc('terr_adj', ter_id):
                ter = self.terr_map[ter_id]
                adj = self.terr_map[row['ter_id']]
                self.m[ter][adj] = 1
            self.m[ter][ter] = 1
    
    def create_order_graph(self):
        pass




if __name__ == '__main__':
    g = graph(1)
    graph_algorithms._print_matrix(g.m)
