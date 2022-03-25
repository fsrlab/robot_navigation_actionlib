# robot_navigation_pointAPI

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseResult

import tf
import tf.transformations

station = [1.09, 1.76, .0]
ore1 = [0.93, 3.25, 3.14]
ore2 = [0.06, 2.90, 5.49]
ore3 = [2.00, 2.70, .0]
ore4 = [2.32, 0.25, 3.14]
ore5 = [2.63, -0.89, .0]
points = [station, ore1, ore2, ore3, ore4, ore5]


def robot_navi(x, y, theta):
    '''
        对机器人进行导航
        input: x, y, theta 相对于初始值坐标
        return: state(3=正常到达)
    '''
    # TODO: 加入范围限制

    # 转换四元数
    q = tf.transformations.quaternion_from_euler(.0, .0, theta)

    # 初始化节点
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()
    
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = 'map'
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.orientation.x = q[0]
    goal.target_pose.pose.orientation.y = q[1]
    goal.target_pose.pose.orientation.z = q[2]
    goal.target_pose.pose.orientation.w = q[3]

    client.send_goal(goal)
    wait = client.wait_for_result()

    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_state()



if __name__ == "__main__":
    # 仅测试
    rospy.init_node('move_base_client')
    for point in points:
        try:
            state = robot_navi(point[0], point[1], point[2])
            if state:
                rospy.loginfo(str(state))
        except rospy.ROSInterruptException:
            rospy.loginfo("Navigation test finished.")