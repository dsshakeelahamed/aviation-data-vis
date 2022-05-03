aviation_accidents = [
                {
                    "$match": {"Investigation.Type": "Accident"}
                },
                {
                    "$count": "num_accidents"
                }
            ]

aircrafts_destroyed = [
                {
                    "$match": {"Aircraft.damage" : "Destroyed"}
                },
                {
                    "$count": "num_destroyed"
                }
            ]
fatal_injuries = [
                {
                 "$group":
                {
                    "_id": "null",
                    "TotalFatal": {"$sum": "$Total.Fatal.Injuries"}
                    }},
            {"$project": {"TotalFatal": 1, "_id": 0}}

            ]

serious_injuries = [
                {
                 "$group":
                {
                    "_id": "null",
                    "TotalFatal": {"$sum": "$Total.Serious.Injuries"}
                    }},
            {"$project": {"TotalFatal": 1, "_id": 0}}
            ]

line_graph = [
             {
                "$match": {"Investigation.Type": "Accident"}
             },
             {
                "$group":
                {
                    "_id": { "year": { "$year": {"$dateFromString": {"dateString" : "$Event.Date", "format": "%Y-%m-%d"}}}},
                    "TotalAccidents": {"$sum": 1}
                 }
            },
            { "$project": { "year": "$_id.year", "TotalAccidents" : 1, "_id":0} },
            { "$sort": {"year":1}}
            ]

bar_graph = [
             {
                "$match": {"Investigation.Type": "Accident" }
             },
             {
                "$group":
                {
                    "_id": {"PhaseOfFlight" : "$Broad.phase.of.flight" },
                    "data": {"$sum": 1}
                 }
            },
            {"$project": {"label": "$_id.PhaseOfFlight", "data": 1, "_id": 0}},
            ]

fatal_accidents = [
    {"$match":
         {"Injury.Severity": "Non-Fatal"}
     },
    {"$count": "fatal"}
]

non_fatal_accidents = [
    {"$match":
         {"Injury.Severity":
              {"$not" : {"$eq" : "Non-Fatal"}}
          }},
    {"$count": "non_fatal"}
]

