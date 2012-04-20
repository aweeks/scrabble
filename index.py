class Node(dict):
    def __init__(self, prefix=""):
        self.prefix = prefix
        self.final = False

    def find(self, s):
        return self.find_helper(s, 0)
            
    def find_helper(self, s, n):
        if n < len(s):
            if not s[n] in self:
                return None
            else:
                return self[s[n]].find_helper(s, n+1)
        else:
            return self

    def insert(self, s):
        self.insert_helper(s, 0)

    def insert_helper(self, s, n):
        if n < len(s):
            branch = self.get( s[n], Node(prefix=self.prefix+s[n]) )
            branch.insert_helper(s, n+1)
            self[s[n]] = branch
        else:
            self.final=True
    

    def contains(self, s):
        return self.contains_helper(s, 0)

    def contains_helper(self, s, n):
        if n < len(s):
            if not s[n] in self:
                return False
            else:
                return self[s[n]].contains_helper(s, n+1)
        else:
            return self.final

