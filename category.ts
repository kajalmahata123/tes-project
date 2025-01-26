export const CATEGORY_DATA = {
    airlines: {
      name: "Emirates Airlines",
      gradient: "from-blue-500 to-indigo-600",
      logo: "/emirates-logo.png",
      items: [{
        id: 1,
        name: "Business Class Ticket",
        price: 5799.98,
        description: "Dubai to New York",
        quantity: 1
      }]
    },
    grocery: {
      name: "Whole Foods",
      gradient: "from-green-500 to-emerald-600",
      logo: "/wholefoods-logo.png", 
      items: [{
        id: 1,
        name: "Organic Groceries",
        price: 299.99,
        description: "Weekly grocery delivery",
        quantity: 1
      }]
    },
    bigticket: {
      name: "Apple Store",
      gradient: "from-purple-500 to-indigo-500",
      logo: "/apple-logo.png",
      items: [{
        id: 1,
        name: "MacBook Pro", 
        price: 2499.99,
        description: "14-inch M2 Pro",
        quantity: 1
      }]
    }
   } as const;