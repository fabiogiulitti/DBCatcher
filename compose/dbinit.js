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

db.createCollection('thirdcollection');

db.thirdcollection.insertMany([
  {
    "name": "Lee Griffith",
    "age": 89,
    "Address": {
      "strit": "Cruz Hill",
      "number": "885",
      "city": "South Elaine",
      "zip_code": "21910"
    }
  },
  {
    "name": "Richard Ryan",
    "age": 22,
    "Address": {
      "strit": "Brooke Mountains",
      "number": "6161",
      "city": "Justinburgh",
      "zip_code": "09554"
    }
  },
  {
    "name": "Isaac Alvarado",
    "age": 64,
    "Address": {
      "strit": "Miller Spur",
      "number": "3597",
      "city": "Hendersonburgh",
      "zip_code": "71453"
    }
  },
  {
    "name": "Antonio James",
    "age": 31,
    "Address": {
      "strit": "Barr Ranch",
      "number": "17434",
      "city": "Goldenville",
      "zip_code": "15247"
    }
  },
  {
    "name": "Danielle Baldwin",
    "age": 72,
    "Address": {
      "strit": "Erica Turnpike",
      "number": "4834",
      "city": "Perkinsburgh",
      "zip_code": "52569"
    }
  },
  {
    "name": "Sean Foley",
    "age": 67,
    "Address": {
      "strit": "Casey Place",
      "number": "7537",
      "city": "Lake Stephentown",
      "zip_code": "14523"
    }
  },
  {
    "name": "Lucas Larson",
    "age": 34,
    "Address": {
      "strit": "Andrew River",
      "number": "5080",
      "city": "New Tiffany",
      "zip_code": "81369"
    }
  },
  {
    "name": "Sherry Rodriguez",
    "age": 23,
    "Address": {
      "strit": "Hill Coves",
      "number": "9035",
      "city": "New Patricia",
      "zip_code": "50113"
    }
  },
  {
    "name": "William Sherman",
    "age": 36,
    "Address": {
      "strit": "Todd Coves",
      "number": "0196",
      "city": "West Joshua",
      "zip_code": "28077"
    }
  },
  {
    "name": "Jean Wilson",
    "age": 82,
    "Address": {
      "strit": "Figueroa Walk",
      "number": "5708",
      "city": "Jameston",
      "zip_code": "15927"
    }
  },
  {
    "name": "Matthew Gonzalez IV",
    "age": 23,
    "Address": {
      "strit": "Jessica Orchard",
      "number": "69058",
      "city": "Jeffreyland",
      "zip_code": "36175"
    }
  },
  {
    "name": "Cynthia Mcmahon",
    "age": 29,
    "Address": {
      "strit": "Susan Forest",
      "number": "4457",
      "city": "Jesusfort",
      "zip_code": "35913"
    }
  },
  {
    "name": "Susan Hernandez",
    "age": 31,
    "Address": {
      "strit": "Johnson Station",
      "number": "792",
      "city": "Lake Rebeccastad",
      "zip_code": "40892"
    }
  },
  {
    "name": "Kathryn Patterson",
    "age": 56,
    "Address": {
      "strit": "Nathan Mill",
      "number": "8836",
      "city": "Robertton",
      "zip_code": "66059"
    }
  },
  {
    "name": "Victoria Smith",
    "age": 20,
    "Address": {
      "strit": "Gary Prairie",
      "number": "93330",
      "city": "Brianland",
      "zip_code": "24873"
    }
  },
  {
    "name": "Adam Garcia",
    "age": 34,
    "Address": {
      "strit": "Yu Mill",
      "number": "431",
      "city": "North Mark",
      "zip_code": "75062"
    }
  },
  {
    "name": "William Ware",
    "age": 35,
    "Address": {
      "strit": "Poole Dale",
      "number": "1460",
      "city": "Martinezland",
      "zip_code": "95525"
    }
  },
  {
    "name": "Michael Grimes",
    "age": 19,
    "Address": {
      "strit": "Cindy Brooks",
      "number": "577",
      "city": "North Amy",
      "zip_code": "08254"
    }
  },
  {
    "name": "David Summers",
    "age": 81,
    "Address": {
      "strit": "Felicia Forge",
      "number": "91034",
      "city": "Jacobsonmouth",
      "zip_code": "77259"
    }
  },
  {
    "name": "Mary Michael",
    "age": 39,
    "Address": {
      "strit": "Roy Fall",
      "number": "369",
      "city": "Lanestad",
      "zip_code": "32424"
    }
  },
  {
    "name": "Taylor English",
    "age": 67,
    "Address": {
      "strit": "John Lock",
      "number": "13386",
      "city": "South Kevin",
      "zip_code": "97774"
    }
  },
  {
    "name": "Cynthia Moyer",
    "age": 88,
    "Address": {
      "strit": "John Hills",
      "number": "803",
      "city": "Crystalfort",
      "zip_code": "12942"
    }
  },
  {
    "name": "Andrew Myers",
    "age": 82,
    "Address": {
      "strit": "Sarah Unions",
      "number": "892",
      "city": "Matthewland",
      "zip_code": "28722"
    }
  },
  {
    "name": "Shannon Schneider",
    "age": 60,
    "Address": {
      "strit": "Medina Points",
      "number": "705",
      "city": "Port Haroldton",
      "zip_code": "50323"
    }
  },
  {
    "name": "Angela Mcdonald",
    "age": 39,
    "Address": {
      "strit": "James Bridge",
      "number": "753",
      "city": "Evansstad",
      "zip_code": "26389"
    }
  },
  {
    "name": "Terry Thompson",
    "age": 82,
    "Address": {
      "strit": "Deanna Road",
      "number": "56025",
      "city": "West Johnnytown",
      "zip_code": "78897"
    }
  },
  {
    "name": "Jeremy Hughes",
    "age": 44,
    "Address": {
      "strit": "Rachel Shoals",
      "number": "943",
      "city": "West Stacey",
      "zip_code": "18838"
    }
  },
  {
    "name": "Monique Hanson",
    "age": 66,
    "Address": {
      "strit": "Christensen Trail",
      "number": "28594",
      "city": "South Jason",
      "zip_code": "75381"
    }
  },
  {
    "name": "Robin Cox",
    "age": 89,
    "Address": {
      "strit": "Mullins Creek",
      "number": "614",
      "city": "North Judymouth",
      "zip_code": "40391"
    }
  },
  {
    "name": "Leslie Mccoy",
    "age": 46,
    "Address": {
      "strit": "Kenneth Spur",
      "number": "7286",
      "city": "North Christopher",
      "zip_code": "55258"
    }
  },
  {
    "name": "James Mills",
    "age": 81,
    "Address": {
      "strit": "Jessica Junction",
      "number": "4191",
      "city": "West Juliaville",
      "zip_code": "84339"
    }
  },
  {
    "name": "Linda Welch",
    "age": 88,
    "Address": {
      "strit": "Mcdonald Via",
      "number": "781",
      "city": "Amyhaven",
      "zip_code": "14304"
    }
  },
  {
    "name": "Ray Riley",
    "age": 80,
    "Address": {
      "strit": "Mccoy Stravenue",
      "number": "624",
      "city": "New Wendyport",
      "zip_code": "51128"
    }
  },
  {
    "name": "Marcia Carrillo",
    "age": 50,
    "Address": {
      "strit": "Karen Hills",
      "number": "205",
      "city": "East Tammyberg",
      "zip_code": "41063"
    }
  },
  {
    "name": "Benjamin Stevens",
    "age": 90,
    "Address": {
      "strit": "Guerrero Springs",
      "number": "08606",
      "city": "East Dianahaven",
      "zip_code": "39366"
    }
  },
  {
    "name": "Scott Ballard",
    "age": 64,
    "Address": {
      "strit": "Parker Mills",
      "number": "800",
      "city": "Theresatown",
      "zip_code": "84989"
    }
  },
  {
    "name": "Jim Lewis",
    "age": 53,
    "Address": {
      "strit": "Pedro Lodge",
      "number": "907",
      "city": "East Matthewburgh",
      "zip_code": "41902"
    }
  },
  {
    "name": "Tonya Reed MD",
    "age": 20,
    "Address": {
      "strit": "Carol Corner",
      "number": "5145",
      "city": "Jacksonville",
      "zip_code": "63853"
    }
  },
  {
    "name": "Sandra Jackson",
    "age": 36,
    "Address": {
      "strit": "Sanchez Creek",
      "number": "87150",
      "city": "Brentbury",
      "zip_code": "56932"
    }
  },
  {
    "name": "Megan Fleming",
    "age": 22,
    "Address": {
      "strit": "Stephen Corners",
      "number": "749",
      "city": "Morrismouth",
      "zip_code": "44737"
    }
  },
  {
    "name": "Christina Barr",
    "age": 20,
    "Address": {
      "strit": "Romero Pike",
      "number": "4588",
      "city": "Melissaville",
      "zip_code": "97632"
    }
  },
  {
    "name": "Ronald Butler",
    "age": 29,
    "Address": {
      "strit": "Boyer Plaza",
      "number": "0746",
      "city": "Aliciastad",
      "zip_code": "31949"
    }
  },
  {
    "name": "Thomas Mcbride",
    "age": 54,
    "Address": {
      "strit": "Wise Stream",
      "number": "0458",
      "city": "South Amandaview",
      "zip_code": "97103"
    }
  },
  {
    "name": "Sandra Gould",
    "age": 80,
    "Address": {
      "strit": "Keith Tunnel",
      "number": "3665",
      "city": "Martinezburgh",
      "zip_code": "43898"
    }
  },
  {
    "name": "Karen Ibarra",
    "age": 61,
    "Address": {
      "strit": "Laura Causeway",
      "number": "5901",
      "city": "East Danielburgh",
      "zip_code": "52467"
    }
  },
  {
    "name": "Melanie Miller",
    "age": 57,
    "Address": {
      "strit": "Debra Meadow",
      "number": "3928",
      "city": "Lake Lorrainemouth",
      "zip_code": "78727"
    }
  },
  {
    "name": "Carol Simmons",
    "age": 52,
    "Address": {
      "strit": "Melton Mill",
      "number": "7110",
      "city": "North Michaelberg",
      "zip_code": "39483"
    }
  },
  {
    "name": "Elizabeth Herrera",
    "age": 52,
    "Address": {
      "strit": "Jeremy Fall",
      "number": "10908",
      "city": "Nelsonland",
      "zip_code": "57457"
    }
  },
  {
    "name": "Martha Shields",
    "age": 23,
    "Address": {
      "strit": "Romero Lane",
      "number": "8406",
      "city": "Chelseaville",
      "zip_code": "85060"
    }
  },
  {
    "name": "Shawn Cohen",
    "age": 52,
    "Address": {
      "strit": "Jesse Plains",
      "number": "22661",
      "city": "North Dwayneberg",
      "zip_code": "26093"
    }
  },
  {
    "name": "Jacqueline Rivera",
    "age": 29,
    "Address": {
      "strit": "Thompson Rue",
      "number": "9288",
      "city": "Lisatown",
      "zip_code": "15376"
    }
  },
  {
    "name": "Stanley Chang",
    "age": 23,
    "Address": {
      "strit": "Cynthia Spur",
      "number": "17429",
      "city": "Lisaville",
      "zip_code": "75565"
    }
  },
  {
    "name": "John Moore",
    "age": 59,
    "Address": {
      "strit": "Laura Burgs",
      "number": "527",
      "city": "Billyton",
      "zip_code": "21869"
    }
  },
  {
    "name": "Aaron Hall",
    "age": 41,
    "Address": {
      "strit": "Daniel Fork",
      "number": "111",
      "city": "Rickystad",
      "zip_code": "55449"
    }
  },
  {
    "name": "Micheal Moreno",
    "age": 46,
    "Address": {
      "strit": "Erica Orchard",
      "number": "8280",
      "city": "West Brentchester",
      "zip_code": "12492"
    }
  },
  {
    "name": "Andrew Fletcher",
    "age": 71,
    "Address": {
      "strit": "Tina Haven",
      "number": "8802",
      "city": "Baileyhaven",
      "zip_code": "76507"
    }
  },
  {
    "name": "Mrs. Elizabeth Holland",
    "age": 87,
    "Address": {
      "strit": "Alexandra Brook",
      "number": "40225",
      "city": "South Garrett",
      "zip_code": "65372"
    }
  },
  {
    "name": "Laura Graves",
    "age": 25,
    "Address": {
      "strit": "Amy Branch",
      "number": "4125",
      "city": "Lake Joshua",
      "zip_code": "28606"
    }
  },
  {
    "name": "Raymond Ward",
    "age": 33,
    "Address": {
      "strit": "Mike Tunnel",
      "number": "96148",
      "city": "Morrisside",
      "zip_code": "56429"
    }
  },
  {
    "name": "Amber Rivas",
    "age": 20,
    "Address": {
      "strit": "Ferrell Rapids",
      "number": "1483",
      "city": "Mercerfort",
      "zip_code": "67021"
    }
  },
  {
    "name": "Debra Hanson",
    "age": 28,
    "Address": {
      "strit": "David Village",
      "number": "1934",
      "city": "Tammystad",
      "zip_code": "56292"
    }
  },
  {
    "name": "Samantha Obrien",
    "age": 24,
    "Address": {
      "strit": "Harris Club",
      "number": "4623",
      "city": "Port Angelahaven",
      "zip_code": "90773"
    }
  },
  {
    "name": "Dennis Adams",
    "age": 26,
    "Address": {
      "strit": "James Branch",
      "number": "1837",
      "city": "Lake Christina",
      "zip_code": "68857"
    }
  },
  {
    "name": "Elizabeth Davis",
    "age": 26,
    "Address": {
      "strit": "Terry Path",
      "number": "4804",
      "city": "Hammondburgh",
      "zip_code": "52749"
    }
  },
  {
    "name": "John Ware",
    "age": 73,
    "Address": {
      "strit": "Rojas Pines",
      "number": "577",
      "city": "Castilloland",
      "zip_code": "25386"
    }
  },
  {
    "name": "Tracy Jackson",
    "age": 90,
    "Address": {
      "strit": "Steven Ranch",
      "number": "112",
      "city": "Joshuaburgh",
      "zip_code": "46162"
    }
  },
  {
    "name": "Willie Cisneros",
    "age": 86,
    "Address": {
      "strit": "Patton Parkway",
      "number": "66812",
      "city": "Alexandermouth",
      "zip_code": "94788"
    }
  },
  {
    "name": "Tanya Davidson",
    "age": 58,
    "Address": {
      "strit": "Lisa Junction",
      "number": "5976",
      "city": "West Sally",
      "zip_code": "79736"
    }
  },
  {
    "name": "Deborah Oliver",
    "age": 39,
    "Address": {
      "strit": "Sherman Place",
      "number": "90326",
      "city": "North Dylantown",
      "zip_code": "48947"
    }
  },
  {
    "name": "Steven Baxter",
    "age": 57,
    "Address": {
      "strit": "Sharon Pike",
      "number": "5945",
      "city": "Fuentesland",
      "zip_code": "13157"
    }
  },
  {
    "name": "Brenda Brown",
    "age": 59,
    "Address": {
      "strit": "Salazar Forest",
      "number": "94595",
      "city": "Port Gina",
      "zip_code": "83417"
    }
  },
  {
    "name": "Latoya Barker",
    "age": 65,
    "Address": {
      "strit": "Danielle Walk",
      "number": "7194",
      "city": "Adamport",
      "zip_code": "74121"
    }
  },
  {
    "name": "Bailey Trujillo",
    "age": 32,
    "Address": {
      "strit": "Robin Prairie",
      "number": "3384",
      "city": "West Patricia",
      "zip_code": "30846"
    }
  },
  {
    "name": "Caitlyn Ferguson",
    "age": 60,
    "Address": {
      "strit": "Lauren Mission",
      "number": "72265",
      "city": "West Mirandaburgh",
      "zip_code": "05854"
    }
  },
  {
    "name": "Angela Grimes",
    "age": 24,
    "Address": {
      "strit": "Williams Village",
      "number": "52710",
      "city": "West Philipchester",
      "zip_code": "19982"
    }
  },
  {
    "name": "Ryan Wilkins",
    "age": 86,
    "Address": {
      "strit": "Lewis Manor",
      "number": "31575",
      "city": "Port Corey",
      "zip_code": "11292"
    }
  },
  {
    "name": "Tiffany Burton",
    "age": 66,
    "Address": {
      "strit": "Martin Branch",
      "number": "44850",
      "city": "New Dustin",
      "zip_code": "13902"
    }
  },
  {
    "name": "Jo Williams",
    "age": 50,
    "Address": {
      "strit": "Francisco Unions",
      "number": "578",
      "city": "Kennethburgh",
      "zip_code": "67220"
    }
  },
  {
    "name": "Joel Rosario",
    "age": 19,
    "Address": {
      "strit": "Connie Mountain",
      "number": "701",
      "city": "Quinnberg",
      "zip_code": "51969"
    }
  },
  {
    "name": "Jason Johnson",
    "age": 75,
    "Address": {
      "strit": "Cassandra Fields",
      "number": "865",
      "city": "Lake Matthew",
      "zip_code": "42748"
    }
  },
  {
    "name": "Todd Mendez",
    "age": 26,
    "Address": {
      "strit": "Miguel Flats",
      "number": "91024",
      "city": "Nicholasmouth",
      "zip_code": "03923"
    }
  },
  {
    "name": "Julie Bender",
    "age": 44,
    "Address": {
      "strit": "Lee Ridges",
      "number": "7356",
      "city": "Lake Matthew",
      "zip_code": "81511"
    }
  },
  {
    "name": "Luis Meyers",
    "age": 45,
    "Address": {
      "strit": "Zachary Station",
      "number": "155",
      "city": "South Jessica",
      "zip_code": "31617"
    }
  },
  {
    "name": "Katherine Williams",
    "age": 27,
    "Address": {
      "strit": "Swanson Pines",
      "number": "45927",
      "city": "West John",
      "zip_code": "31043"
    }
  },
  {
    "name": "Michael Soto",
    "age": 42,
    "Address": {
      "strit": "Allen Lake",
      "number": "6168",
      "city": "East Joshua",
      "zip_code": "81818"
    }
  },
  {
    "name": "Brian Garcia",
    "age": 39,
    "Address": {
      "strit": "Serrano View",
      "number": "8418",
      "city": "Hoopertown",
      "zip_code": "74696"
    }
  },
  {
    "name": "Julie Kelly",
    "age": 90,
    "Address": {
      "strit": "Kevin Shore",
      "number": "851",
      "city": "West Stephanie",
      "zip_code": "52837"
    }
  },
  {
    "name": "Travis Long",
    "age": 81,
    "Address": {
      "strit": "Chapman Skyway",
      "number": "37761",
      "city": "Boltonfort",
      "zip_code": "16339"
    }
  },
  {
    "name": "Carol Johnson",
    "age": 72,
    "Address": {
      "strit": "Jessica View",
      "number": "80477",
      "city": "Katiebury",
      "zip_code": "76353"
    }
  },
  {
    "name": "Stephanie Weaver",
    "age": 26,
    "Address": {
      "strit": "Escobar View",
      "number": "509",
      "city": "Elizabethport",
      "zip_code": "56442"
    }
  },
  {
    "name": "Erik Nicholson",
    "age": 32,
    "Address": {
      "strit": "Sarah Rest",
      "number": "9916",
      "city": "Paulahaven",
      "zip_code": "78004"
    }
  },
  {
    "name": "Harry Roman",
    "age": 71,
    "Address": {
      "strit": "Thomas Falls",
      "number": "434",
      "city": "New Bradleyview",
      "zip_code": "80403"
    }
  },
  {
    "name": "Amanda Kim",
    "age": 28,
    "Address": {
      "strit": "Miller Street",
      "number": "623",
      "city": "South Monicaland",
      "zip_code": "93632"
    }
  },
  {
    "name": "Dana Hill",
    "age": 28,
    "Address": {
      "strit": "King Well",
      "number": "9635",
      "city": "Murphyfort",
      "zip_code": "20713"
    }
  },
  {
    "name": "Eric Nguyen",
    "age": 35,
    "Address": {
      "strit": "Schneider Ports",
      "number": "91253",
      "city": "West Nancymouth",
      "zip_code": "33915"
    }
  },
  {
    "name": "Jordan Valdez",
    "age": 37,
    "Address": {
      "strit": "Jennifer Ramp",
      "number": "428",
      "city": "Timothyfurt",
      "zip_code": "32274"
    }
  },
  {
    "name": "Dean Cook",
    "age": 57,
    "Address": {
      "strit": "Sherry Haven",
      "number": "527",
      "city": "Lake Harold",
      "zip_code": "19839"
    }
  },
  {
    "name": "Kelli Green",
    "age": 20,
    "Address": {
      "strit": "James Path",
      "number": "546",
      "city": "Port Victoriashire",
      "zip_code": "06792"
    }
  },
  {
    "name": "Andrew Davis",
    "age": 80,
    "Address": {
      "strit": "Lee Fields",
      "number": "84554",
      "city": "North Carrieburgh",
      "zip_code": "38879"
    }
  },
  {
    "name": "Sandy Martinez",
    "age": 53,
    "Address": {
      "strit": "Diaz Course",
      "number": "90132",
      "city": "North Paulchester",
      "zip_code": "30621"
    }
  }
]);