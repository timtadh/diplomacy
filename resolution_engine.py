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
        self.ter_m = [[0 for x in xrange(len(self.terr_list))] for y in xrange(len(self.terr_list))]
        for ter_id in self.terr_list:
            for row in db.callproc('terr_adj', ter_id):
                ter = self.terr_map[ter_id]
                adj = self.terr_map[row['ter_id']]
                self.ter_m[ter][adj] = 1
            self.ter_m[ter][ter] = 1
    
    def create_order_graph(self):
        self.pieces_info = dict([(int(p['pce_id']), p) for p in db.callproc('pieces_for_game', self.gam_id)])
        self.pieces = [k for k in self.pieces_info.keys()]
        self.pieces.sort()
        self.ter_piece_map = dict([(int(self.pieces_info[k]['ter_id']), k) for k in self.pieces_info.keys()])
        
        self.piece_map = dict([(pce_id, i) for i, pce_id in enumerate(self.pieces)])
        
        self.pce_m = [[0 for x in xrange(len(self.terr_list))] for y in xrange(len(self.pieces))]
        
        self.no_conflict = list()
        
        for pce_id in self.pieces:
            for row in db.callproc('orders_for_piece', pce_id):
                dst = row['destination']
                
                if dst and self.ter_piece_map.has_key(int(dst)):
                    order_type = int(row['order_type'])
                    if order_type == 1: # move
                        self.pce_m[pce_id][dst] = 1
                    elif order_type == 2: # support
                        self.pce_m[pce_id][dst] = 2
                    elif order_type == 3: # hold
                        self.pce_m[pce_id][dst] = 3
                    else:
                        raise Exception, "order type %d is not yet supported" % order_type
                else:
                    self.no_conflict.append(row)
        
        print len(self.no_conflict)
        graph_algorithms._print_matrix(g.pce_m)




if __name__ == '__main__':
    g = graph(1)
    g.create_order_graph()
    #graph_algorithms._print_matrix(g.m)
