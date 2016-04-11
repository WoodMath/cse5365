v_indice_start=[]
v_group_size=[]
arr_vert_list=[]
def test_function(v_vert_group):
    ## Performs a prefix sort / radix sort
    ## Cycles through an array of 2 element arrays such to insert an array [x,y] such that
    ##      All elements x are no less than the elements x before it.
    ##      For any given x, all elements y are no less than the elements y before it
    ##      Think [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]
#    print(' *** New Call *** ')
#    print(' v_indice_start = ' + str(v_indice_start))
#    print(' v_group_size = ' + str(v_group_size))
#    print(' arr_vert_list = ' + str(arr_vert_list))

    i_current_vert_group = v_vert_group[0]
#    print(' i_current_vert_group = ' + str(i_current_vert_group))
    i_current_vert_group_count = len(v_indice_start)
#    print(' i_current_vert_group_count = ' + str(i_current_vert_group_count))
    
    if(i_current_vert_group < i_current_vert_group_count):
        if(v_indice_start[i_current_vert_group] == -1):
            ## First edge in group (with v_vert_group[0])
#            print(' Group ' + str(i_current_vert_group) + ' not found')
            i_found = -1
            i_previous_group = -1
            ## Find previous group
            for i_inc in range(0,i_current_vert_group):
#                print(' i_inc = ' + str(i_inc) + ' ; v_indice_start[i_inc] = ' + str(v_indice_start[i_inc] ))
                if(v_indice_start[i_inc] > -1):
                    i_previous_group = i_inc;
                    i_found = i_inc;

#                print(' i_found = ' + str(i_found))
#                print(' i_previous_group = ' + str(i_previous_group))
            if(i_found == -1):                                      ## No previous start found
                i_start = 0                                         ## Just use 0
            else:                                                   ## Otherwise
                i_start = \
                        v_indice_start[i_previous_group] + v_group_size[i_previous_group]
                ## Use start of Previous group start Plus previous group size

            v_indice_start[i_current_vert_group] = i_start          ## Set group start for first time

            ## Inser occurs at group start
            i_ins = v_indice_start[i_current_vert_group]
#            print(' i_ins = ' + str(i_ins))
#            print(' i_start = ' + str(i_start))
            
        else:
            ## Get elements to cycle throug
            i_index_start = v_indice_start[i_current_vert_group]
            i_index_stop = i_index_start + v_group_size[i_current_vert_group]

            i_found = -1
            print(' i_index_start = ' + str(i_index_start) + ' ; i_index_stop = ' + str(i_index_stop))
            for i_inc in range(i_index_start, i_index_stop):
                print(' i_inc = ' + str(i_inc))
                v_test = arr_vert_list[i_inc]
                if(v_test[0] != i_current_vert_group):   ## Something happended causing to go outside the current group
                    ValueError(' Something bad happened: v_test[0] = ' + str(v_test[0]) + \
                               ' Not the same as i_current_vert_group = ' + str(i_current_vert_group))
                print(' v_vert_group = ' + str(v_vert_group) + ' ; v_test = ' + str(v_test))
                if(v_test[1] == v_vert_group[1]):       ## Dubplicate is being inserted
                    i_ins = -1                          ## Do not insert
                    i_found = i_inc                     ## Place found
                    break
                    print(' got here ');
                if(v_test[1] > v_vert_group[1]):
                    i_ins = i_inc                       ## Insert occurs at place it fails
                    i_found = i_inc                     ## Place found
                    break
                
            if(i_found == -1):                          ## No insert place found    
                i_ins = i_inc + 1                       ## Choose next spot
                i_found = i_ins
        
    else:
        ## Keep adding dummy elemends
        for i_inc in range(i_current_vert_group_count,i_current_vert_group):
            v_indice_start.append(-1)                   ## To start indice array
            v_group_size.append(0)                      ## And group size array

        i_ins = len(arr_vert_list)                      ## Set insert position as end of vertice list

        v_indice_start.append(i_ins)                    ## Set the start to this position
        v_group_size.append(0)                          ## Still keeping group size as 0 because element hasn't been appendied to vertice list yet

    i_current_vert_group_count = len(v_indice_start)    ## Restablish group count
#    print(' i_current_vert_group_count = ' + str(i_current_vert_group_count))

    
    if(i_ins > -1):
        arr_vert_list.insert(i_ins,v_vert_group)        ## Insert actual vertex
        
        (v_group_size[i_current_vert_group]) += 1       ## Increase the group size by 1

        for i_inc in range(i_current_vert_group+1, i_current_vert_group_count):
            (v_indice_start[i_inc]) += 1                ## Increment starting index of remaining group
            

#    print(' v_indice_start = ' + str(v_indice_start))
#    print(' v_group_size = ' + str(v_group_size))
#    print(' arr_vert_list = ' + str(arr_vert_list))
        
    

#test_function([0,0])

#test_function([5,0])

#test_function([3,0])

#test_function([7,0])

#test_function([7,5])

#test_function([3,5])

#test_function([3,7])

#test_function([3,3])

#test_function([3,5])


#print(' v_indice_start = ')
#print(v_indice_start)

#print(' v_group_size = ')
#print(v_group_size)

#print(' arr_vert_list = ')
#print(arr_vert_list)


v_test_vert = [[0,0,0,1],\
               [0,1,0,1],\
               [1,1,0,1],\
               [1,0,0,1]]\
               
v_test_ind = [[0,1],\
              [1,2],\
              [2,3],\
              [3,0]]

def seperate_points(v_vertices, v_indices ):
    v_out_vertices=[]
    v_out_indices=[]
    i_index = 0
    for i_inc in range(0,len(v_indices)):
        i_index_one = v_indices[i_inc][0]
        i_index_two = v_indices[i_inc][1]
        v_vertex_one = v_vertices[i_index_one]
        v_vertex_two = v_vertices[i_index_two]
        
        v_out_vertices.append(v_vertex_one)
        v_out_vertices.append(v_vertex_two)

        v_out_indices.append([i_index,i_index+1])
        i_index += 2
    
    return (v_out_vertices,v_out_indices)


test = seperate_points(v_test_vert, v_test_ind)
        
