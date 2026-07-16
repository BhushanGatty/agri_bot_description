# Smart Harvest: Autonomous Agricultural Mobile Manipulator

This repository contains the ROS 2 Jazzy and Gazebo Harmonic digital twin simulation environment for **Smart Harvest**, an autonomous crop-harvesting platform featuring a 5-DOF manipulator arm and a differential drive chassis.

##  Simulation Demo

High fedelity agriculture Digital twin environment in gazebo harmonic.(*The live simulation animation gifs will be uploaded later)
<img width="1422" height="914" alt="WhatsApp Image 2026-07-16 at 1 42 00 AM" src="https://github.com/user-attachments/assets/1e0144eb-a3b3-41fb-b775-2f14f28aa5fc" />

Real time edge perception pipeline and spacial coordinates visualization mapped within ros2 rviz interface
<img width="1405" height="796" alt="Screenshot 2026-07-15 230748" src="https://github.com/user-attachments/assets/77f2e162-aae9-4200-93ea-cf1676874b41" />
The left side of the figure shows the spatial RViz point-cloud generation, in comparison to the raw camera stream fed through the edge classifier (right, inset). The high-density clusters of green are visualizations of the detected plant foliage and structural leaves and the red point clouds represent the flat terrain and soil boundaries. The purple cuboids are the defensive bounding boxes used to carry out real-time collision checking in the automated motion planning phases. The red-green-blue coordinate frame is also positioned near the center axis, and it provides the exact 6-DOF location and orientation of the target pick goal to directly feed into the inverse kinematics solver of the manipulator. It shows that these integrated overlays are able to separate the localized fruit clusters from obstacles around them and to publish highly reliable spatial coordinate frames prior to the approach sequence of the 5-DOF arm.

##  System Overview
- **Chassis:** 4-wheel differential drive platform optimized for narrow crop centerlines.
- **Manipulator:** 5-DOF serial link chain configured for precise coordinate targeting.
- **Perception:** Real-time RGB-D vision tracking mapped to standard ROS 2 perception topics.
