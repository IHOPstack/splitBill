def main():
    items = [line.split() for line in open('splitBills', 'r')]
    subtotal = 0
    taxTip = float(items[-1][-1])
    items.remove(items[-1])
    people = {}
    print(items)
    for item in items:
        price = float(item[-1])
        person = item[0]
        people[person] = people.get(person, 0) + price
        subtotal += price
    for person in people:
        print(people[person])
        price = people[person]
        billPercent = price/subtotal
        taxTipShare = billPercent * taxTip
        print(person, taxTipShare, price, round((taxTipShare + price), 2))
main()


