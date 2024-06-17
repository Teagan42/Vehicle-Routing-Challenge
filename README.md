# Vehicle Routing Challenge

This repository contains my solution to a vehicle routing problem. In addition to providing a solution to the challenge itself, assumptions are presented to facilitate some of the gaps that occur with many requirements of feature and product requests and to have a bit of fun.

##  Running

To run the application:

1. Install dependencies:
```shell
pip3 install -r requirements.txt
```
2. Run the `vrp` module, passing as a positional argument a path to a problem set file

```shell
python3 -m vrp data/problem4.txt
```

Currently, only one routing strategy is enabled, the others are simply commented out. Feel free to compare the results by enabling the other routing strategies under `vrp/strategies/__init__.py`

```python
routing_strategies = [
    # LeastStopsStrategy,
    # NearestNeighborStrategy,
    NearestAndShortestJobStrategy,
    # ShortedJobStrategy,
]
```

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
* Loads cannot be completed while completing another load
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

### Future Improvements

Sadly, the time I had to work on this was interrupted by family and it is not as up to par with my usual standards. Honestly, it's a bit embarrassing to present to the world. 

Things that I would like to have improved:
* Utilizing pandas and scipy to improve the optimization. I know the ability to perform the linear algebra to optimize the routes is available, and I will continue to attempt to learn more about these tools
* Since the distance travelled is equivalent to the travel time, I had thought about how optimizing the schedule along with the route could have been benefitcial.
* Considering how little time was allotted to begin with, let alone the interruption, I would have preferred to explore this challenge using GoLang and goroutines.

### Grading My Work

Personally, I would give this project a C at best - there's something in the routing logic that seems to prefer assigning more and more vehicles instead of more stops to less vehicles. Since the challenge was to reduce cost, in that aspect I failed.

However, I did try to implement a few different routing strategies - and they do all effect the final result pretty drastically.
* Nearest Neighbor
* Shortest Delivery Duration
* Minimizing Stops
* Closest and Shortest Delivery

