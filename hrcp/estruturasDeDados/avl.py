from typing import List

class Node:
    '''
    Class that models a dinamic node of a binary tree.
    '''
    def __init__(self,value:object):
        '''
        Constructor that initializes a node with data and no children.
        The height of the node is set to 1 (leaf node)
        '''
        self.__value = value
        self.__left = None
        self.__right = None
        # attribute that specifies the height (balance factor of the node)
        self.__height = 1

    def __repr__(self):
        return f'<{self.__value}>'

    @property
    def value(self)->object:
        return self.__value

    @value.setter
    def value(self, newValue:object):
        self.__value = newValue

    @property
    def left(self)->'Node':
        return self.__left

    @left.setter
    def left(self, newLeftChild:object):
        self.__left = newLeftChild

    @property
    def right(self)->'Node':
        return self.__right

    @right.setter
    def right(self, newRightChild:'Node'):
        self.__right = newRightChild

    @property
    def height(self)->int:
        return self.__height

    @height.setter
    def height(self, newHeight:int):
        self.__height = newHeight

    def insertLeft(self, data:object):
        if self.__left == None:
            self.__left = Node(data)	

    def hasLeftChild(self)->bool:
        return self.__left != None

    def hasRightChild(self)->bool:
        return self.__right != None

    def insertRight(self,data:object):
        if self.__right == None:
            self.__right = Node(data)

    def __str__(self):
        #return f'{self.__data}'
        return f'|{self.__value}:h={self.__height}|'
    

  
