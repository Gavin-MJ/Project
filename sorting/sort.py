
class ProductNode:
    """ Node for Linked List """

    def __init__(self, data):
        self.data = data
        self.next_node = None

class ProductLinkedListSorter:
    """ Linked List Sorter """

    def __init__(self, sort_lowest_first=True):
        self.sort_lowest_first = sort_lowest_first

    def sort_products(self, products):
        head = None
        for product in products:
            node = ProductNode(product)
            node.next_node = head
            head = node

        head = self._sort_head(head)

        sorted_products = []
        while head:
            sorted_products.append(head.data)
            head = head.next_node

        return sorted_products

    def _sort_head(self, head):
        current = head
        while current:
            runner = current.next_node
            while runner:
                stock_current = current.data["stock"]
                stock_runner = runner.data["stock"]

                if (stock_current > stock_runner and self.sort_lowest_first) or \
                    (stock_current < stock_runner and not self.sort_lowest_first):
                        current.data, runner.data = runner.data, current.data

                runner = runner.next_node
            current = current.next_node

        return head

def sort_products(products:list[dict], sort_lowest_first=True) -> list[dict]:
    """ Sorts Product List by number of stock depending on the currently selected sorting method """

    sorter = ProductLinkedListSorter(sort_lowest_first)
    
    return sorter.sort_products(products)
