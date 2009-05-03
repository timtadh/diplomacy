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

def dislodge(pce_id, ter_id, exclude):
    """ Moves specified piece to a territory adjacent to ter_id but not in exclude.
        Returns True if successful, False if not.
    """
    for adj_ter in db.callproc('terr_adj', ter_id):
        #print adj_ter
        if not db.callproc('terr_occupied', adj_ter['ter_id']) and adj_ter['ter_id'] not in exclude:
            db.callproc('move_piece', pce_id, adj_ter['ter_id'])
            return True
    return False

def execute(pce_id):
    """So far, only supports move orders"""
    order = db.callproc('orders_for_piece', pce_id)
    if order and order[0]['order_type'] == 1:
        db.callproc('move_piece', pce_id, order[0]['destination'])
        print "Move order by", pce_id, "executed<br>"

class graph(object):
    def __init__(self, gam_id):
        self.gam_id = gam_id
        self.terr_list = sorted(
            [int(row['ter_id']) for row in db.callproc('terrs_in_game', gam_id)]
        )
        self.terr_map = dict(zip(self.terr_list, xrange(len(self.terr_list))))
        #self.terr_map = dict([(self.terr_list[i], i) for i in xrange(len(self.terr_list))])
        self.ter_m = [[0 for x in xrange(len(self.terr_list))] for y in xrange(len(self.terr_list))]
        for ter_id in self.terr_list:
            for row in db.callproc('terr_adj', ter_id):
                ter = self.terr_map[ter_id]
                adj = self.terr_map[row['ter_id']]
                self.ter_m[ter][adj] = 1
            self.ter_m[ter][ter] = 1
        
        self.get_orders()
        self.create_moves()
        self.create_supports()
    
    def get_orders(self):
        self.pieces_info = dict([(int(p['pce_id']), p) for p in db.callproc('pieces_for_game', self.gam_id)])
        self.pieces = [k for k in self.pieces_info.keys()]
        self.pieces.sort()
        self.piece_map = dict([(pce_id, i) for i, pce_id in enumerate(self.pieces)])
        
        self.orders = db.callproc('orders_for_game', self.gam_id)
        self.operands = db.callproc('operands_for_game', self.gam_id)
        
        #print self.pieces
        self.loc_pce = dict([
                        (int(self.pieces_info[pce_id]['ter_id']), i) 
                                for i, pce_id in enumerate(self.pieces)
                        ])
        self.pce_loc = dict([
                        (self.loc_pce[ter_id], ter_id) 
                                for ter_id in self.loc_pce.keys()
                        ])
        #print self.loc_pce, self.pce_loc
        self.dst_pce = dict([
                        (int(o['destination']), self.piece_map[int(o['pce_id'])]) 
                                for o in self.orders 
                                if o['destination'] != None
                        ])
        self.pce_dst = dict([
                        (self.dst_pce[ter_id], ter_id) 
                                for ter_id in self.dst_pce.keys()
                        ])
        #print self.dst_pce, self.pce_dst
        #self.op_pce = dict([
                        #(int(o['ter_id']), self.piece_map[int(o['pce_id'])]) 
                                #for o in self.operands if o['ter_id'] and o['pce_id']
                        #])
        #self.pce_op = dict([
                        #(self.op_pce[ter_id], ter_id) 
                                #for ter_id in self.op_pce.keys()
                        #])
        #print self.op_pce, self.pce_op
        
        self.pce_m = [[0 for x in xrange(len(self.pieces))] for y in xrange(len(self.pieces))]
        
    
    def create_moves(self):
    
        for i, pce_id in enumerate(self.pieces):
            for row in db.callproc('orders_for_piece', pce_id):
                dst = row['destination']
                order_type = int(row['order_type'])
                if dst and order_type == 1:
                    #print order_type, len(db.callproc('orders_for_piece', pce_id)), pce_id
                    if self.loc_pce.has_key(dst) and self.loc_pce[dst] != i:
                        self.pce_m[i][self.loc_pce[dst]] = 1
                    for o in self.orders:
                        if o['destination'] == dst and o['order_type'] == 1\
                           and self.piece_map[int(o['pce_id'])] != i:
                            self.pce_m[i][self.piece_map[int(o['pce_id'])]] = 1
                            
                        #print i, self.dst_pce[dst], len(self.pce_m[i])
        
        graph_algorithms._print_matrix(self.pce_m)
    
    def create_supports(self):
    
        for i, pce_id in enumerate(self.pieces):
            for row in db.callproc('orders_for_piece', pce_id):
                dst = row['destination']
                order_type = int(row['order_type'])
                if dst and order_type == 2:
                    operands = db.callproc('operands_for_piece', pce_id)
                    if len(operands) == 1:
                        sup_pce = operands[0]['ter_id']
                        if not self.loc_pce.has_key(sup_pce): continue
                        sup_pce = self.loc_pce[sup_pce]
                        sup_orders = db.callproc('orders_for_piece', self.pieces[sup_pce])
                        if not sup_orders: continue
                        sup_dst = sup_orders[0]['destination']
                        if sup_dst != dst or sup_pce == i: continue
                        
                        self.pce_m[i][sup_pce] = 2
                    #print order_type, len(db.callproc('orders_for_piece', pce_id)), pce_id
                    #if self.loc_pce.has_key(dst) and self.loc_pce[dst] != i:
                        #self.pce_m[i][self.loc_pce[dst]] = 1
                    #for o in self.orders:
                        #if o['destination'] == dst and o['order_type'] == 2\
                           #and self.piece_map[int(o['pce_id'])] != i:
                            #self.pce_m[i][self.piece_map[int(o['pce_id'])]] = 2
                            
                        #print i, self.dst_pce[dst], len(self.pce_m[i])
        
        graph_algorithms._print_matrix(self.pce_m)
    
    def step_one(self):
        count = 0
        for i in xrange(len(self.pce_m)):
            conflicts = False
            break_sup = False
            for j in xrange(len(self.pce_m)):
                if self.pce_m[i][j] != 0:  conflicts = True
                if self.pce_m[j][i] != 0:  break_sup = True
            #if not conflicts: count += 1; execute_order(self.pieces[i])
            if break_sup:
                for j in xrange(len(self.pce_m)):
                    if self.pce_m[i][j] == 2: self.pce_m[i][j] = 0
        #print count
    
    def adj(self, v):
        a = list()
        for j in xrange(len(self.pce_m)):
            if self.pce_m[v][j] != 0:  a.append(j)
        return a
        
    def sup(self, v):
        s = 1
        for j in xrange(len(self.pce_m)):
            if self.pce_m[j][v] == 2: s += 1
        return s
    
    def dfs(self):
        color = [0 for i in self.pieces]
        path = [None for i in self.pieces]
        
        def dfs_visit(v):
            color[v] = 1
            print v
            for u in self.adj(v):
                if color[u] == 0:
                    path[u] = v
                    dfs_visit(u)
            color[v] = 2
        
        for v in xrange(len(self.pce_m)):
            #print v, color[v], path[v], self.adj(v)
            if color[v] == 0:
                dfs_visit(v)
        
    
    def step_two(self, dont=False):
        dislodged = set()
        exe = set()
        color = [0 for i in self.pieces]
        path = [None for i in self.pieces]
        
        def dfs_visit(v):
            color[v] = 1
            #print v-
            max_sup = 0
            for u in self.adj(v):
                if color[u] == 0:
                    path[u] = v
                    dfs_visit(u)
                if self.sup(u) > max_sup: max_sup = self.sup(u)
            color[v] = 2
            
            print v, self.sup(v), max_sup, self.sup(v) > max_sup
            if self.sup(v) > max_sup: 
                exe.add(v)
                for u in self.adj(v):
                    #print self.pce_loc[u],
                    #print self.pce_dst[v]
                    #print self.pce_m[v][u],
                    if self.pce_m[v][u] == 1 and self.pce_loc[u] == self.pce_dst[v]: dislodged.add(u)
                #print
            
        
        for v in xrange(len(self.pce_m)):
            #print v, color[v], path[v], self.adj(v)
            if color[v] == 0:
                dfs_visit(v)
        print path
        print exe - dislodged
        for pce in list(exe - dislodged):
            if not dont: execute(self.pieces[pce])
        for pce in list(dislodged):
            if not dont: dislodge(self.pieces[pce], self.pieces_info[self.pieces[pce]]['ter_id'], 
                                  [self.pieces[p] for p in list(exe - dislodged)])
        print dislodged

def resolve(gam_id):
    g = graph(gam_id)
    g.step_one()
    #graph_algorithms._print_matrix(g.pce_m)
    g.step_two()

if __name__ == '__main__':
    pass
    #dislodge(1, 5)
    g = graph(1)
    g.step_one()
    graph_algorithms._print_matrix(g.pce_m)
    g.step_two(True)
    #g.create_order_graph()
