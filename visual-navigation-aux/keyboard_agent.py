#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import sys
import signal
import argparse
import numpy as np

from utils.tools import SimpleImageViewer
from scene_loader import THORDiscreteEnvironment as Environment

import ai2thor.controller
#
# Navigate the scene using your keyboard
#

def key_press(key, mod):

  global human_agent_action, human_wants_restart, stop_requested
  if key == ord('R') or key == ord('r'): # r/R
    human_wants_restart = True
  if key == ord('Q') or key == ord('q'): # q/Q
    stop_requested = True
  if key == 0xFF52: # up
    human_agent_action = 0
  if key == 0xFF53: # right
    human_agent_action = 1
  if key == 0xFF51: # left
    human_agent_action = 2
  if key == 0xFF54: # down
    human_agent_action = 3

def rollout(env):

  global human_agent_action, human_wants_restart, stop_requested
  human_agent_action = None
  human_wants_restart = False
  while True:
    # waiting for keyboard input
    if human_agent_action is not None:
      # move actions
      env.step(human_agent_action)
      env.update()
      if env.terminal:
        print("terminal")
      human_agent_action = None

    # waiting for reset command
    if human_wants_restart:
      # reset agent to random location
      env.reset()
      human_wants_restart = False

    # check collision
    if env.collided:
      print('Collision occurs.')
      env.collided = False

    # check quit command
    if stop_requested: break

    viewer.imshow(env.observation)

if __name__ == '__main__':

  env = Environment({
    'scene_name': 'kitchen_02',
    'terminal_state_id': 'chair1',
    'checkpoint_state_id': 'k_c1'
  })
  # manually disable terminal states
  #env.terminals = np.zeros_like(env.terminals)
  #env.terminal_states, = np.where(env.terminals)
  env.reset()
  #print(env.s_position)

  human_agent_action = None
  human_wants_restart = False
  stop_requested = False

  viewer = SimpleImageViewer()
  viewer.imshow(env.observation)
  viewer.window.on_key_press = key_press
  counter = 0
  
  # tmp = []
  # while True:
  #   counter += 1
  #   env.step_advance(counter)
  #   try:
  #     viewer.saveImage(env.observation, './living_room_08/' + str(counter) + '.png')
  #   except Exception as e:
  #     print("not exist id: " + str(counter))
  #   if counter > 500: break
  
  print("Use arrow keys to move the agent.")
  print("Press R to reset agent\'s location.")
  print("Press Q to quit.")
  
  rollout(env)

  print("Goodbye.")
