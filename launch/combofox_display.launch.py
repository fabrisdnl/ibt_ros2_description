# @brief     Launch file for visualizing the models of the combofox robot
#
# @author    Mattia Dei Rossi <mattia.deirossi@innobotics.it>
# @copyright (C) IBT


import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import Command, FindExecutable, LaunchConfiguration
from launch.conditions import IfCondition
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument


def generate_launch_description():
    declared_arguments = []
    declared_arguments.append(
        DeclareLaunchArgument(
            "arm_type",
            description="Type/series of used IBT robot.",
            choices=["robofox_61814v3"],
            default_value="robofox_61814v3",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "arm_prefix",
            default_value='robofox',
            description="Prefix of the joint names, useful for multi-robot setup."
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "use_gui",
            default_value='true',
            description="Launch joint_state_publisher_gui."
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "use_rviz",
            default_value='false',
            description="Launch RViz2 with predefines config."
        )
    )

    arm_type = LaunchConfiguration("arm_type")
    arm_prefix = LaunchConfiguration("arm_prefix")
    use_gui = LaunchConfiguration("use_gui")
    use_rviz = LaunchConfiguration("use_rviz")
    
    pkg_dir = get_package_share_directory('ibt_ros2_description')

    # Configuration files
    xacro_file = os.path.join(pkg_dir, 'xacro', 'combofox/combofox_rs.urdf.xacro')
    robot_description = Command([FindExecutable(name='xacro'),
                                 ' ', xacro_file,
                                 ' ', 'arm_type:=', arm_type,
                                 ' ', 'arm_prefix:=', arm_prefix
                                 ])
    rviz_config_path = os.path.join(pkg_dir, 'config', 'config.rviz')

    # Nodes
    robot_state_publisher_node = Node(
        name='robot_state_publisher',
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[
            {'robot_description': robot_description},
        ]
    )

    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen',
        parameters=[
            {'source_list': ['/robofox/joint_states']}
        ]
    )

    # joint_state_publisher_gui_node = Node(
    #     package='joint_state_publisher_gui',
    #     executable='joint_state_publisher_gui',
    #     condition=IfCondition(use_gui)
    # )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=[
            '-d', rviz_config_path
        ],
        condition=IfCondition(use_rviz)
    )
    nodes = [
        robot_state_publisher_node,
        joint_state_publisher,
        # joint_state_publisher_gui_node,
        rviz_node
    ]

    return LaunchDescription(declared_arguments + nodes)
