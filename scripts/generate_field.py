#!/usr/bin/env python3
import os
import sys
from pathlib import Path

def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)

def main():
    root = Path(__file__).resolve().parent.parent
    worlds_dir = root / "worlds"
    ensure_dir(worlds_dir)

    # World configuration with enhanced ambient lighting and expanded soil scaling
    world_content = """<?xml version="1.0" ?>
<sdf version="1.9">
  <world name="agriculture">
    <physics name="1ms" type="ignored">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
    </physics>
    <plugin filename="gz-sim-physics-system" name="gz::sim::systems::Physics"/>
    <plugin filename="gz-sim-user-commands-system" name="gz::sim::systems::UserCommands"/>
    <plugin filename="gz-sim-scene-broadcaster-system" name="gz::sim::systems::SceneBroadcaster"/>
    <plugin filename="gz-sim-sensors-system" name="gz::sim::systems::Sensors"/>
	
    <scene>
      <ambient>0.6 0.6 0.6 1.0</ambient>
      <background>0.7 0.8 1.0 1.0</background>
      <grid>false</grid>
    </scene>

    <light type="directional" name="sun">
      <cast_shadows>true</cast_shadows>
      <pose>0 0 30 0 0 0</pose>
      <direction>-0.5 0.1 -0.9</direction>
      <diffuse>0.9 0.9 0.85 1</diffuse>
      <specular>0.1 0.1 0.1 1</specular>
    </light>

    <model name="soil_plane">
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry>
            <mesh>
              <uri>model://ground/meshes/ground.dae</uri>
              <scale>10 10 1</scale>
            </mesh>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <mesh>
              <uri>model://ground/meshes/ground.dae</uri>
              <scale>10 10 1</scale>
            </mesh>
          </geometry>
        </visual>
      </link>
    </model>
"""
    
    # FIX 3: High-density procedural crop row matrix (4 rows, 15 plants per row)
    # Aisle channels generated at Y = [-2.4, -0.8, 0.8, 2.4]
    plant_idx = 0
    y_rows = [-2.4, -0.8, 0.8, 2.4]
    
    # Generates 15 plants spanning from X = -7.0 meters to +7.0 meters
    x_positions = [x * 1.0 for x in range(-7, 8)] 

    for y_pos in y_rows:
        for x_pos in x_positions:
            # Leave space right in the center (0,0) so the robot doesn't spawn stuck inside a bush
            if abs(x_pos) < 0.5 and abs(y_pos) < 1.0:
                continue
                
            world_content += f"""
    <include>
      <name>plant_{plant_idx}</name>
      <uri>model://tomato_plant</uri>
      <pose>{x_pos} {y_pos} 0 0 0 0</pose>
    </include>"""
            plant_idx += 1

    world_content += "\n  </world>\n</sdf>"
    (worlds_dir / "agriculture.sdf").write_text(world_content)
    print(f"Successfully generated high-density field with {plant_idx} photorealistic crop assets!")

if __name__ == "__main__":
    main()
