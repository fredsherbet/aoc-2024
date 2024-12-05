
class PrintingValidator:
    def __init__(self):
        self.rules = []

    def add_rule(self, ordering):
        assert len(ordering) > 0, f"Ordering of bad length {ordering}"
        self.rules.append(ordering)

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


validator = PrintingValidator()

with open('input') as input:
    # Load up the rules first
    for l in input:
        l = l.strip()
        if not l:
            # Blank line; we've gotten all the rules
            break
        validator.add_rule([int(n) for n in l.split('|')])

    result = 0

    # Process the printing orders (we'll continue where the previous loop left off)
    for l in input:
        page_order = [int(n) for n in l.strip().split(',')]
        assert len(page_order) % 2 == 1, f"Bad page-order length {page_order}"
        if validator.validate_page_order(page_order):
            result += page_order[len(page_order) // 2]

    print(f"Sum of the middle page of valid print orders: {result}")

