class Link:
    """ A link for representing a doubly-linked list. """

    def __init__(self, value=None):
        self.value = value
        self.next = None
        self.prev = None

    def link_next(self, nxt):
        self.next = nxt
        nxt.prev = self

    def link_prev(self, prev):
        self.prev = prev
        prev.next = self

    def del_next(self, cleanup=True):
        old_next = self.next
        self.link_next(old_next.next)
        if cleanup:
            old_next.prev = None
            old_next.next = None

    def del_prev(self, cleanup=True):
        old_prev = self.prev
        self.link_prev(old_prev.prev)
        if cleanup:
            old_prev.prev = None
            old_prev.next = None
