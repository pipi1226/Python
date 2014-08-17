import json
import types
js_file = json.load(file('***.json'))


huffman_dict={}
huffman_result={}


maxn = 1000
maxint = 9999999999

class TreeNode(object):
    def __init__(self,w=maxint,pos=0,key=''):
        self.w = w
        self.pos = pos
        self.key = key

class TreeType():
    def __init__(self, prt=-1, lch=-1, rch=-1,w=0,key=''):
        self.prt = prt
        self.lch = lch
        self.rch = rch
        self.w = w
        self.key = key

counts = 0

nodes = [TreeNode()]*(maxn)
for i in range(maxn):
    nodes[i] = TreeNode(maxint, i,'')


trees = [TreeType()]*(2*maxn-1)
for i in range(2*maxn-1):
    trees[i] = TreeType(-1, -1, -1,maxint,'')


class Huffman():
    #get the total number of keys from dict
    def tt(self,sub_dict,num):
        if(isinstance(sub_dict,list)):
            for tmp in range(len(sub_dict)):
                if(type(sub_dict[tmp]) is types.DictType):
                    self.tt(sub_dict[tmp],num+1)
                if(isinstance(tmp,list)):
                    self.tt(sub_dict[tmp],num+1)

        if(isinstance(sub_dict,dict)):
            for ks,vls in sub_dict.iteritems():
                if(ks in huffman_dict.keys()):
                    huffman_dict[ks]+=1
                else:
                    huffman_dict[ks]=1
                if(type(vls) is types.DictType):
                    vs_c = vls
                    self.tt(vs_c,num+1)
                if(isinstance(vls,list)):
                    vs_c = vls
                    self.tt(vls,num+1)

    #Translate the dict to nodes
    def compute_frequency(self):
        count = 1
        for kk, vv in huffman_dict.iteritems():
            nodes[count].w = vv
            nodes[count].key = kk
            nodes[count].leaf = 1
            count += 1
        return count

    def print_frequency(self,counts):
        print "in print_frequency function counts=",counts
        for i in range(1,counts,1):
            print nodes[i].key,nodes[i].w

    #building min-heap
    def heap(self, s, n):
        j = 1
        print "heap function"
        while(j != maxint):
            i = nodes[s].w
            j = maxint
            if(s*2 <= n):
                if(nodes[2*s].w <= i and nodes[2*s].key == ''):
                    i = nodes[2*s].w
                    j = s*2
                if(nodes[2*s].w < i):
                    i = nodes[2*s].w
                    j=s*2
    
            if((s*2+1) <= n):
                if(nodes[2*s+1].w <= i and nodes[2*s+1].key == ''):
                    i = nodes[2*s+1].w
                    j = s*2+1
                if(nodes[s*2+1].w < i):
                    i = nodes[2*s+1].w
                    j=s*2+1
                
            if(j!=maxint):
                temp = nodes[s]
                nodes[s] = nodes[j]
                nodes[j] = temp
                s=j
                
    # Calculate the Optimal Binary Tree
    def calc_tree(self, total):
        print "calc_tree"
        for i in range(1,total+1,1):
            print "i=",i,"key=",nodes[i].key,"w=",nodes[i].w,"pos=",nodes[i].pos
        
        # build min-heap
        tot = total
        for i in range(total/2,0,-1):
            self.heap(i, tot)
 
        #print "after heap---------------"
        for i in range(1,total+1,1):
            trees[nodes[i].pos].w=nodes[i].w
            trees[nodes[i].pos].key=nodes[i].key

        #print "begin to huffman operation----------------"
        tot = total
        for i in range(tot+1, 2*tot, 1):
            #t1 = nodes[1], take out the top element of the min-heap
            t1 = TreeNode(nodes[1].w, nodes[1].pos,nodes[1].key)
            #nodes[1] = nodes[tot], move the last element of the min-heap to the top
            nodes[1] =  TreeNode(nodes[tot].w, nodes[tot].pos,nodes[tot].key)

            tot -= 1
            #print "---------------------before first heap------------------"
            #for ii in range(1,tot+1,1):
                #print 'i=',i,"ii=",ii,"key=",nodes[ii].key,"w=",nodes[ii].w,"pos=",nodes[ii].pos

            #--------modify heap----------
            self.heap(1, tot)

            #print "--------------------after first heap------------------"
            #for ii in range(1,tot+1,1):
                #print 'i=',i,"ii=",ii,"key=",nodes[ii].key,"w=",nodes[ii].w,"pos=",nodes[ii].pos

            #label t1's position of the binary tree
            trees[t1.pos].prt = i
            trees[i].lch = t1.pos
            #t2 = nodes[1], take out the top element of the min-heap
            t2 = TreeNode(nodes[1].w, nodes[1].pos,nodes[1].key)
        
            #add the new node to the heap
            tot += 1
            nodes[tot] = TreeNode(t1.w+t2.w, i, '')

            #nodes[1]=nodes[tot], move the last element of the min-heap to the top
            nodes[1] = TreeNode(nodes[tot].w, nodes[tot].pos,nodes[tot].key)

            tot -= 1

            #print "---------------------before second heap------------------"
            #for ii in range(1,tot+1,1):
                #print 'i=',i,"ii=",ii,"key=",nodes[ii].key,"w=",nodes[ii].w,"pos=",nodes[ii].pos

            self.heap(1, tot)

            #print "-------------------after second heap-------------------------"
            #for ii in range(1,tot+1,1):
                #print 'i=',i,"i=",ii,"key=",nodes[ii].key,"w=",nodes[ii].w,"pos=",nodes[ii].pos
            #too = input("second heap")

            #label t2's position of the binary tree, and label the ith node's left child and right child
            trees[t2.pos].prt = i
            trees[i].rch = t2.pos
            trees[i].w = t1.w+t2.w
            trees[i].key = ''
        #print "combine heap"
        #sos = total
        #for i in range(1,2*sos,1):
            #print "trees position i=",i,"key=",trees[i].key,"w=",trees[i].w,"prt=",trees[i].prt,"lch=",trees[i].lch,"rch=",trees[i].rch
        
    def calc_code(self, n):
        for i in range(1,n+1,1):
            cd = ''
            f = trees[i].prt
            c = i
            while(f != -1):
                if(trees[f].lch == c):
                    cd = '0'+cd
                else:
                    cd = '1'+cd
                c = f
                f = trees[f].prt
            huffman_result[trees[i].key]=cd
            #huffman_result[trees[i].key]=Bi2De(cd)
        print "code:"
        for i in range(1,n+1,1):
            kk = trees[i].key
            vv = huffman_result[kk]
            #print "w=",trees[i].w,"keys=",kk,"code=",vv,"code(decimal)=",self.Bi2De(vv)
            print "w=",trees[i].w,"keys=",kk,"code=",vv,"code(decimal)=",int(vv,2)

    #decode the number to string
    def calc_decode(self,num,n):
        print "in decode function"
        s = bin(num)[2:]
        #print s
        flag = 0
        for k,values in huffman_result.iteritems():
            if(s == values):
                flag = 1
        if(flag == 0):
            return "failed!"
        else:
            s = s+'.'
            s1 = ''
            i = 0
            while(s[i] != '.' ):
                l = 2*n-1
                while(trees[l].lch != -1):
                    if(s[i] == '0'):
                        l = trees[l].lch
                    else:
                        l = trees[l].rch
                    i += 1
            s1 = trees[l].key
            return s1
        


    
huf_test = Huffman()
huf_test.array = {}
huf_test.tt(js_file,1)
cc = huf_test.compute_frequency()

huf_test.calc_tree(cc-1)
huf_test.calc_code(cc-1)
#1001011000 decode test
#huf_test.calc_decode("1001011000",cc-1)
decodes = huf_test.calc_decode(999,cc-1)
print decodes
decodes = huf_test.calc_decode(602,cc-1)
print decodes
