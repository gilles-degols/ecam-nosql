db.sales.aggregate( [
   {
      $project: {
         items: {
            $filter: {
               input: "$items",
               as: "item",
               cond: { $eq: [ "$$item.name", "pen"] }
            }
         }
      }
   }
] )

[
    {
      _id: 0,
      items: [ { item_id: 43, quantity: 2, price: 10, name: 'pen' } ]
   },
   {
      _id: 1,
      items: [ { item_id: 103, quantity: 4, price: 5, name: 'pen' } ]
   },
   { _id: 2, items: [] }
]