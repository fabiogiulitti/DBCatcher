db = db.getSiblingDB('testdb');

db.createCollection('testcollection');

db.testcollection.insertMany([
  { name: "Alice", age: 25 },
  { name: "Bob", age: 30 },
  { name: "Charlie", age: 35 }
]);
