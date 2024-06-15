# Vehicle Routing Challenge

This repository contains my solution to a vehicle routing problem. In addition to providing a solution to the challenge itself, assumptions are presented to facilitate some of the gaps that occur with many requirements of feature and product requests and to have a bit of fun.

## Defining the Problem

We have agreed to handle a set of orders; each order requires a pickup and delivery to be made.

**Statement of Intent:**  
As a company, we have deliveries that each require a pickup and delivery to be made.
We would like to find an optimal set of routes to complete these deliveries.
So that we can minimize the cost and maximize revenue.

### Given

* A directory containing text files
* Each text file contains a list of loads
* A load has a load number, a pickup location, and a dropoff location
* A location is specified by (x, y) cartesian coordinates
* Drive time between locations, in minutes, is equal to their Euclidean distance
* Each truck must start from the origin (0, 0)
* Each truck must end at the origin (0, 0)
* Each truck costs $500
* Each minute driven costs $1
* No truck can exceed 12 hours of drive time

### Acceptance Criteria:
* Maximize the total distance traveled by each truck
* Minimize the total number of trucks
* Minimize the total cost of all routes travelled
* Minimize the application's run time

## Refining the Problem

In practice, many of the following assumptions would be discussed with product and feature stakeholders to:  
1. Ensure the problem is well defined and understood. assumptions are valid.
2. Identify any gaps in the requirements.
3. Offer alternative suggestions if applicable.
4. Reduce the risk of over-engineering or under-engineering the solution.
5. Deliver the right solution the first time.

### Assumptions
    
* Each load must be handled by one truck
* Load weight does not effect cost
* Load volume does not effect cost
* Trucks can handle infinite weight
* Trucks can handle infinite volume
* Trucks will not experience any delays due maintenance issues
* Trucks will not experience any delays due to weather
* Trucks will not experience any delays due to road construction
* Trucks will not experience any delays due traffic
* Trucks do not experience the law of inertia
* Trucks are equipped with teleportation technology, allowing for instantaneous loading and unloading
* Trucks are Autobots, not Decepticons
* Trucks are the drivers and the drivers are the trucks
* Trucks are powered by Energon, requiring no refueling or breaks
* Trucks will not transform when on route
    
## Working the Problem

### Approach

* Each load's Euclidean distance is a constant, and added as a property on the load as read in from the file
* Create a `green thread` for each load, as completing the set of loads with 1 truck is a best case and completing each load with a separate truck is a worst case.
* For each thread:
    * Generate a matrix containing all possible valid routes and cost for the given loads.
    * Return the most cost effective set of routes for this set of trucks.
* Report the most cost effective result for this set of loads

Green Threads:

Python's native multithreading feature, limited by the Global Interpreter Lock (GIL), ensures thread safety but reduces the benefits of concurrency for CPU-bound tasks. The GIL limits one thread of Python bytecode execution at a time in a single process, making it more suitable for I/O-bound tasks.

Green threads, managed in the user space rather than by the operating system, are not bound by the GIL. Calculating the cost and distance of each combination makes this a heavily CPU-bound task. By using lightweight green threads, we can achieve cooperative concurrency on a single CPU, avoiding the overhead of creating and managing multiple processes and improving resource usage efficiency.


### Alternatives

* As the calculations for this problem require simple arithmetic, utilizing GPU compute features would allow for 1000s of calculations to be performed in parallel. This would require a significant investment in hardware and software, and would not be cost effective for this challeng.
* The problem could be solved using a genetic algorithm, which would allow for a more efficient search of the solution space. This would require significant development time and would be cost prohibitive.
* The problem could be solved using a constraint programming library, such as Google's OR-Tools. This is against the rules of the challenge.
