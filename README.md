# Vehicle Routing Challenge

Given:
    - A directory containing text files
    - Each text file contains a list of loads
    - A load has an identifier, a pickup location, and a dropoff location
    - A location is specified by (x, y) cartesian coordinates
    - Drive time between locations, in minutes, is equal to their Euclidean distance
    - Each truck must start from the origin (0, 0)
    - Each truck must end at the origin (0, 0)
    - Each truck costs $500
    - Each minute driven costs $1
    - No truck can exceed 12 hours of drive time

Then:
    - A route consists of a sequence of loads
    - The first load in a route has the origin as the pickup location
    - The last load in a route has the origin as the dropoff location

Assumptions:
    - Each load must be handled by one truck
    - Load weight does not effect cost
    - Load volume does not effect cost
    - Trucks can handle infinite weight
    - Trucks can handle infinite volume
    - Trucks will not experience any delays due maintenance issues
    - Trucks will not experience any delays due to weather
    - Trucks will not experience any delays due to road construction
    - Trucks will not experience any delays due traffic
    - Trucks do not experience the law of inertia
    - Trucks are equipped with teleportation technology, allowing for instantaneous loading and unloading
    - Trucks are Autobots, not Decepticons
    - Trucks are powered by Energon, requiring no refueling or breaks
    - When on a route trucks will not transform
    
Objective:
    - Maximize the total distance traveled by each truck
    - Minimize the total cost of all routes travelled
    - Minimize the application's run time

Approach:
    - TODO