import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    pkg_dir = get_package_share_directory('agri_bot_description')
    
    # 1. Process Xacro Robot State Description
    xacro_file = os.path.expanduser('~/robot_ws/src/agri_bot_description/urdf/agri_bot.urdf.xacro')
    robot_desc = xacro.process_file(xacro_file).toxml()

    # 2. Boot up Gazebo Sim loading the generated Agricultural World
    world_file = os.path.join(pkg_dir, 'worlds', 'agriculture.sdf')
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')]),
        launch_arguments={'gz_args': f'-r {world_file}'}.items(),
    )

    # 3. CRITICAL FIXED NODE: Publishes the Joint Transformations Tree to ROS 2
    robot_state_pub = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_desc, 'use_sim_time': True}]
    )

    # 4. Spawns the Robot directly down into the clear central aisle (X=0, Y=0)
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description', '-name', 'agri_bot', '-x', '0.0', '-y', '0.0', '-z', '0.30'],
        output='screen'
    )

    # 5. Core Simulation Communication Bridge
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/joint_states@sensor_msgs/msg/JointState[gz.msgs.JointState', # ADD THIS LINE
            '/camera/image@sensor_msgs/msg/Image[gz.msgs.Image',
            '/camera/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo',
            '/camera/points@sensor_msgs/msg/PointCloud2[gz.msgs.PointCloud2'
        ],
        remappings=[
            ('/camera/image', '/camera/image_raw')
        ],
        output='screen'
    )

    # 6. Automated Sequenced Controller Spawners (Added Joint State Broadcaster)
    load_joint_state = Node(package="controller_manager", executable="spawner", arguments=["joint_state_broadcaster"])
    load_base = Node(package="controller_manager", executable="spawner", arguments=["base_controller"])
    load_arm = Node(package="controller_manager", executable="spawner", arguments=["arm_controller"])
    load_gripper = Node(package="controller_manager", executable="spawner", arguments=["gripper_controller"])

    controller_spawners = TimerAction(
        period=5.0,
        actions=[load_joint_state, load_base, load_arm, load_gripper]
    )

    return LaunchDescription([
        gazebo,
        robot_state_pub,
        spawn_robot,
        bridge,
        controller_spawners
    ])