# Classe AVL tree 
class AVLTree(object): 
    """ 
    Class that creates a AVL tree in memory. AVL tree is a self-balancing
    Binary Search Tree (BST) where the difference between heights
    of left and right subtrees cannot be more than one for all nodes. 

    Original source: 
        https://www.geeksforgeeks.org/avl-tree-set-1-insertion/
        https://www.geeksforgeeks.org/avl-tree-set-2-deletion/?ref=lbp
    Modifications, fixing bugs and new methods:
        Prof. Alex Cunha
    
    Author: Alex Cunha  
    Date of last modification: 31/10/2023
    Attributes
    ----------
    root: reference to the root node.
    """
    preorder  = 0
    inorder   = 1
    postorder = 2

    def __init__(self, value:object = None):
        """ 
        Constructor of the AVL tree object
        Arguments
        ----------------
        value (object): data to be added to AVL tree. If a value
                        is not provided, the tree initializes "empty".
                        Otherwise, a node with "value" is created as root.
        """
        self.__root = None if value is None else self.insert(value)

    def __repr__(self):
        return f"{self.__root=}"

    def getRoot(self)->any:
        '''
        Method that returns the object/value stored on root node.
        Returns
        ------------
        None if there is no root node, otherwise, returns the object/value stored
        on root node
        '''
        return None if self.__root is None else self.__root.value

    def isEmpty(self)->bool:
        '''
        Method that verifies AVL Tree is empty or not.
        Returns
        ---------
        True: AVL Tree is empty
        False: AVL Tree is not empty, i.e., there is at least a root node.
        '''
        return self.__root == None

    def height(self)->int:
        '''
        Returns the height of the tree.
        -1 if the tree is empty. The root node has height 0.
        '''
        return self.__height(self.__root)
    
    def __height(self, root:Node)->int:
        if root is None:
            return -1
        else:
            return 1 + max(self.__height(root.left), self.__height(root.right))

    def search_all(self, key: any) -> list:
        """
        Perform a search in AVL Tree to find all nodes whose key is equal to the "key" argument.

        Returns
        ----------
        An empty list if the key was not found or AVL Tree is empty. Otherwise, returns
        a list of all values stored at the corresponding key nodes.
        """
        results = []
        if self.__root is not None:
            self.__search_all(key, self.__root, results)
        return results

    # def __search_all(self, key: any, node: Node, results: list):
    #     """
    #     Private method that performs a recursive search in AVL Tree to find all nodes
    #     whose key is equal to "key" argument.

    #     Arguments
    #     ------------
    #     key (any): the key value to be searched in AVL Tree
    #     node (Node): the node to be used as reference to start the search
    #     results (list): list to store found values
    #     """
    #     if node is None:
    #         return
        
    #     if key == node.value:
    #         results.append(node.value)
    #         self.__search_all(key, node.right, results)
        
    #     if key < node.value:
    #         self.__search_all(key, node.left, results)
        
    #     if key > node.value:
    #         self.__search_all(key, node.right, results)
    def __search_all(self, key: any, node: Node, results: list):
        """
        Private method that performs a recursive search in AVL Tree to find all nodes
        whose key is equal to "key" argument.
        """
        if node is None:
            return

        if key == node.value:
            results.append(node.value)
            self.__search_all(key, node.left, results)  # Buscar na esquerda também!
            self.__search_all(key, node.right, results)

        elif key < node.value:
            self.__search_all(key, node.left, results)

        else:  # key > node.value
            self.__search_all(key, node.right, results)
    def search(self, key:any )->any:
        '''
        Perform a search in AVL Tree to find the node whose key is equal to "key" argument.
        Returns
        ----------
        None if the key was not found or AVL Tree is empty. Otherwise, returns
        the object/value stored at the corresponding key node.
        '''
        if( self.__root != None ):
           node = self.__searchData(key, self.__root)
           return node.value if node is not None else None
        else:
            return None
    
    def __searchData(self, key:any, node:Node)->Node:
        '''
        Private method that performs a recursive search in AVL Tree to find the node 
        whose key is equal to "key" argument.
        
        Arguments
        ------------
        key (any): the key value to be searched in AVL Tree
        node (Node): the node to be used as reference to start the search 
        Returns
        ----------
        None if the key was not found or AVL Tree is empty. Otherwise, returns
        the object/value stored at the node corresponding the key.
        '''
        if ( key == node.value):
            return node
        elif ( key < node.value and node.left != None):
            return self.__searchData( key, node.left)
        elif ( key > node.value and node.right != None):
            return self.__searchData( key, node.right)
        else:
            return None

    def __len__(self)->int:
        '''Method that returns the number of nodes of this AVL tree
        Returns
        -------------
        int: the number of nodes of the tree.
        '''
        return self.__count(self.__root)

    def __count(self, node:Node)->int:
        if ( node == None):
            return 0
        else:
            return 1 + self.__count(node.left) + self.__count(node.right)


    def add(self, value:object):
        '''
        Insert a new node in AVL Tree recursively from root.
        AVL tree is a self-balancing Binary Search Tree (BST) where the 
        difference between heights of left and right subtrees cannot be 
        more than one for all nodes.
        The given tree remains AVL after every insertion after re-balancing.

        Parameters
        ----------
        data (any): the data to be stored in the new node.
        '''
        if(self.__root == None):
            self.__root = Node(value)
        else:
            self.__root = self.__add(self.__root, value)
  
    def __add(self, root:Node, key:any):
        # Step 1 - Performs a BST recursion to add the node in 
        # the right place
        if not root: 
            return Node(key) 
        elif key < root.value: 
            root.left = self.__add(root.left, key) 
        else: 
            root.right = self.__add(root.right, key) 
  
        # Step 2 
        # The current node must be one of the ancestors of the newly
        # inserted node. Thus, update the height of the current node
        root.height = 1 + max(self.__getHeight(root.left), 
                              self.__getHeight(root.right)) 
  
        # Step 3 - Computes the balance factor 
        # (left subtree height – right subtree height) of the current node
        balance = self.__getBalance(root) 
  
        # Step 4 - Checks if the node is unbalanced
        # Then, one of the following actions will be performed:

        # CASE 1 - Right rotation
        if balance > 1 and key < root.left.value: 
            return self.__rightRotate(root) 
  
        # CASE 2 - Left rotation
        if balance < -1 and key > root.right.value: 
            return self.__leftRotate(root) 
  
        # CASE 3 - Double rotation: Left-> Right 
        if balance > 1 and key > root.left.value: 
            root.left = self.__leftRotate(root.left) 
            return self.__rightRotate(root) 
  
        # CASE 4 - Double rotation: Right-> Left 
        if balance < -1 and key < root.right.value: 
            root.right = self.__rightRotate(root.right) 
            return self.__leftRotate(root) 
  
        return root 
  
    def __leftRotate(self, p:Node)->Node: 
        """
        Perform a left rotation taking the node "p" as base
        to make "u" the new root.
        T1, T2 and T3 are subtrees of the tree, rooted with P (on the left
        side). Keys in both of the above trees follow the following order:
        keys(T1) < key(P) < keys(T2) < key(u) < keys(T3).
        So BST property is not violated anywhere
        """
        #     p                                 u
        #    / \                               /  \
        #   T1  u                             p    T3 
        #      / \     < - - - - - - -       / \  
        #     T2 T3    Left Rotation        T1 T2 
        
        u = p.right 
        T2 = u.left 
  
        # Perform rotation 
        u.left = p 
        p.right = T2 
  
        # Update heights 
        p.height = 1 + max(self.__getHeight(p.left), 
                         self.__getHeight(p.right)) 
        u.height = 1 + max(self.__getHeight(u.left), 
                         self.__getHeight(u.right)) 
  
        # Return the new root "u" node 
        return u 
  
    def __rightRotate(self, p:Node)->Node: 
        """ 
        Perform a right rotation taking the node "p" as base
        to make "u" the new root.        
        T1, T2 and T3 are subtrees of the tree, rooted with p 
        (on the right side). Keys in both of the above trees follow the following order:
        Keys()
        """
        # keys(T1) < key(u) < keys(T2) < key(p) < keys(T3).
        # So BST property is not violated anywhere
        #      p                               u
        #     / \     Right Rotation          /  \
        #    u   T3   - - - - - - - >        T1   p 
        #   / \                                  / \
        #  T1  T2                               T2  T3
        
        u = p.left 
        T2 = u.right 
  
        # Perform rotation 
        u.right = p 
        p.left = T2 
  
        # Update heights 
        p.height = 1 + max(self.__getHeight(p.left), 
                        self.__getHeight(p.right)) 
        u.height = 1 + max(self.__getHeight(u.left), 
                        self.__getHeight(u.right)) 
  
        # Return the new root ("u" node)
        return u 
  
    def __getHeight(self, node:Node)->int: 
        """ 
        Gets the height of the node passed by argument.
        Arguments:
        -----------
        node (Node): the node to be used as reference to get the height

        Returns
        -----------
        Returns an integer representing the height of the node.  
        A value 0 means that the not exists the node.
        """
        if node is None: 
            return 0
  
        return node.height 
  
    def __getBalance(self, node:Node)->int: 
        """
        Compute the balance factor of a node. The balance factor is 
        defined as:
        balance = height(left subtree) - height(right subtree)

        Arguments
        -----------
        node (object): the node to be used as reference to calculate
                      the balance factor


        Returns
        -----------
        Returns the balance factor of the node passed by argument.
        A value 0, +1 or -1 indicates that the node is balanced.
        """
        if not node: 
            return 0
  
        return self.__getHeight(node.left) - self.__getHeight(node.right) 

    def __getMinValueNode(self, root:Node)->Node:
        """
        Get the node with the minimum value from node key
        Arguments
        ------------
        root (Node): the node to be used as reference to traverse the nodes
                     always to the left and get the minimum value
        Returns
        ------------
        The node with the minimum value
        """
        if root is None or root.left is None:
            return root
 
        return self.__getMinValueNode(root.left)
    
    def __getMaxValueNode(self, root:Node)->Node:
        """
        Get the node with the maximum value from node key
        Arguments
        ------------
        root (Node): the node to be used as reference to traverse the nodes
                     always to the right and get the maximum value
        Returns
        ------------
        The node with the maximum value 
        """
        if root is None or root.right is None:
            return root
 
        return self.__getMaxValueNode(root.right)  


    def delete(self, key:object):
        '''
        Perform a delete operation of the specified key in AVL Tree
        Arguments  
        ------------
        key (object): the key value to be deleted from AVL Tree
        '''
        if(self.__root is not None):
            node = self.__searchData(key, self.__root)
            load = node.value if node is not None else None
            self.__root = self.__delete(self.__root, key)
            if load is None:
                return None
            else:
                return load
        else:
            return None


    def __delete(self, root:Node, key:object)->Node: 
        """
        Recursive function to delete a node with given key from subtree
        with given root.

        Retorno
        --------------
        It returns root of the modified subtree.
        """
        # Step 1 - Perform standard BST delete 
        if not root: 
            return root   
        elif key < root.value: 
            root.left = self.__delete(root.left, key)   
        elif key > root.value: 
            root.right = self.__delete(root.right, key)   
        else: 
            if root.left is None: 
                temp = root.right 
                root = None
                return temp 
  
            elif root.right is None: 
                temp = root.left 
                root = None
                return temp 
  
            temp = self.__getMinValueNode(root.right) 
            root.value = temp.value 
            root.right = self.__delete(root.right, 
                                      temp.value) 
  
        # If the tree has only one node, 
        # simply return it 
        if root is None: 
            return root 
  
        # Step 2 - Update the height of the  
        # ancestor node 
        root.height = 1 + max(self.__getHeight(root.left), 
                            self.__getHeight(root.right)) 
  
        # Step 3 - Get the balance factor 
        balance = self.__getBalance(root) 
  
        # Step 4 - If the node is unbalanced,  
        # then try out the 4 cases 
        # Case 1 - Left Left 
        if balance > 1 and self.__getBalance(root.left) >= 0: 
            return self.__rightRotate(root) 
  
        # Case 2 - Right Right 
        if balance < -1 and self.__getBalance(root.right) <= 0: 
            return self.__leftRotate(root) 
  
        # Case 3 - Left Right 
        if balance > 1 and self.__getBalance(root.left) < 0: 
            root.left = self.__leftRotate(root.left) 
            return self.__rightRotate(root) 
  
        # Case 4 - Right Left 
        if balance < -1 and self.__getBalance(root.right) > 0: 
            root.right = self.__rightRotate(root.right) 
            return self.__leftRotate(root) 
  
        return root  

    def clear(self):
        '''
        Deletes all nodes of the tree.
        '''
        # garbage collector will do the work of removing the nodes automatically.
        self.__root = None

    def __str__(self):
        '''
        Returns a string representation of the AVL Tree
        '''
        return self.__strPreOrder(self.__root)
    
    def __strPreOrder(self, root:Node)->str:
        if root is None:
            return ''
        else:
            return f'{root} {self.__strPreOrder(root.left)} {self.__strPreOrder(root.right)}'
    
    def build(self,values:List[any]):
        '''
        Builds a balanced binary search tree in the order the nodes appear in
        the list.        
        Precondition: the tree must be empty

        Arguments
        ---------
        values (List[any]): the list of values to be inserted in 
        the tree.
        '''
        if not values or self.__root != None:
            return None 

        for element in values:
            self.add(element)
    
    def __iter__(self):
        '''
        Returns an iterator for the tree.
        '''
        self.__stack = [self.__root]
        return self

    def __next__(self):
        '''
        Returns the next node in the iteration.
        '''
        if not self.__stack:
            raise StopIteration
        node = self.__stack.pop()
        if node.right:
            self.__stack.append(node.right)
        if node.left:
            self.__stack.append(node.left)
        return node.value

    def __contains__(self, key:any)->bool:
        '''
        Verifies if a key is present in the tree.
        Method is called when the operator "in" is used.
        '''
        value = self.search(key)
        return True if value else None
    
    def buscar_reservas_por_cpf(self, usuario):
        reservas = []
        if self.getRoot:  # Verifica se a árvore não está vazia
            self._buscar_reservas_por_cpf(self.root, usuario.cpf, reservas)
        return reservas


    def _buscar_reservas_por_cpf(self, node, cpf, reservas):
        if node is not None:
            # Verifica se o CPF do nó atual é o que estamos buscando
            if node.reserva.cpf_usuario == cpf:
                reservas.append(node.reserva)
            # Continua buscando nas subárvores esquerda e direita
            self._buscar_reservas_por_cpf(node.esquerda, cpf, reservas)
            self._buscar_reservas_por_cpf(node.direita, cpf, reservas)


            
