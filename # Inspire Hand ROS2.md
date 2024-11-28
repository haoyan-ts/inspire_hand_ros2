# Inspire Hand ROS2

This project is a ROS2 package for controlling the Inspire Hand robotic hand. It provides the necessary nodes and interfaces to interact with the hardware and perform various robotic hand operations.

## Features

- Control the Inspire Hand robotic hand
- ROS2 nodes for communication and control
- Example launch files and configurations

## Installation

1. Clone the repository into your ROS2 workspace:
    ```sh
    git clone https://github.com/haoyan-ts/inspire_hand_ros2.git
    ```

2. Navigate to your ROS2 workspace and build the package:
    ```sh
    cd ~/dobot_ws
    colcon build
    ```

3. Source the workspace:
    ```sh
    source install/setup.bash
    ```

## Usage

To launch the pub/sub control node, use the following command:
```sh
ros2 run inspire_hand_demo talker
ros2 run inspire_hand_demo client
```

## Nodes
### inspire_hand_demo
This node handles the communication and control of the Inspire Hand robotic hand.

### Parameters
port (string): The serial port to which the Inspire Hand is connected.
baudrate (int): The baud rate for the serial communication.

## Launch Files
control.launch.py
Launches the inspire_hand_demo node with the necessary parameters.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
