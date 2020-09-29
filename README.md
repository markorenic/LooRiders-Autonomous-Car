# LooRiders
Project for SE101

SE 101 Project Proposal: Loo Riders
Faraz Khoubsirat, Marko Renic, Iva Chho, Quy Duc Do, Michael Solodko

Summary
Link ro car : https://www.amazon.ca/gp/product/B07WK21QP1?ref=ppx_pt2_dt_b_prod_image
Software Components

Image localization and processing of a physical maze(grid)
Car pathfinding Program using A*star path finding algorithm
Hardware Components
Arduino Uno: Processes and receives information from the processed grid to map a suitable path for the car
Ultrasonic sensor: Identifies possible barriers along the cars trajectory to prevent collisions
Arduino two wheel car: Construct a function car with turning capabilities
Raspberry Pi camera to scan the grid

Challenges
Localizing the image of the maze into usable data points to form a virtual grid and determine the shortest path for the car
Optimizing the car’s path if multiple routes are available
Programming the car’s turning angle and speed in order to avoid crashing any blocks upon turning
Evolutionary Prototype Plan
Building functional arduino two wheel car
Constructing a physical and changeable maze grid
Using the raspberry pi camera to function as a hanging satellite to capture the grid
Localizing the picture of the grid and transforming the grid in the picture to a pygame grid
Plotting the starting point, ending point and positions of obstacles on the grid
Identifying the shortest route to reach the destination 
Sending the direction instructions to arduino car via bluetooth and starting the autonomous car
Upon success, changing the maze setup and trying out the new route

Extras
Adding voice recognition to the car to activate the camera and itself upon receiving vocal destination coordinates
Adding traffic lights or sudden obstacles to the maze and enabling the camera(satelite) to send live data to the car in order to change its direction to avoid collision