if __name__ == "__main__":
    class Reserva:
        def __init__(self, quarto, periodo, cliente):
            self.quarto = quarto
            self.periodo = periodo
            self.cliente = cliente
            
        def __lt__(self, o):
            return self.periodo <  o.periodo
        
        def __eq__(self, o):
            return self.periodo == o.periodo
            
        def __str__(self):
            return f"{self.quarto=} {self.periodo=} {self.cliente=}"
        
        def __repr__(self):
            return f"{self.quarto=} {self.periodo=} {self.cliente=}"
        
    import random
    # Gera varias reservas aleatorias
    objetos = [Reserva(*(random.sample(range(30), 3))) for _ in range(10)]

    a = AVLTree()

    # Coloca esses objetos na AVL
    for o in objetos:
        a.add(o)
        
    # Adiciona algumas reservas com o periodo 1
    a.add(Reserva(0, 1, 32))
    a.add(Reserva(1, 1, 32))
    a.add(Reserva(2, 1, 32))
        
    # Procuro 1 reserva como periodo 1
    print("Primeira busca ---")   
    print(a.search(Reserva(0, 1, 0)))

    # Procuro todas as reservas com o periodo 1
    # (obs: coloquei o *map(str, ...))) so para ficar visualizável, mas nao precisa)
    print("\nSegunda busca ---")   
    print(*map(str, a.search_all(Reserva(0, 1, 0))), sep="\n")

    # Busco por um valor ou mais valores especificos
    valores = []
    for i in a:
        if i.quarto == 2:
            valores.append(i)
            
    print("\nTerceira busca ---")   
    print(*map(str, valores), sep="\n")