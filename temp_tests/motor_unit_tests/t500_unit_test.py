import rospy
from std_msgs.msg import String
from std_msgs.msg import Int16
import time

# note 1250 lower bound, 1750 upper bound, do not know what is forward and backward

# hardcodied the publishing
rospy.init_node('test_t500')
mc = rospy.Publisher('/wamv/t500/motor_cmd', String, queue_size=10)
print("init done")
# to intitialize/stop the motors
time.sleep(3)
pwrL = 1500
pwrR = 1500
pub_str = '{"lp":' + str(pwrL) +  ', "rp":' + str(pwrR) +  '}'
mc.publish(pub_str)
print("step1 done")
time.sleep(3)

#manuvers
pwrL = 1600
pwrR = 1600
pub_str = '{"lp":' + str(pwrL) +  ', "rp":' + str(pwrR) +  '}'
mc.publish(pub_str)
print("step2 done")
time.sleep(10)

#manuvers
#pwrL = 1450
#pwrR = 1450
#pub_str = '{"lp":' + str(pwrL) +  ', "rp":' + str(pwrR) +  '}'
#mc.publish(pub_str)
#print("step3 done")
#time.sleep(3)

pwrL = 1500
pwrR = 1500
pub_str = '{"lp":' + str(pwrL) +  ', "rp":' + str(pwrR) +  '}'
mc.publish(pub_str)
