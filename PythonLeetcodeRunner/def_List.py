
from typing import *


class ListNode:
    """ 若定义类内方法 import_from_$Data_Type, 在本地调试时会将$Data_Type表示的输入数据导入到类中. """
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def import_from(self, val: List):
        self.val = val[0]
        node = self
        for v in val[1:]:
            node.next = ListNode(v)
            node = node.next
        return self

    def export_to(self):
        vals = [self.val]
        node = self.next
        while node is not None:
            vals.append(node.val)
            node = node.next
        return vals

    def __str__(self):
        return f'{self.export_to()}'

    def __eq__(self, list_in):
        return list_in == self.export_to()
