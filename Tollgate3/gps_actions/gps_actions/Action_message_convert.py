##!/usr/bin/env python3

import re


class MessageTransformer(object):
    
    def splitter_actions(self,msg):
#         pattern = re.compile(r";|,|[|] ")
#         delimiters = ",", " ", "[", "]"
        split_string = str(msg).split(',')
        action_id=split_string[0];
        #print(action_id)
        robot_id=split_string[1];
        #print(robot_id)
        return action_id, robot_id
    
#     def splitter_robot(self,msg):
#         pattern = re.compile(r";|,|[|] ")
# #         delimiters = ",", " ", "[", "]"
#         split_string = msg.split(msg)
#         action_id=split_string[0];
#         robot_id=split_string[1];
#         return robot_id
    

def main():

     print("Starting..")  
     q=MessageTransformer()
     t=q.splitter_actions('k, 4')
     print(t[1])

if __name__ == '__main__':
     main()
