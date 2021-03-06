# coding=utf-8
# Copyright 2019 The Tensor2Tensor Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""PPO binary over a gym env."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import functools

from absl import app
from absl import flags
from absl import logging
from tensor2tensor.trax import stax
from tensor2tensor.trax.rlax import ppo

FLAGS = flags.FLAGS

flags.DEFINE_string("env_name", None, "Name of the environment to make.")
flags.DEFINE_string("t2t_gym_env", None, "Name of the T2TGymEnv to make.")
flags.DEFINE_integer("epochs", 100, "Number of epochs to run for.")
flags.DEFINE_integer("random_seed", 0, "Random seed.")
flags.DEFINE_integer("log_level", logging.INFO, "Log level.")
flags.DEFINE_integer("batch_size", 32, "Batch of trajectories needed.")
flags.DEFINE_integer("boundary", 20,
                     "We pad trajectories at integer multiples of this number.")


def common_stax_layers():
  return [stax.Dense(16), stax.Relu, stax.Dense(4), stax.Relu]


def main(argv):
  del argv
  logging.set_verbosity(FLAGS.log_level)
  bottom_layers = common_stax_layers()

  if FLAGS.env_name == "Pong-v0":
    bottom_layers = [stax.Div(255.0), stax.Flatten(2)] + bottom_layers

  ppo.training_loop(
      env_name=FLAGS.env_name,
      epochs=FLAGS.epochs,
      policy_net_fun=functools.partial(
          ppo.policy_net, bottom_layers=bottom_layers),
      value_net_fun=functools.partial(
          ppo.value_net, bottom_layers=bottom_layers),
      batch_size=FLAGS.batch_size,
      boundary=FLAGS.boundary,
      random_seed=FLAGS.random_seed)


if __name__ == "__main__":
  app.run(main)
