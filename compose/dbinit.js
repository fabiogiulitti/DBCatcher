db = db.getSiblingDB('testdb');

db.createCollection('firstcollection');

db.firstcollection.insertMany([
  { name: "Alice", age: 25 },
  { name: "Bob", age: 30 },
  { name: "Charlie", age: 35 }
]);

db.createCollection('secondcollection');

db.secondcollection.insertMany([
  { name: "Fabio", age: 45 },
  { name: "Jane", age: 20 },
  { name: "Charlie", age: 35 }
]);
