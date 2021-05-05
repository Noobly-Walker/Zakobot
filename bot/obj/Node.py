class Node:
    def __init__(self):
        self.name = "something generated"
        self.parent = None
        self.child = None
    def addChild(child):
        if self.child == None:
            self.child = {}
            self.child[child.name] = child      # Set the child object as your own.
        if self.child.parent == None:
            child.setParent(self)             # Set yourself as the child object's new parent.
    def setParent(parent):
        if self.parent == None:
            self.parent = parent              # Set the parent object as your own.
        if parent.child not None and self.name not in parent.child.keys:
            self.parent.child[name] = self    # Set yourself as the parent object's new child.
