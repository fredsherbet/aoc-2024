import sys
from collections import defaultdict
# Can we solve the order by swapping books in their rule chains?

# Rules: 1,2 1,3
# order: 321 -> 312 -> 132 (or -> 123)
# order: 231 -> 132
#
# Rules: 1,2 1,3 2,4 2,5
# order: 54321
# Chain rules: 1>2>4
#                 >5
#               >4>5
#
# Track which pages have nothing pointing at; they represent each of the chains


class PrintingValidator:
    def __init__(self):
        self.link = defaultdict(set)
        self.in_a_chain = set()
        self.starts_of_chains = set()
        self.rules = []

    def add_rule(self, before, after):
        self.rules.append([before, after])
        if after in self.starts_of_chains: self.starts_of_chains.remove(after)
        if before not in self.in_a_chain: self.starts_of_chains.add(before)
        self.in_a_chain.add(after)
        self.link[before].add(after)

    def validate_page_order(self, page_order):
        def check_rule(r):
            max_ix = -1
            for p in page_order:
                if p in r:
                    ix = r.index(p)
                    if max_ix != -1 and ix < max_ix:
                        return False
                    max_ix = ix
            return True

        return all(check_rule(r) for r in self.rules)

    def fixup(self, page_order):
        new_order = []
        for p in page_order:
            pass

    def get_middle_page(self, page_order):
        pages_after = self.relevant_rules(page_order)
        middle_page_has_after = len(page_order)//2
        for page in pages_after:
            if len(pages_after[page]) == middle_page_has_after:
                return page
        assert False, f"Did not find middle page for {page_order}"


    def relevant_rules(self, page_order):
        rules = defaultdict(set)
        for l in self.link:
            if l in page_order:
                rules[l] = self.link[l].intersection(set(page_order))

        return rules





validator = PrintingValidator()

with open('input') as input:
    # Load up the rules first
    for l in input:
        l = l.strip()
        if not l:
            # Blank line; we've gotten all the rules
            break
        rule = [int(n) for n in l.split('|')]
        assert len(rule) == 2, f"Unexpected rule length: {rule}"
        validator.add_rule(rule[0], rule[1])

    result = 0

    # Process the printing orders (we'll continue where the previous loop left off)
    for l in input:
        page_order = [int(n) for n in l.strip().split(',')]
        assert len(page_order) % 2 == 1, f"Bad page-order length {page_order}"
        if not validator.validate_page_order(page_order):
            middle_page = validator.get_middle_page(page_order)
            print(f"Middle page is {middle_page} in {page_order}")
            result += middle_page

    print(f"Sum of the middle page of fixed print orders: {result}")

