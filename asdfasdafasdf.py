#!/usr/bin/env python3
# encoding: utf-8

__copyright__ = "Copyright 2022, AAIR Lab, ASU"
__authors__ = ["Abhyudaya Srinet", "Rushang Karia", "Naman Shah"]
__credits__ = ["Siddharth Srivastava"]
__license__ = "MIT"
__version__ = "1.3"
__maintainers__ = ["Pulkit Verma", "Naman Shah"]
__contact__ = "aair.lab@asu.edu"
__docformat__ = 'reStructuredText'



def get_goal_string(object_dict, obj_list, obj_loc_list, goal_list, 
    goal_loc_list,env):
    """
        Returns
        ========
            str:
                A generic goal condition that will place every object based on
                its type and size at the correct goal.
    """

    # Append your goal condition to this string.
    #
    # Below are a few hints to help you along the way:
    # =================================================
    #
    # You can print the parameters to help you in coming up with a generalized
    # goal condition.
    #
    # You can also look at the (:objects) and (:init) of problem.pddl to give
    # you an idea of where your goal string is going wrong.
    #
    # Keep in mind the subject type and sizes of the bins and the books must
    # match.
    #
    # High level plans do not need actual co-ordinates, rather they use the
    # high-level locations found in the parameters of this method.
    #
    # Finally, there exists a way to write the goal condition using universal
    # and existential quantifiers.
    #
    # Executing wrong plans on Gazebo might not give you the right execution!
    #
    # Remember that the two environments have unique objects, goals and predicates!
    
    goal_string = "(:goal (and "

    goal_location = dict(zip(goal_list, goal_loc_list))

    if env == "bookWorld":
        #TODO: 
        # Replace this with the correct goal for bookWorld environment
        for objects in obj_list:
            object_info = object_dict[objects]
            object_subject = object_info["subject"]
            object_size = object_info["size"]

            matched_goal = None

            for goal in goal_list:
                goal_info = object_dict[goal]
                
                if goal_info["subject"] == object_subject and goal_info["size"] == object_size:
                    matched_goal = goal
                    break
                
            if matched_goal is None:
                raise ValueError(f"Matching is not founded for {objects} (subject={object_subject}, size={object_size})")        
                
            final_goal_location = goal_location[matched_goal]
            goal_string += f"(Book_At {objects} {final_goal_location}) "


    elif env == "cafeWorld":
        #TODO:
        # Replace this with the correct goal for cafeWorld environment

        for objects in obj_list:
            object_info = object_dict[objects]
            object_type = object_info["food_type"]
            object_size = object_info["size"]

            matched_goal = None

            for goal in goal_list:
                goal_info = object_dict[goal]
                if goal_info["food_type"] == object_type and goal_info['size'] == object_size:
                    matched_goal = goal
                    break
            
            if matched_goal is None:
                raise ValueError(f"Matching is not founded for {objects} (food_type={object_type}, size={object_size})")

            final_goal_location = goal_location[matched_goal]
            
            goal_string += f"(Food_At {objects} {final_goal_location}) "
    
    goal_string += "))\n"
    
    return goal_string

def sample_goal_condition(object_dict, obj_list, obj_loc_list, goal_list, 
    goal_loc_list):
    """
        Returns
        ========
            str:
                A generic goal condition that moves the robot to any one of
                the object locations.

        
        .. note ::

            You can replace the contents of get_goal_string() with the text below
            to get an idea of what is expected.
            
            The goal condition in the stock task here is VASTLY different from the
            expectation from you. Please review the homework documentation to identify
            your task.
            
            Here are some instructions to run this in Gazebo.
            1. Replace the content of get_goal_string() with this method.
            2. rosrun hw2 refinement.py \
                --objtypes <object types> \
                --objcount <number of objects> \
                --seed <seed>
            3. rosrun hw2 gazebo.py

            The generic goal condition here is to move the robot to a object location.
            
            The stock task below generates a generic goal condition that moves the
            robot to a random object location and this is independent of the total 
            number of locations and objects. 
            
    """

    import random
    assert len(obj_loc_list) > 0
    i = random.randint(0, len(obj_loc_list) - 1)
    
    goal_string = "(:goal (and "
    goal_string += "(Robot_At tbot3 %s)" % (obj_loc_list[i])
    goal_string += "))\n"
    
    return goal_string
