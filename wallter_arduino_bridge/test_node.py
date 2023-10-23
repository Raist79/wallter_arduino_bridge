import rclpy
import serial
from rclpy.node import Node
from wallter_interfaces.msg import AkkuStats
from std_msgs.msg import String
encodedString = ''
decodedString = ''
tmpTest = []

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(AkkuStats, 'topic', 10)
        timer_period = 5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        self.serial_port = "/dev/ttyACM0"
        self.baud_rate = 115200
        self.get_logger().info(f"Connecting to port {self.serial_port} at {self.baud_rate}.")

        self.conn = serial.Serial(self.serial_port, self.baud_rate, timeout=1.0)
        while self.conn.is_open == False:
            self.get_logger().info('is connecting')
            
        self.get_logger().info(" connected to {self.serial_port} ")

    def timer_callback(self):
        global tmpTest
        global encodedString
        global decodedString
        self.conn.write('v \r\n'.encode())#  b"v \n\r"))        
        encodedString = self.conn.readline().decode('Ascii')
        
        print(encodedString)
            
        tmpTest = encodedString.split()
        msg = AkkuStats()
        if len(tmpTest) > 0:
            msg.bus_voltage = round(float(tmpTest[0]),1)
            msg.load_voltage = round(float(tmpTest[1]),1)
            msg.shunt_voltage = round(float(tmpTest[2]),1)
            msg.current = round(float(tmpTest[3]),1)
            tmpInt = float(tmpTest[4])
            tmpInt = float(tmpInt) 
            msg.power = int(tmpInt)
            self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()